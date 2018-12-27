'''
[views.py]
This file contains classes that represent the appearance of the application.
It includes the config of layout, the appearance of widgets, 
and also assigns event-handler for each widget.

'''


import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, 
                             QLabel, QHBoxLayout, QWidget, QGroupBox, 
                             QVBoxLayout)
from camera import FrameThread

class MainWindow(QMainWindow):
    '''
    MainWindow

    Arguments:
        None -- no argument needed
    '''

    def __init__(self):
        super().__init__()
        self.content_wid = QWidget(self)
        self.setCentralWidget(self.content_wid)
        self.init_ui()
        self.frame_thread.start()

    def init_ui(self):
        self.set_window_size_title()

        self.create_camera_horizontal_layout()
        self.create_filters_horizontal_layout()
        # Set up menu bar
        self.set_menubar()

        # set up layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.camera_horizontal_group_box)
        main_layout.addWidget(self.filter_horizontal_group_box)
        self.content_wid.setLayout(main_layout)

    def create_camera_horizontal_layout(self):
        self.camera_horizontal_group_box = QGroupBox('Camera')
        layout = QHBoxLayout()
        camera_label = QLabel()
        camera_label.resize(600, 400)
        self.frame_thread = FrameThread(0, camera_label)
        layout.addWidget(camera_label)

        self.camera_horizontal_group_box.setLayout(layout)

    def create_filters_horizontal_layout(self):
        self.filter_horizontal_group_box = QGroupBox('Filters')


    def set_window_size_title(self):
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('Main Window')

    def set_menubar(self):
        menubar = self.menuBar()
        _ = menubar.addMenu('File')
        menubar.setNativeMenuBar(False)