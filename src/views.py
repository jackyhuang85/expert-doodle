'''
[views.py]
This file contains classes that represent the appearance of the application.
It includes the config of layout, the appearance of widgets, 
and also assigns event-handler for each widget.

'''
import os
from PyQt5.QtWidgets import (QMainWindow, QLabel, QHBoxLayout,
                             QWidget, QGroupBox, QVBoxLayout,
                             QPushButton, QScrollArea, QGridLayout,
                             QRadioButton, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from controller import MainViewController


class MainWindow(QMainWindow):
    '''
    MainWindow

    Arguments:
        None -- no argument needed
    '''
    controller = None

    def __init__(self):
        super().__init__()
        self.content_wid = QWidget(self)
        self.setCentralWidget(self.content_wid)
        self.controller = MainViewController(self)
        self.init_ui()
        self.controller.start()

    def init_ui(self):
        '''
        Initiate UI components in MainWindow
        '''
        # Meta
        self.set_window_size_title()

        # Main component
        self.create_camera_horizontal_layout()
        self.create_filters_horizontal_layout()

        # Set up menu bar
        self.set_menubar()

        # Set up main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.camera_horizontal_group_box)
        main_layout.addWidget(self.filter_horizontal_group_box)
        self.content_wid.setLayout(main_layout)

    def create_camera_horizontal_layout(self):
        '''
        Set up Camera Box-Layout (above)
        '''
        self.camera_horizontal_group_box = QGroupBox('Camera')
        layout = QHBoxLayout()

        # Left-side group box
        camera_operation_group_box = QGroupBox('Operation')
        camera_operation_layout = QVBoxLayout()

        start_button = QPushButton('Start/Stop')
        take_photo_button = QPushButton('Take a photo')
        take_photo_button.clicked.connect(self.on_clicked_take_photo_button)
        camera_operation_layout.addWidget(start_button)
        camera_operation_layout.addWidget(take_photo_button)
        camera_operation_group_box.setLayout(camera_operation_layout)

        # Camera frame
        camera_label = QLabel()
        camera_label.resize(600, 400)
        self.controller.bind_to_frame_thread(camera_label)
        # self.frame_thread = FrameThread(0, camera_label)

        # Right-side group box
        camera_filters_para_group_box = QGroupBox('Parameter')
        camera_filters_para_group_layout = QVBoxLayout()
        parameter_block = ParametersBlock(self)
        camera_filters_para_group_layout.addWidget(parameter_block)
        camera_filters_para_group_box.setLayout(
            camera_filters_para_group_layout)

        layout.addWidget(camera_operation_group_box)
        layout.addWidget(camera_label)
        layout.addWidget(camera_filters_para_group_box)

        self.camera_horizontal_group_box.setLayout(layout)

    def create_filters_horizontal_layout(self):
        '''
        Set up Filter Box-Layout (bottom)
        '''
        self.filter_horizontal_group_box = QGroupBox('Filters')
        layout = QHBoxLayout()

        filters_block = FiltersBlock(self)
        filters_block.setMinimumWidth(1500)
        scroll = QScrollArea()
        scroll.setWidget(filters_block)
        scroll.setWidgetResizable(True)
        scroll.setAutoFillBackground(True)

        layout.addWidget(scroll)

        self.filter_horizontal_group_box.setLayout(layout)

    def set_window_size_title(self):
        '''
        Meta config of MainWindow
        '''
        self.setGeometry(300, 300, 1440, 810)
        self.setWindowTitle('Main Window')

    def set_menubar(self):
        menubar = self.menuBar()
        _ = menubar.addMenu('File')
        menubar.setNativeMenuBar(False)

    def on_clicked_take_photo_button(self):
        path = self.controller.take_photo()
        #path = self.camera_thread.save_frame()
        print('Image is saved to %s' % path)


class FiltersBlock(QWidget):
    filters = {}

    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent
        self.controller = parent.controller
        self.init_ui()

    def init_ui(self):
        self.filters_grid_layout = QGridLayout()
        self.setLayout(self.filters_grid_layout)
        self.controller.load_filters(self.filters)

        filters_name = self.filters.keys()

        for i, name in enumerate(filters_name):
            print(name)
            if name == 'none':
                rbt = QRadioButton('None')
                rbt.setChecked(True)
                rbt.toggled.connect(
                    lambda checked, text=name, button=rbt: self.r_btn_state('None', button))

            else:
                rbt = QRadioButton('%s' % name.replace('_', ' '))
                rbt.toggled.connect(
                    lambda checked, text=name, button=rbt: self.r_btn_state(text, button))

            thumb = QLabel()
            thumb.resize(150, 150)
            thumb_img = QPixmap(os.path.join('../example/', ('%s.jpg' % name)))
            thumb_img = thumb_img.scaled(150, 150, QtCore.Qt.KeepAspectRatio)
            thumb.setPixmap(thumb_img)

            self.filters_grid_layout.addWidget(thumb, 0, i, 2, 1)
            self.filters_grid_layout.addWidget(
                rbt, 2, i, QtCore.Qt.AlignHCenter)

    def r_btn_state(self, btn_text, button):
        if button.isChecked():
            print(button.text())
            self.flag = btn_text
            self.controller.apply_filter(self.flag)


class ParametersBlock(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent
        self.controller = parent.controller
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.rate_slider = QSlider(QtCore.Qt.Horizontal)
        self.rate_slider.setRange(-49, 50)
        self.rate_slider.setValue(0)
        self.rate_slider.setTickPosition(QSlider.TicksBelow)
        self.rate_slider.setTickInterval(10)
        self.rate_slider.valueChanged.connect(self.rate_value_change)

        self.strength_slider = QSlider(QtCore.Qt.Horizontal)
        self.strength_slider.setRange(-49, 50)
        self.strength_slider.setValue(0)
        self.strength_slider.setTickPosition(QSlider.TicksBelow)
        self.strength_slider.setTickInterval(10)
        self.strength_slider.valueChanged.connect(self.strength_value_change)

        self.layout.addWidget(self.rate_slider)
        self.layout.addWidget(self.strength_slider)

    def rate_value_change(self, value):
        self.controller.change_filter_rate(value)

    def strength_value_change(self, value):
        self.controller.change_filter_strength(value)
