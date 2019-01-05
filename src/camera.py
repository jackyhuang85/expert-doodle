'''
[camera.py]
This file contains classes for handling camera

'''
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from filters import *
import cv2
import time
import os


class FrameThread(QThread):
    imgLab = None
    device = None

    def __init__(self, deviceIndex, imgLab):
        QThread.__init__(self)
        self.imgLab = imgLab
        self.deviceIndex = deviceIndex
        self.device = cv2.VideoCapture(self.deviceIndex)
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def run(self):
        if self.device.isOpened():
            try:
                while True:
                    ret, frame = self.device.read()
                    height, width, bytesPerComponent = frame.shape
                    bytesPerLine = bytesPerComponent * width
                    # convert from BGR to RGB
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)

                    self.frame = edge_detect(frame, thin=False).astype('uint8')

                    # Extend to 3 channel if only 1
                    if len(self.frame.shape) == 2:
                        self.frame = np.repeat(
                            self.frame[:, :, np.newaxis], 3, axis=2)

                    # convert to QImage
                    image = QImage(self.frame.data, width, height,
                                   bytesPerLine, QImage.Format_RGB888)

                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                    self.imgLab.setPixmap(pixmap)
            finally:
                self.device.release()

    def destroyed(self, QObject=None):
        self.device.release()

    def save_frame(self, path=None):
        if path is None:
            name = 'img-'+str(int(time.time()))+'.png'
            path = os.path.join('../data', name)

        cv2.imwrite(path, self.frame)

        return path
