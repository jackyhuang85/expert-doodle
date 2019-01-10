import sys
import platform
from PyQt5.QtWidgets import QApplication
from views import MainWindow

def detect_os_platform():
    return platform.system()

os = detect_os_platform()
app = QApplication(sys.argv)
main_window = MainWindow(platform=os)
main_window.show()
sys.exit(app.exec_())
