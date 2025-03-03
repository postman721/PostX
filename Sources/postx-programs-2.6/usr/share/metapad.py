from PyQt5.QtCore import (Qt, QRegExp, QRect, QUrl, QSize, pyqtSignal)
from PyQt5.QtGui import (QFont, QIcon, QPainter, QTextCharFormat, QSyntaxHighlighter, 
                         QTextCursor, QColor, QTextDocument)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPlainTextEdit,
                             QToolBar, QAction, QLabel, QFileDialog, QMessageBox, 
                             QFontDialog, QInputDialog, QDialog, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QCheckBox)
from PyQt5.QtPrintSupport import QPrintPreviewDialog
import sys, os

# ---- Syntax Highlighter (Optional) ----
class PythonHighlighter(QSyntaxHighlighter):
    """A basic Python syntax highlighter."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_highlighting_rules()

    def init_highlighting_rules(self):
        # Generic format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.cyan)
        keyword_format.setFontWeight(QFont.Bold)

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.green)

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(Qt.yellow)

        # Python Keywords
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'True', 'try', 'while', 'with', 'yield'
        ]

        self.highlighting_rules = []
        # Keyword patterns
        for word in keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((pattern, keyword_format))

        # Comment pattern (start with # until end of line)
        self.highlighting_rules.append((r'#[^\n]*', comment_format))

        # String patterns
        # Single-quoted string
        self.highlighting_rules.append((r'\'[^\']*\'', string_format))
        # Double-quoted string
        self.highlighting_rules.append((r'\"[^\"]*\"', string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)


# ---- Line Number Area ----
class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.metapad = editor

    def sizeHint(self):
        return QSize(self.metapad.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.metapad.lineNumberAreaPaintEvent(event)


# ---- Main Editor (Metapad) ----
class Metapad(QPlainTextEdit):
    cursorPositionChangedSignal = pyqtSignal(int, int)  # custom signal to update line/col in status bar

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)

        # Connect cursor position changes to a method that emits line/col
        self.cursorPositionChanged.connect(self.onCursorPositionChanged)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value //= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), 
                                       self.lineNumberArea.size().width(), 
                                       rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 
                                              self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.yellow)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()

        while block.isValid() and (top <= event.rect().bottom()):
            number = str(blockNumber + 1)
            painter.setPen(Qt.black)
            painter.drawText(0, top, self.lineNumberArea.width(), height, 
                             Qt.AlignCenter, number)
            block = block.next()
            top = int(bottom)
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def onCursorPositionChanged(self):
        # Emit current line and column.
        # Calculate column as the difference between the cursor's absolute position and the block's position.
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.position() - cursor.block().position() + 1
        self.cursorPositionChangedSignal.emit(line, col)


# ---- Find & Replace Dialog ----
class FindReplaceDialog(QDialog):
    def __init__(self, parent=None, editor=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Find & Replace")
        self.setModal(False)
        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        # Find input
        find_layout = QHBoxLayout()
        find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        # Replace input
        replace_layout = QHBoxLayout()
        replace_label = QLabel("Replace:")
        self.replace_input = QLineEdit()
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        # Match case checkbox
        self.match_case_checkbox = QCheckBox("Match case")
        layout.addWidget(self.match_case_checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        self.find_button = QPushButton("Find Next")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.replace_button)
        button_layout.addWidget(self.replace_all_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setFixedSize(400, 160)

        # Signals
        self.find_button.clicked.connect(self.find_next)
        self.replace_button.clicked.connect(self.replace_one)
        self.replace_all_button.clicked.connect(self.replace_all)

    def find_flags(self):
        """Returns appropriate QTextDocument.FindFlags based on user selections."""
        flags = QTextDocument.FindFlags()  # default flags (i.e. 0)
        if self.match_case_checkbox.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        return flags

    def find_next(self):
        text = self.find_input.text()
        if text:
            if not self.editor.find(text, self.find_flags()):
                # If not found, move cursor to start and try again
                cursor = self.editor.textCursor()
                cursor.movePosition(QTextCursor.Start)
                self.editor.setTextCursor(cursor)
                self.editor.find(text, self.find_flags())

    def replace_one(self):
        text_find = self.find_input.text()
        text_replace = self.replace_input.text()
        cursor = self.editor.textCursor()

        if not cursor.hasSelection():
            # Find next occurrence first
            self.find_next()
            return

        # If the selected text matches, replace
        if (cursor.selectedText() == text_find or 
            (not self.match_case_checkbox.isChecked() and cursor.selectedText().lower() == text_find.lower())):
            cursor.insertText(text_replace)
        self.find_next()  # Move on to the next occurrence

    def replace_all(self):
        text_find = self.find_input.text()
        text_replace = self.replace_input.text()

        if not text_find:
            return

        # Move cursor to the start
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.editor.setTextCursor(cursor)

        count = 0
        while self.editor.find(text_find, self.find_flags()):
            cursor = self.editor.textCursor()
            cursor.insertText(text_replace)
            count += 1

        QMessageBox.information(self, "Replace All", f"Replaced {count} occurrence(s).")


# ---- MainWindow ----
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metapad")

        # Center on screen
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        # Create the text editor
        self.metapad = Metapad(self)
        self.resize(800, 600)

        # (Optional) Syntax highlighting for Python
        self.highlighter = PythonHighlighter(self.metapad.document())

        # Create main toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # -------- Add actions to the toolbar --------
        # Open
        open_icon = QIcon.fromTheme("document-open")
        open_action = QAction(open_icon, 'Open', self)
        open_action.triggered.connect(self.openFile)
        self.toolbar.addAction(open_action)

        # Undo
        undo_icon = QIcon.fromTheme("edit-undo")
        undo_action = QAction(undo_icon, 'Undo', self)
        undo_action.triggered.connect(self.undo)
        self.toolbar.addAction(undo_action)

        # Redo
        redo_icon = QIcon.fromTheme("edit-redo")
        redo_action = QAction(redo_icon, 'Redo', self)
        redo_action.triggered.connect(self.redo)
        self.toolbar.addAction(redo_action)

        # Save
        save_icon = QIcon.fromTheme("document-save")
        save_action = QAction(save_icon, 'Save', self)
        save_action.triggered.connect(self.saveFile)
        self.toolbar.addAction(save_action)

        # Print
        print_icon = QIcon.fromTheme("document-print")
        print_action = QAction(print_icon, 'Print', self)
        print_action.triggered.connect(self.printing)
        self.toolbar.addAction(print_action)

        # Font
        font_icon = QIcon.fromTheme("preferences-desktop-font")
        font_action = QAction(font_icon, 'Font', self)
        font_action.triggered.connect(self.changeFont)
        self.toolbar.addAction(font_action)

        # Exit
        close_icon = QIcon.fromTheme("application-exit")
        close_action = QAction(close_icon, 'Exit', self)
        close_action.triggered.connect(self.close)
        self.toolbar.addAction(close_action)

        # -------- Create a second toolbar for file address info --------
        self.address_toolbar = QToolBar("File Path")
        self.addToolBar(self.address_toolbar)
        self.address = QLabel()
        self.address.setText('')
        self.address_toolbar.addWidget(self.address)

        # -------- Menubar setup --------
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(print_action)
        file_menu.addSeparator()
        file_menu.addAction(close_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        # Find & Replace
        find_replace_action = QAction("Find & Replace", self)
        find_replace_action.triggered.connect(self.openFindReplaceDialog)
        edit_menu.addAction(find_replace_action)

        # Go to line
        goto_line_action = QAction("Go to Line", self)
        goto_line_action.triggered.connect(self.gotoLine)
        edit_menu.addAction(goto_line_action)

        # Word Wrap Toggle
        self.word_wrap_action = QAction("Word Wrap", self, checkable=True)
        self.word_wrap_action.setChecked(True)  # start with wrap on
        self.word_wrap_action.triggered.connect(self.toggleWordWrap)
        edit_menu.addAction(self.word_wrap_action)

        edit_menu.addSeparator()
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)

        # -------- Status Bar (Line/Column) --------
        self.status = self.statusBar()
        self.status.showMessage("Ready")

        # Connect our custom signal from Metapad to update the status bar
        self.metapad.cursorPositionChangedSignal.connect(self.updateStatusBar)

        # -------- Set central widget --------
        self.setCentralWidget(self.metapad)

        # -------- Styling --------
        self.setStyleSheet("""
            background-color: #434C5E; 
            color: #FAFAFA; 
            border: 1px solid #393F4B; 
            border-radius: 6px; 
            font-size: 14px; 
            selection-background-color: #2B3345; 
            padding: 6px; 
            QToolBar QToolButton {
                background-color: #5E6977; 
                color: #FFFFFF; 
                border: 1px solid #505C6C; 
                font-weight: 500; 
                padding: 4px; 
                margin: 3px; 
                min-width: 18px; 
                min-height: 18px; 
                border-radius: 4px; 
            }
            QToolBar QToolButton:hover {
                background-color: #697885; 
            }
            QMenu::item:selected { 
                background-color: #5E6977; 
            }
            QMenu::item:hover { 
                background-color: #6C7684; 
            }
        """)
        self.metapad.setStyleSheet("""
            QPlainTextEdit {
                background-color: #343D4C; 
                color: #F5F5F5; 
                border: 1px solid #2D3643; 
                border-radius: 6px; 
                font-size: 15px; 
                selection-background-color: #404A58; 
                padding: 6px;
            }
        """)

        # Default font
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

        # Keep reference to Find & Replace dialog
        self.find_replace_dialog = None

    # ----- Additional Feature Methods -----

    def updateStatusBar(self, line, col):
        self.status.showMessage(f"Line: {line}, Col: {col}")

    def toggleWordWrap(self):
        if self.word_wrap_action.isChecked():
            self.metapad.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        else:
            self.metapad.setLineWrapMode(QPlainTextEdit.NoWrap)

    def gotoLine(self):
        line, ok = QInputDialog.getInt(self, "Go to Line", "Line number:", 1, 1)
        if ok and line > 0:
            cursor = self.metapad.textCursor()
            block_count = self.metapad.blockCount()
            if line <= block_count:
                cursor.movePosition(QTextCursor.Start)
                cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line - 1)
                self.metapad.setTextCursor(cursor)

    def openFindReplaceDialog(self):
        if not self.find_replace_dialog:
            self.find_replace_dialog = FindReplaceDialog(self, self.metapad)
        self.find_replace_dialog.show()
        self.find_replace_dialog.raise_()
        self.find_replace_dialog.activateWindow()

    # ----- Original Methods (with minor adjustments) -----
    def changeFont(self):
        font, ok = QFontDialog.getFont(self.metapad.font(), self, 
                                       'Select a font (applies to selected text if present).')
        if ok:
            cursor = self.metapad.textCursor()
            fmt = QTextCharFormat()
            fmt.setFont(font)
            cursor.mergeCharFormat(fmt)
            self.metapad.setTextCursor(cursor)

    def undo(self):
        self.metapad.undo()

    def redo(self):
        self.metapad.redo()

    def closeEvent(self, event):
        buttonReply = QMessageBox.question(self.metapad, 'Quit now?',
                                           "All unsaved documents will be lost. "
                                           "If unsure press Cancel now.",
                                           QMessageBox.Cancel | QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            print('Ok clicked, messagebox closed.')
            event.accept()
            print("\nProgram ends. Goodbye.\n")
        else:
            print("Do not quit. --> Going back to the program.")
            event.ignore()

    def openFile(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self.metapad,
                                                      "Open a file",
                                                      "",
                                                      "All Files (*);;Text Files (*.txt);;"
                                                      "Python Files (*.py);;C++ Files (*.cpp);;"
                                                      "Bash Files (*.sh);;Javascript Files (*.js);;"
                                                      "Odt text files (*.odt)",
                                                      options=options)
            if fileName:
                buttonReply = QMessageBox.question(self.metapad, 'Open new file?',
                                                   "All unsaved documents will be lost. "
                                                   "If unsure press Cancel now.",
                                                   QMessageBox.Cancel | QMessageBox.Ok)
                if buttonReply == QMessageBox.Ok:
                    with open(fileName, 'r', encoding='utf-8', errors='ignore') as f:
                        alltxt = f.read()
                        self.metapad.setPlainText(alltxt)
                    filename = os.path.basename(fileName)
                    self.address.setText('Now viewing: ' + filename)
        except Exception as e:
            print("Cannot handle, Will not continue. Error:", e)

    def saveFile(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self.metapad,
                                                      "Save as",
                                                      "",
                                                      "All Files (*);;Text Files (*.txt);;"
                                                      "Python Files (*.py);;C++ Files (*.cpp);;"
                                                      "Bash Files (*.sh);;Javascript Files (*.js);;"
                                                      "Odt text Files (*.odt)",
                                                      options=options)
            if fileName:
                with open(fileName, 'w', encoding='utf-8') as f:
                    f.write(self.metapad.toPlainText())
                filename = os.path.basename(fileName)
                self.address.setText('Now viewing: ' + filename)
        except Exception as e:
            print("Cannot handle, Will not continue. Error:", e)

    def printing(self):
        preview = QPrintPreviewDialog()
        preview.paintRequested.connect(lambda x: self.metapad.print_(x))
        preview.exec_()

    def close(self):
        buttonReply = QMessageBox.question(self.metapad, 'Quit now?',
                                           "All unsaved documents will be lost. "
                                           "If unsure press Cancel now.",
                                           QMessageBox.Cancel | QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            print('Ok clicked, messagebox closed.')
            QApplication.instance().quit()
            print("\nProgram ends. Goodbye.\n")
        else:
            print("Do not quit. --> Going back to the program.")

    def showAbout(self):
        QMessageBox.information(self, "About Metapad v3.0",
                                "Metapad v3.0\n\n"
                                "Copyright (c) 2017 JJ Posti <techtimejourney.net>\n"
                                "Improved Features Example\n\n"
                                "This program comes with ABSOLUTELY NO WARRANTY.\n"
                                "Distributed under GPL v2.\n\n"
                                "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html")


# ---- Main Entry Point ----
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Optional: Zoom the text a bit for readability
    window.metapad.zoomIn(1)

    sys.exit(app.exec_())
