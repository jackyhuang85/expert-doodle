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

    def __init__(self, deviceIndex, output):
        QThread.__init__(self)
        self.output = output
        self.deviceIndex = deviceIndex
        self.device = cv2.VideoCapture(self.deviceIndex)
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def run(self):
        if self.device.isOpened():
            try:
                while True:
                    _, frame = self.device.read()

                    # convert from BGR to RGB
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)

                    # convert to QImage
                    if self.output.not_in_use:
                        self.output.not_in_use = False
                        self.output.data = frame
                        self.output.not_in_use = True

            finally:
                self.device.release()

    def destroyed(self, QObject=None):
        self.device.release()


class FrameThread(QThread):
    input_frame = None
    _filter_enable = False
    _img_lab = None
    _filter = None
    _rate = 0
    _strength = 0
    output_frame = None
    WIDTH = 1280
    HEIGHT = 720
    CHANNEL = 3

    def __init__(self, img_lab, i_frame):
        QThread.__init__(self)
        self._img_lab = img_lab
        self.input_frame = i_frame

    def run(self):
        try:
            while True:
                if (self.input_frame.data is not None) and (self.input_frame.not_in_use):
                    self.input_frame.not_in_use = False
                    if self._filter_enable:
                        kernel = (self._strength/10+5, self._strength/20+5)
                        sigma = self._strength/10+5
                        rate = self._rate/50+1
                        contrast = (self._rate+10)/50+1
                        brightness = self._strength
                        self.output_frame = self._filter(
                            self.input_frame.data,
                            kernel=kernel,
                            sigma=sigma,
                            rate=rate,
                            contrast=contrast,
                            brightness=brightness
                        ).astype('uint8')

                        image = self.output_frame
                        image = Image.fromarray(image)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        image = ImageQt(image)
                        pixmap = QPixmap.fromImage(image)
                        pixmap = pixmap.scaled(
                            640, 480, QtCore.Qt.KeepAspectRatio)
                        self._img_lab.setPixmap(pixmap)
                        del image
                        del self.input_frame.data

                    else:
                        # frame = self.input_frame.data
                        # image = QImage(self.input_frame.data,
                        #                self.WIDTH,
                        #                self.HEIGHT,
                        #                QImage.Format_RGB888)
                        self.output_frame = self.input_frame.data
                        image = Image.fromarray(self.output_frame)
                        image = ImageQt(image)
                        pixmap = QPixmap.fromImage(image)
                        pixmap = pixmap.scaled(
                            640, 480, QtCore.Qt.KeepAspectRatio)
                        self._img_lab.setPixmap(pixmap)
                        del image
                        del self.input_frame.data
                    self.input_frame.not_in_use = True
        finally:
            pass

    def apply_filter(self, to_apply):
        if to_apply is not None:
            self._filter_enable = True
            self._filter = to_apply
        else:
            self._filter_enable = False
            self._filter = None

    def change_filter_rate(self, rate):
        self._rate = rate

    def change_filter_strength(self, strength):
        self._strength = strength

    def save_frame(self, path=None):
        if path is None:
            name = 'img-'+str(int(time.time()))+'.png'
            path = os.path.join('../data', name)

        image = Image.fromarray(self.output_frame)
        image.save(path)
        return path
