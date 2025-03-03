#!/usr/bin/env python3

#QCalculator 2.1 Copyright (c) 2018 JJ Posti <techtimejourney.net> 
#QCalculator comes with ABSOLUTELY NO WARRANTY; 
#for details see: http://www.gnu.org/copyleft/gpl.html. 
#This is free software, and you are welcome to redistribute it under 
#GPL Version 2, June 1991.

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os, sys

class Ui_MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(370, 396)
        MainWindow.setMinimumSize(QSize(370, 396))
        MainWindow.setMaximumSize(QSize(370, 396))
        MainWindow.setStyleSheet(("* {border: none; color: #e3e0d8; background-color: #1b1b1b; selection-background-color:#080912;selection-color: #3f3f40; margin-top:14px; margin-bottom:14px; }")) 
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(10, 10, 341, 381))
        self.frame.setMinimumSize(QSize(24, 53))
        font = QFont()
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.display = QLineEdit(self.frame)
        self.display.setGeometry(QRect(10, 10, 311, 42))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.display.sizePolicy().hasHeightForWidth())
        self.display.setSizePolicy(sizePolicy)
        self.display.setMinimumSize(QSize(24, 42))
        self.display.setObjectName("display")
        self.button_1 = QPushButton(self.frame)
        self.button_1.setGeometry(QRect(10, 58, 75, 53))
        self.button_1.setMinimumSize(QSize(24, 53))
        self.button_1.setMaximumSize(QSize(16777215, 53))
        self.button_1.setObjectName("button_1")
        self.button_2 = QPushButton(self.frame)
        self.button_2.setGeometry(QRect(91, 58, 75, 53))
        self.button_2.setMinimumSize(QSize(24, 53))
        self.button_2.setMaximumSize(QSize(16777215, 53))
        self.button_2.setObjectName("button_2")
        self.button_3 = QPushButton(self.frame)
        self.button_3.setGeometry(QRect(172, 58, 75, 53))
        self.button_3.setMinimumSize(QSize(24, 53))
        self.button_3.setMaximumSize(QSize(16777215, 53))
        self.button_3.setObjectName("button_3")
        self.button_plus = QPushButton(self.frame)
        self.button_plus.setGeometry(QRect(253, 58, 75, 53))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_plus.sizePolicy().hasHeightForWidth())
        self.button_plus.setSizePolicy(sizePolicy)
        self.button_plus.setMinimumSize(QSize(24, 53))
        self.button_plus.setMaximumSize(QSize(16777215, 53))
        font = QFont()
        self.button_plus.setFont(font)
        self.button_plus.setObjectName("button_plus")
        self.button_4 = QPushButton(self.frame)
        self.button_4.setGeometry(QRect(10, 117, 75, 53))
        self.button_4.setMinimumSize(QSize(24, 53))
        self.button_4.setMaximumSize(QSize(16777215, 53))
        self.button_4.setObjectName("button_4")
        self.button_5 = QPushButton(self.frame)
        self.button_5.setGeometry(QRect(91, 117, 75, 53))
        self.button_5.setMinimumSize(QSize(24, 53))
        self.button_5.setMaximumSize(QSize(16777215, 53))
        self.button_5.setObjectName("button_5")
        self.button_6 = QPushButton(self.frame)
        self.button_6.setGeometry(QRect(172, 117, 75, 53))
        self.button_6.setMinimumSize(QSize(24, 53))
        self.button_6.setMaximumSize(QSize(16777215, 53))
        self.button_6.setObjectName("button_6")
        self.button_x = QPushButton(self.frame)
        self.button_x.setGeometry(QRect(253, 122, 75, 53))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_x.sizePolicy().hasHeightForWidth())
        self.button_x.setSizePolicy(sizePolicy)
        self.button_x.setMinimumSize(QSize(24, 53))
        self.button_x.setMaximumSize(QSize(16777215, 42))
        font = QFont()
        self.button_x.setFont(font)
        self.button_x.setObjectName("button_x")
        self.button_7 = QPushButton(self.frame)
        self.button_7.setGeometry(QRect(10, 176, 75, 53))
        self.button_7.setMinimumSize(QSize(24, 53))
        self.button_7.setMaximumSize(QSize(16777215, 53))
        self.button_7.setObjectName("button_7")
        self.button_8 = QPushButton(self.frame)
        self.button_8.setGeometry(QRect(91, 176, 75, 53))
        self.button_8.setMinimumSize(QSize(24, 53))
        self.button_8.setMaximumSize(QSize(16777215, 53))
        self.button_8.setObjectName("button_8")
        self.button_9 = QPushButton(self.frame)
        self.button_9.setGeometry(QRect(172, 176, 75, 53))
        self.button_9.setMinimumSize(QSize(24, 53))
        self.button_9.setMaximumSize(QSize(16777215, 53))
        self.button_9.setObjectName("button_9")
        self.button_minus = QPushButton(self.frame)
        self.button_minus.setGeometry(QRect(253, 181, 75, 53))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_minus.sizePolicy().hasHeightForWidth())
        self.button_minus.setSizePolicy(sizePolicy)
        self.button_minus.setMinimumSize(QSize(24, 53))
        self.button_minus.setMaximumSize(QSize(16777215, 42))
        font = QFont()
        self.button_minus.setFont(font)
        self.button_minus.setObjectName("button_minus")
        self.spot = QPushButton(self.frame)
        self.spot.setGeometry(QRect(10, 235, 75, 53))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spot.sizePolicy().hasHeightForWidth())
        self.spot.setSizePolicy(sizePolicy)
        self.spot.setMinimumSize(QSize(24, 53))
        self.spot.setMaximumSize(QSize(16777215, 53))
        font = QFont()
        self.spot.setFont(font)
        self.spot.setObjectName("spot")
        self.button_divide = QPushButton(self.frame)
        self.button_divide.setGeometry(QRect(91, 235, 75, 53))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_divide.sizePolicy().hasHeightForWidth())
        self.button_divide.setSizePolicy(sizePolicy)
        self.button_divide.setMinimumSize(QSize(24, 53))
        self.button_divide.setMaximumSize(QSize(16777215, 53))
        font = QFont()
        self.button_divide.setFont(font)
        self.button_divide.setObjectName("button_divide")
        self.button_0 = QPushButton(self.frame)
        self.button_0.setGeometry(QRect(172, 235, 75, 53))
        self.button_0.setMinimumSize(QSize(24, 53))
        self.button_0.setMaximumSize(QSize(16777215, 53))
        self.button_0.setObjectName("button_0")
        self.button_equals = QPushButton(self.frame)
        self.button_equals.setGeometry(QRect(253, 235, 75, 53))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_equals.sizePolicy().hasHeightForWidth())
        self.button_equals.setSizePolicy(sizePolicy)
        self.button_equals.setMinimumSize(QSize(24, 53))
        self.button_equals.setMaximumSize(QSize(16777215, 53))
        font = QFont()
        self.button_equals.setFont(font)
        self.button_equals.setObjectName("button_equals")
        self.clear = QPushButton(self.frame)
        self.clear.setGeometry(QRect(90, 290, 77, 53))
        self.clear.setMinimumSize(QSize(77, 53))
        self.clear.setMaximumSize(QSize(77, 53))
        self.clear.setObjectName("clear")
        self.back = QPushButton(self.frame)
        self.back.setGeometry(QRect(10, 290, 77, 53))
        self.back.setMinimumSize(QSize(77, 53))
        self.back.setMaximumSize(QSize(77, 53))
        self.back.setObjectName("back")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

#Buttons to the screen, using Lambda here to save time
        self.button_1.clicked.connect(lambda:self.insert_number('1'))

        self.button_2.clicked.connect(lambda:self.insert_number('2'))
        self.button_3.clicked.connect(lambda:self.insert_number('3'))
        self.button_4.clicked.connect(lambda:self.insert_number('4'))
        self.button_5.clicked.connect(lambda:self.insert_number('5'))
        self.button_6.clicked.connect(lambda:self.insert_number('6'))
        self.button_7.clicked.connect(lambda:self.insert_number('7'))
        self.button_8.clicked.connect(lambda:self.insert_number('8'))
        self.button_9.clicked.connect(lambda:self.insert_number('9'))
        self.button_0.clicked.connect(lambda:self.insert_number('0'))
        self.button_x.clicked.connect(lambda:self.insert_number(' * '))
        self.button_divide.clicked.connect(lambda:self.insert_number(' / '))
        self.button_plus.clicked.connect(lambda:self.insert_number(' + '))
        self.button_equals.clicked.connect(self.calculation)
        self.button_minus.clicked.connect(lambda:self.insert_number(' - '))
        self.clear.clicked.connect(lambda:self.display.clear())
        self.back.clicked.connect(lambda:self.display.backspace())
        self.spot.clicked.connect(lambda:self.insert_number('.'))

#Return pressed        
        self.display.returnPressed.connect(self.calculation)


#Make display uneditable + add placeholder text
        self.display.setReadOnly(True)
        self.display.setPlaceholderText("Press = after x(operator)y. ")


    def insert_number(self,value):
        self.display.setAlignment(Qt.AlignCenter)
        self.display.insert(value)

    
#Injecting numbers to the screen                  			
    def calculation(self):
        try:
            screen_value=str(self.display.text()).split(' ')
            value1=float(screen_value[0])
            operate=(screen_value[1])
            value2=(screen_value[2])
            result_is=self.finalize(value1,value2,operate)
            print (result_is)
            self.display.setText(str(result_is))	
        except Exception as e:
            self.display.setText("Something went wrong.")
            
#Doing the actual calculations
    def finalize(self, value1, value2, operate):
        try:
            value1=float(value1)
            value2=float(value2)
        
            if operate is '+':
                return value1 + value2                
            elif operate is '*':
                return value1 * value2
            elif operate is '-':
                return value1 - value2 
            elif operate is '/':
                return value1 / value2               
        except Exception as e:
            print ("Something went wrong.")
            
#Keypress events
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()    
        
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QCalculator"))
        self.button_1.setText(_translate("MainWindow", "1"))
        self.button_2.setText(_translate("MainWindow", "2"))
        self.button_3.setText(_translate("MainWindow", "3"))
        self.button_4.setText(_translate("MainWindow", "4"))
        self.button_5.setText(_translate("MainWindow", "5"))
        self.button_6.setText(_translate("MainWindow", "6"))
        self.button_x.setText(_translate("MainWindow", "x"))
        self.button_7.setText(_translate("MainWindow", "7"))
        self.button_8.setText(_translate("MainWindow", "8"))
        self.button_9.setText(_translate("MainWindow", "9"))
        self.button_minus.setText(_translate("MainWindow", "-"))
        self.spot.setText(_translate("MainWindow", "."))
        self.button_plus.setText(_translate("MainWindow", "+"))
        self.button_divide.setText(_translate("MainWindow", "/"))
        self.button_0.setText(_translate("MainWindow", "0"))
        self.button_equals.setText(_translate("MainWindow", "="))
        self.clear.setText(_translate("MainWindow", "C"))
        self.back.setText(_translate("MainWindow", "Back"))
 
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def keyPressEvent(self, ev):
        #print(ev.text())
        if ev.key() == Qt.Key_1:
            print ("key 1")
            self.ui.button_1.click()
            
        if ev.key() == Qt.Key_2:
            print ("key 2")
            self.ui.button_2.click()
            
        if ev.key() == Qt.Key_3:
            print ("key 3")
            self.ui.button_3.click()
            
        if ev.key() == Qt.Key_4:
            print ("key 4")
            self.ui.button_4.click()
       
        if ev.key() == Qt.Key_5:
            print ("key 5")
            self.ui.button_5.click()
        
        if ev.key() == Qt.Key_6:
            print ("key 6")
            self.ui.button_6.click()
        
        if ev.key() == Qt.Key_7:
            print ("key 7")
            self.ui.button_7.click()
            
        if ev.key() == Qt.Key_8:
            print ("key 8")
            self.ui.button_8.click()
            
        if ev.key() == Qt.Key_9:
            print ("key 9")
            self.ui.button_9.click()
       
        if ev.key() == Qt.Key_0:
            print ("key 0")
            self.ui.button_0.click()
        
        if ev.key() == Qt.Key_Plus:
            print ("key +")
            self.ui.button_plus.click()
        
        if ev.key() == Qt.Key_Minus:
            print ("key -")
            self.ui.button_minus.click()
            
        if ev.key() == Qt.Key_Escape:
            print ("Clear")
            self.ui.clear.click()
        
        if ev.key() == Qt.Key_Comma:
            print (".")
            self.ui.spot.click()
        
        if ev.key() == Qt.Key_Slash:
            print ("/")
            self.ui.button_divide.click()
            
        if ev.key() == Qt.Key_Asterisk:
            print ("*")
            self.ui.button_x.click()
            
        if ev.key() == Qt.Key_Space:
            print ("Back")
            self.ui.back.click()                                                          
                               
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Window()
    
    MainWindow.show()
    sys.exit(app.exec_())
