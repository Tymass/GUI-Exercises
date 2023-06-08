import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class CameraWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CameraWindow, self).__init__(parent)
        self.capture = cv2.VideoCapture(0)

        # Check if camera opened successfully
        if not self.capture.isOpened():
            print("Error opening video camera")
        else:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(1)

            self.image_label = QtWidgets.QLabel()
            self.setCentralWidget(self.image_label)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0],
                                 frame.strides[0], QtGui.QImage.Format_RGB888)
            self.image_label.setPixmap(QtGui.QPixmap.fromImage(image))
