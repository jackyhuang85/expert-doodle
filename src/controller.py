from camera import CameraThread, FrameThread
import filters


class MainViewController():
    camera_thread = None
    frame_thread = None
    filters_list = []

    def __init__(self, window):
        self.window_view = window
        self.main_widget = window.centralWidget()

    def start(self, debug=False):
        self.camera_thread.start()
        self.frame_thread.start()

    def bind_to_frame_thread(self, frame_label):
        io_frame = self.FrameIO()
        self.frame_thread = FrameThread(frame_label, io_frame)
        self.camera_thread = CameraThread(0, io_frame)

    def load_filters(self, filters_list):
        '''
        Binding for FiltersBlock class
        Arguments:
            filters_list {dict} -- [description]
        '''
        filters_list['none'] = None
        filters_list['gray_scale'] = filters.gray_scale
        filters_list['blur'] = filters.blur
        filters_list['sharpen'] = filters.sharpen
        filters_list['invert'] = filters.invert
        filters_list['enhance'] = filters.enhance
        filters_list['power'] = filters.power
        filters_list['sobel'] = filters.sobel
        filters_list['edge_detect'] = filters.edge_detect
        self.filters_list = filters_list

    def apply_filter(self, filter_name):
        if filter_name == 'None':
            filter_selected = None
            self.frame_thread.apply_filter(filter_selected)
        else:
            filter_selected = self.filters_list[filter_name]
            self.frame_thread.apply_filter(filter_selected)

    def change_filter_rate(self, rate):
        self.frame_thread.change_filter_rate(rate)

    def change_filter_strength(self, strength):
        self.frame_thread.change_filter_strength(strength)

    def take_photo(self, path=None):
        return self.frame_thread.save_frame(path=path)

    class FrameIO():
        data = None
        not_in_use = True
