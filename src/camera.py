'''
[camera.py]
This file contains classes for handling camera

'''
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from PIL.ImageQt import ImageQt
from PIL import Image
from filters import *
import cv2
import time
import os


class CameraThread(QThread):
    imgLab = None
    device = None

    def __init__(self, deviceIndex, output, lock):
        QThread.__init__(self)
        self.output = output
        self.deviceIndex = deviceIndex
        self.device = cv2.VideoCapture(self.deviceIndex)
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.lock = lock

    def run(self):
        if self.device.isOpened():
            try:
                while True:
                    _, frame = self.device.read()
                    # convert from BGR to RGB
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                    # frame = blur(frame)
                    # frame = gray_scale(frame).astype('uint8')
                    # convert to QImage
<<<<<<< HEAD
                    if self.output.not_in_use:
                        self.output.not_in_use = False
                        self.output.data = frame
                        # import pdb
                        # pdb.set_trace()
                        self.output.not_in_use = True

=======
                    self.lock.acquire()
                    self.output.data = frame.data
                    self.lock.release()
                    
>>>>>>> Add threading.Lock
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


class FrameThread(QThread):
    input_frame = None
    _filter_enable = False
    _img_lab = None

    WIDTH = 1280
    HEIGHT = 720
    CHANNEL = 3
<<<<<<< HEAD

    def __init__(self, img_lab, i_frame):
        QThread.__init__(self)
        self._img_lab = img_lab
        self.input_frame = i_frame

=======
    
    def __init__(self, img_lab, i_frame, lock):
        QThread.__init__(self)
        self._img_lab = img_lab
        self.input_frame = i_frame
        self.lock = lock
    
>>>>>>> Add threading.Lock
    def run(self):
        try:
            while True:
                # print(self.input_frame)
<<<<<<< HEAD
                if (self.input_frame.data is not None) and (self.input_frame.not_in_use):
                    self.input_frame.not_in_use = False
=======
                self.lock.acquire()
                if (self.input_frame.data is not None):
>>>>>>> Add threading.Lock
                    if self._filter_enable:
                        pass
                    else:
                        # frame = self.input_frame.data
                        # image = QImage(self.input_frame.data,
                        #                self.WIDTH,
                        #                self.HEIGHT,
                        #                QImage.Format_RGB888)
                        image = Image.fromarray(self.input_frame.data)
                        image = ImageQt(image)
                        pixmap = QPixmap.fromImage(image)
                        pixmap = pixmap.scaled(
                            640, 480, QtCore.Qt.KeepAspectRatio)
                        self._img_lab.setPixmap(pixmap)
                        del image
                        del self.input_frame.data
                
                self.lock.release()

        finally:
            pass
