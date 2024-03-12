from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize

from round_button import RoundButton


class GameLabel(QFrame):
    def __init__(self, game_name, callback, imgpath, parent=None):
        super().__init__(parent)
        self.init_ui(game_name, callback, imgpath)

    def init_ui(self, game_name, callback, imgpath):
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.setFixedSize(len(game_name)*6+100, 60)
        self.setStyleSheet("background-color: rgba(200, 200, 200, 128); border-radius: 15px;")

        label = QLabel(game_name)
        label.setStyleSheet("background-color: transparent; font-size: 18px;")
        self.layout.addWidget(label)

        button = RoundButton(self, callback, imgpath)
        button.setFixedSize(QSize(40, 40))
        self.layout.addWidget(button,Qt.AlignCenter)

