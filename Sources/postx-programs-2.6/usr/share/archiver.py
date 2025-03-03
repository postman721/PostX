import sys
import os
import zipfile
import tarfile

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QDialog,
    QTextEdit,
    QTreeView,
    QFileSystemModel,
    QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDir

##########################
# CONFIG AND HELPER LOGIC
##########################

SUPPORTED_EXTENSIONS = [
    ".zip",
    ".tar",
    ".tar.gz", ".tgz",
    ".tar.bz2", ".tbz2",
    ".tar.xz", ".txz",
]

# Maps user-selected filters to a "primary" extension
FILTER_TO_EXTENSION = {
    "Zip (*.zip)": ".zip",
    "Tar (*.tar)": ".tar",
    "Tar GZ (*.tar.gz *.tgz)": ".tar.gz",
    "Tar BZ2 (*.tar.bz2 *.tbz2)": ".tar.bz2",
    "Tar XZ (*.tar.xz *.txz)": ".tar.xz",
}


def determine_tar_mode_compress(filename: str) -> str:
    """
    Pick tarfile write mode based on extension:
      *.tar      -> "w"
      *.tar.gz,
      *.tgz      -> "w:gz"
      *.tar.bz2,
      *.tbz2     -> "w:bz2"
      *.tar.xz,
      *.txz      -> "w:xz"
    Default -> "w"
    """
    fn = filename.lower()
    if fn.endswith(".tar"):
        return "w"
    elif fn.endswith((".tar.gz", ".tgz")):
        return "w:gz"
    elif fn.endswith((".tar.bz2", ".tbz2")):
        return "w:bz2"
    elif fn.endswith((".tar.xz", ".txz")):
        return "w:xz"
    else:
        return "w"


def determine_tar_mode_decompress(filename: str) -> str:
    """
    Pick tarfile read mode based on extension.
    """
    fn = filename.lower()
    if fn.endswith(".tar"):
        return "r"
    elif fn.endswith((".tar.gz", ".tgz")):
        return "r:gz"
    elif fn.endswith((".tar.bz2", ".tbz2")):
        return "r:bz2"
    elif fn.endswith((".tar.xz", ".txz")):
        return "r:xz"
    else:
        return "r"


def maybe_add_extension(out_path: str, selected_filter: str) -> str:
    """
    If the user didn't type a recognized extension,
    append the extension from the chosen filter.
    """
    lower = out_path.lower()
    # If the user already typed one of our known extensions, do nothing
    if any(lower.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
        return out_path

    # Otherwise, see which filter was selected
    for filter_text, ext in FILTER_TO_EXTENSION.items():
        if filter_text in selected_filter:
            return out_path + ext

    # If no known match, just return as-is
    return out_path


##########################
# CUSTOM SELECTION DIALOG
##########################

class CustomSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Files and Folders to Compress")
        self.resize(600, 400)
        layout = QVBoxLayout(self)

        # Use a QTreeView with a QFileSystemModel to display the file system.
        self.tree = QTreeView(self)
        self.tree.setSelectionMode(QTreeView.ExtendedSelection)
        self.model = QFileSystemModel(self)
        self.model.setRootPath(QDir.homePath())
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))
        # Optionally hide extra columns (size, type, date modified)
        self.tree.setColumnWidth(0, 250)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        layout.addWidget(self.tree)

        # Ok and Cancel buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def selected_paths(self):
        """
        Returns a list of selected file and folder paths.
        """
        indexes = self.tree.selectionModel().selectedIndexes()
        paths = set()
        for index in indexes:
            # Only consider the first column to avoid duplicates
            if index.column() == 0:
                paths.add(self.model.filePath(index))
        return list(paths)


##########################
# MAIN WIDGET / APP LOGIC
##########################

class ArchiveHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Set up the main window, layout, and widgets."""
        self.setWindowTitle("Compressor & Archive Inspector")

        layout = QVBoxLayout()

        # 1) Compress Folder Button (now using custom selection dialog)
        self.compress_folder_button = QPushButton("Compress Files/Folders")
        self.compress_folder_button.clicked.connect(self.compress_folder)

        # 2) View Archive Button (inspect archive contents)
        self.view_archive_button = QPushButton("View Archive Contents")
        self.view_archive_button.clicked.connect(self.view_archive_contents)

        # 3) Decompress Archive Button
        self.decompress_button = QPushButton("Decompress Archive")
        self.decompress_button.clicked.connect(self.decompress_archive)

        # Status Label
        self.status_label = QLabel("Select an action.")
        self.status_label.setFont(QFont("Arial", 10))

        layout.addWidget(self.compress_folder_button)
        layout.addWidget(self.view_archive_button)
        layout.addWidget(self.decompress_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    ########################
    # 1) COMPRESS SELECTED ITEMS
    ########################
    def compress_folder(self):
        """
        Opens a custom dialog that allows the user to select one or more files and/or folders.
        Then prompts for an archive name and compresses the selected items.
        """
        selected_items = self._open_custom_selection_dialog()
        if not selected_items:
            return

        file_filter = (
            "Zip (*.zip);;"
            "Tar (*.tar);;"
            "Tar GZ (*.tar.gz *.tgz);;"
            "Tar BZ2 (*.tar.bz2 *.tbz2);;"
            "Tar XZ (*.tar.xz *.txz);;"
            "All Archives (*.zip *.tar *.tar.gz *.tgz *.tar.bz2 *.tbz2 *.tar.xz *.txz);;"
            "All Files (*.*)"
        )
        out_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            caption="Save compressed file as",
            filter=file_filter
        )
        if not out_path:
            return  # user canceled

        out_path = maybe_add_extension(out_path, selected_filter)

        # Validate extension
        if not self._check_supported_extension(out_path):
            return

        if out_path.lower().endswith(".zip"):
            self._compress_zip_items(selected_items, out_path)
        else:
            self._compress_tar_items(selected_items, out_path)

    def _open_custom_selection_dialog(self):
        """
        Opens the custom dialog to select files and folders.
        """
        dialog = CustomSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.selected_paths()
        return []

    def _compress_zip_items(self, selected_items, out_path):
        """
        Compress the selected files/folders into a ZIP archive.
        """
        try:
            # Compute a common base for relative paths.
            common_base = os.path.commonpath(selected_items)
        except ValueError:
            # Fallback: if items are on different drives (Windows), use empty base.
            common_base = ""
        try:
            with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for item in selected_items:
                    if os.path.isfile(item):
                        arcname = os.path.relpath(item, common_base) if common_base else os.path.basename(item)
                        zf.write(item, arcname=arcname)
                    elif os.path.isdir(item):
                        for root, dirs, files in os.walk(item):
                            for file_name in files:
                                full_path = os.path.join(root, file_name)
                                arcname = os.path.relpath(full_path, common_base) if common_base else os.path.basename(full_path)
                                zf.write(full_path, arcname=arcname)
            self.status_label.setText(f"Compressed selected items into '{out_path}'")
        except Exception as e:
            self.status_label.setText(f"Error compressing selected items to ZIP: {e}")

    def _compress_tar_items(self, selected_items, out_path):
        """
        Compress the selected files/folders into a TAR-based archive.
        """
        mode = determine_tar_mode_compress(out_path)
        try:
            common_base = os.path.commonpath(selected_items)
        except ValueError:
            common_base = ""
        try:
            with tarfile.open(out_path, mode=mode) as tar:
                for item in selected_items:
                    arcname = os.path.relpath(item, common_base) if common_base else os.path.basename(item)
                    tar.add(item, arcname=arcname)
            self.status_label.setText(f"Compressed selected items into '{out_path}'")
        except Exception as e:
            self.status_label.setText(f"Error compressing selected items to TAR: {e}")

    ########################
    # 2) VIEW ARCHIVE CONTENTS
    ########################
    def view_archive_contents(self):
        """
        Lets the user pick an existing archive, then displays its contents
        (filenames) in a popup text box.
        """
        archive_path = self._open_file_dialog_for_archive()
        if not archive_path:
            return

        try:
            contents_list = self._inspect_archive(archive_path)
            self._show_contents_dialog(archive_path, contents_list)
        except Exception as e:
            self.status_label.setText(f"Error viewing archive: {e}")

    def _inspect_archive(self, archive_path):
        """
        Returns a list of filenames inside the archive.
        """
        archive_lower = archive_path.lower()
        if archive_lower.endswith(".zip"):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                return zf.namelist()
        else:
            mode = determine_tar_mode_decompress(archive_path)
            with tarfile.open(archive_path, mode=mode) as tar:
                return tar.getnames()

    def _show_contents_dialog(self, archive_path, contents_list):
        """
        Shows a dialog with the names of all files/folders inside the archive.
        """
        text = f"Archive: {archive_path}\n\n"
        if not contents_list:
            text += "[No files found in this archive]"
        else:
            for item in contents_list:
                text += item + "\n"

        dlg = QDialog(self)
        dlg.setWindowTitle("Archive Contents")
        dlg.resize(500, 400)

        layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text)

        layout.addWidget(text_edit)
        dlg.setLayout(layout)

        dlg.exec_()

    ########################
    # 3) DECOMPRESS ARCHIVE
    ########################
    def decompress_archive(self):
        """
        Lets the user pick a supported archive, then choose a directory to extract to.
        """
        archive_path = self._open_file_dialog_for_archive()
        if not archive_path:
            return

        extract_dir = QFileDialog.getExistingDirectory(
            self,
            caption="Select extraction directory"
        )
        if not extract_dir:
            return

        try:
            self._decompress(archive_path, extract_dir)
        except Exception as e:
            self.status_label.setText(f"Error decompressing file: {e}")

    def _open_file_dialog_for_archive(self):
        """
        Opens a dialog for selecting a ZIP or TAR-based archive.
        """
        archive_path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Select archive",
            filter=(
                "All Supported Archives (*.zip *.tar *.tar.gz *.tgz "
                "*.tar.bz2 *.tbz2 *.tar.xz *.txz);;"
                "All Files (*.*)"
            )
        )
        return archive_path

    def _decompress(self, archive_path, extract_dir):
        """
        Decompress the chosen archive into extract_dir.
        """
        archive_lower = archive_path.lower()
        if archive_lower.endswith(".zip"):
            self._decompress_zip(archive_path, extract_dir)
        else:
            self._decompress_tar(archive_path, extract_dir)

    def _decompress_zip(self, archive_path, extract_dir):
        try:
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(extract_dir)
            self.status_label.setText(
                f"Decompressed '{archive_path}' into '{extract_dir}'"
            )
        except Exception as e:
            raise RuntimeError(f"Error decompressing ZIP: {e}")

    def _decompress_tar(self, archive_path, extract_dir):
        mode = determine_tar_mode_decompress(archive_path)
        try:
            with tarfile.open(archive_path, mode=mode) as tar:
                tar.extractall(path=extract_dir)
            self.status_label.setText(
                f"Decompressed '{archive_path}' into '{extract_dir}'"
            )
        except Exception as e:
            raise RuntimeError(f"Error decompressing TAR: {e}")

    ############################
    # HELPER / VALIDATION
    ############################
    def _check_supported_extension(self, out_path: str) -> bool:
        """
        Ensure the output archive has one of our recognized extensions.
        If not, warn the user.
        """
        if not any(out_path.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            QMessageBox.warning(
                self,
                "Unsupported Extension",
                "Please use one of the supported extensions:\n" +
                ", ".join(SUPPORTED_EXTENSIONS)
            )
            return False
        return True


def main():
    app = QApplication(sys.argv)

    # Apply a dark QSS theme for a sleek look
    dark_stylesheet = """
    QWidget {
        background-color: #2F2F2F;
        color: #FFFFFF;
        font-family: "Segoe UI", sans-serif;
        font-size: 10pt;
    }
    QPushButton {
        background-color: #444444;
        color: #FFFFFF;
        border: 1px solid #666666;
        border-radius: 4px;
        padding: 6px;
    }
    QPushButton:hover {
        background-color: #555555;
    }
    QLabel {
        color: #FFFFFF;
    }
    QTextEdit {
        background-color: #3F3F3F;
        color: #FFFFFF;
        border: 1px solid #666666;
    }
    QMessageBox {
        background-color: #2F2F2F;
        color: #FFFFFF;
    }
    """
    app.setStyleSheet(dark_stylesheet)

    window = ArchiveHandler()
    window.resize(600, 300)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
