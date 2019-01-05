from camera import FrameThread

class MainViewController():
    frame_thread = None
    def __init__(self, window):
        self.window_view = window
        self.main_widget = window.centralWidget()


    def start(self, debug=False):
        self.frame_thread.start()


    def bind_to_frame_thread(self, frame_label):
        self.frame_thread = FrameThread(0, frame_label)
