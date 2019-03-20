# always seem to need this
import sys

# This gets the Qt stuff
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QBasicTimer

# This is our window from QtCreator
import mainwindow_auto

# PinOut settings
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import os
camera = PiCamera()
GPIO.setmode(GPIO.BCM)

step_delay = 500
steps_per_rotation_for_motor = 18

dir_r = 26
step_r = 19
enable_r = 13

ms1 = 17
ms2 = 27
ms3 = 22

GPIO.cleanup()

GPIO.setup(dir_r, GPIO.OUT)
GPIO.setup(step_r, GPIO.OUT)
GPIO.setup(enable_r, GPIO.OUT)

GPIO.setup(ms1, GPIO.OUT)
GPIO.setup(ms2, GPIO.OUT)
GPIO.setup(ms3, GPIO.OUT)

# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
 # access variables inside of the UI's file

 ### functions for the buttons to call

 #Function to take pictures and rotate the step_motor
 def pressedTakeButton(self):
     #Just a feedback that the button has just been pressed
     print ("Pressed Take!")
     for n in range(1, 210):
         GPIO.output(ms1, 1)
         GPIO.output(ms2, 1)
         GPIO.output(ms3, 1)

         GPIO.output(enable_r, 0)
         time.sleep(0.0001)
         GPIO.output(dir_r, 0)

         #One only step for take a picture
         for m in range(0, steps_per_rotation_for_motor):
             GPIO.output(step_r, 0)
             time.sleep(0.0005)
             GPIO.output(step_r, 1)
             time.sleep(0.0005)

         GPIO.output(enable_r, 1)

         #Taking a picture
         dirpath = os.getcwd()
         camera.start_preview()
         time.sleep(1)
         camera.capture(dirpath + '/image_%s.jpg' %n)
         camera.stop_preview()

         time.sleep(0.7)

 def pressedSendButton(self):
     #Just a feedback that the button has just been pressed
     print ("Pressed Send!")
     time.sleep(2)
     os.system('~/Dropbox-Uploader/dropbox_uploader.sh upload *.jpg /Apps/PythonUploader')

 def pressedTestButton(self):
     print("Pressed Test")
     if self.timer.isActive():
         self.timer.stop()
         self.btnTest.setText('Start')
     else:
         self.timer.start(100, self)
         self.btnTest.setText('Stop')

 def timerEvent(self, event):
     if self.step >= 100:
         self.timer.stop()
         self.btnTest.setText('Finished')
         return
     self.step = self.step + 1
     self.progressBar.setValue(self.step)

 def __init__(self):
     super(self.__class__, self).__init__()
     self.setupUi(self) # gets defined in the UI file

     ### Hooks to for buttons
     self.btnTAKE.clicked.connect(lambda: self.pressedTakeButton())
     self.btnSEND.clicked.connect(lambda: self.pressedSendButton())
     self.btnTest.clicked.connect(lambda: self.pressedTestButton())

     self.progressBar = QProgressBar(self)
     self.progressBar.setGeometry(320,400,200,25)

     self.timer = QBasicTimer()
     self.step = 0;

# I feel better having one of these
def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())

# python bit to figure how who started This
if __name__ == "__main__":
 main()
