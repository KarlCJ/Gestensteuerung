import sys
from PyQt5.QtWidgets import QApplication, QWidget
from camera_widget import CameraWidget
from constants import WIDTH, HEIGHT

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setWindowTitle('Python Camera UI')
        self.camera_widget = CameraWidget(self)
        self.camera_widget.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraWidget(peer_ip='tcp://localhost:5556')
    window.show()
    sys.exit(app.exec_())
