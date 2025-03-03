import os, sys, subprocess, getpass
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Main(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)
        self.setStyleSheet("*{color:#ffffff; background-color:#2f2e2d; border: 2px solid #353535; border-radius: 3px;font-size: 12px;}"
                           "*:selected{background-color:#125c8c;}")
        self.openFileNameDialog()
           
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose wallpaper", "/usr/share/postx-wallpapers", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            subprocess.Popen(['feh', '--bg-scale', fileName])
            name = getpass.getuser()
            uhome = "/home/"
            wall = ".wall/wall.sh"        
            combine = os.path.join(uhome, name, wall)
            folder = os.path.join(uhome, name)
            fehcommand = "feh --bg-scale "

            # Create the folder if it doesn't exist
            if not os.path.exists(os.path.dirname(combine)):
                os.makedirs(os.path.dirname(combine))

            if os.path.exists(combine):
                os.remove(combine)

            with open(combine, 'a') as f:
                f.write(fehcommand)
                f.write(fileName)
                f.write('\n')

            sys.exit()
        else:
            sys.exit()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
