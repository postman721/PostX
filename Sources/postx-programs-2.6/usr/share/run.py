#!/usr/bin/env python3
#Runner-QT v.8 Copyright (c) 2017 JJ Posti <techtimejourney.net> This program comes with ABSOLUTELY NO WARRANTY;  for details see: http://www.gnu.org/copyleft/gpl.html.  This is free software, and you are welcome to redistribute it under  GPL Version 2, June 1991")

import os
import sys
import subprocess
import shutil

from PyQt5 import QtCore
from PyQt5.QtCore import Qt  
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QMessageBox

class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
           
        # A bit more modern outlook
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3A3A;
            }
            
            QLineEdit {
                border: 2px solid #555;
                border-radius: 15px;
                padding: 5px;
                background-color: #333;
                color: #EEE;
            }
            
            QMessageBox {
                background-color: #2E3A3A;
            }
            
            QLabel {
                color: #EEE;
            }
            
            QPushButton {
                color: #EEE;
                background-color: #555;
                border-radius: 5px;
                padding: 5px 15px;
            }
            
            QPushButton:hover {
                background-color: #666;
            }
        """)
        
        # Text
        self.address = QLineEdit(self)
        self.address.setAlignment(Qt.AlignCenter)
        self.address.setFixedSize(320, 35)
        self.address.returnPressed.connect(self.navigatex)
        
        # Set main window size to fit just the QLineEdit
        self.setFixedSize(self.address.width(), self.address.height())
        
        # Center the application on the screen
        screen_geo = QApplication.primaryScreen().geometry()
        window_geo = self.geometry()
        self.move((screen_geo.width() - window_geo.width()) // 2, (screen_geo.height() - window_geo.height()) // 2)


# Frameless might be bad for dual screen setups. Disabling due to this.
       
        # Make a Frameless window & Disable grip
        #self.frameless = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(self.frameless)

    def navigatex(self):
        self.location = self.address.text().split()[0]  # Get the first word, assuming it's the command/program name.

        # Check if the program exists
        if shutil.which(self.location):
            try:
                self.process = subprocess.Popen(self.address.text(), shell=True)
                self.close()
            except Exception as e:
                # Notify the user of any exceptions.
                QMessageBox.critical(self, "Execution Error", f"Failed to execute '{self.location}': {str(e)}")
        else:
            # Notify the user that the program doesn't exist.
            QMessageBox.critical(self, "Error", f"'{self.location}' does not exist or is not executable.")

    # Quit program
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show() 
    sys.exit(app.exec_())
