'''
[views.py]
This file contains classes that represent the appearance of the application.
It includes the config of layout, the appearance of widgets, 
and also assigns event-handler for each widget.

'''
from PyQt5.QtWidgets import (QMainWindow, QLabel, QHBoxLayout, 
                             QWidget, QGroupBox, QVBoxLayout,
                             QPushButton, QScrollArea, QGridLayout)
from camera import FrameThread
from controller import MainViewController

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
        self.controller = MainViewController(self)
        self.init_ui()
        self.controller.start()

    def init_ui(self):
        '''
        Initiate UI components in MainWindow
        '''
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
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('Main Window')

    def set_menubar(self):
        menubar = self.menuBar()
        _ = menubar.addMenu('File')
        menubar.setNativeMenuBar(False)

    def on_clicked_take_photo_button(self):
        print('clicked')




class FiltersBlock(QWidget):
    FILTER_NUM = 6
    filters_list = []
    def __init__(self, parent):
        QWidget.__init__(self)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.filters_grid_layout = QGridLayout()
        for i in range(self.FILTER_NUM):
            bt = QPushButton('%d' % i)
            bt.resize(50, 50)
            self.filters_list.append(bt)
            self.filters_grid_layout.addWidget(bt, 0, i)

        self.setLayout(self.filters_grid_layout)
