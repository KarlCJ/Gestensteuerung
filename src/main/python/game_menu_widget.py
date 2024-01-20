from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QHBoxLayout, QLabel, QListWidgetItem, \
    QListWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

from src.main.python.gamelabel import GameLabel
from src.main.python.round_button import RoundButton


class GamesMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setup_ui()

    def setup_ui(self):
        self.setLayout(QVBoxLayout())
        self.setWindowOpacity(0.8)  # Halbtransparent

        # Verwende QListWidget für die Spieleliste
        self.gamesList = QListWidget()
        self.gamesList.setStyleSheet(
            "border: none; background-color: transparent;")  # Kein Rahmen, transparenter Hintergrund
        self.layout().addWidget(self.gamesList)

        # Spiele hinzufügen
        self.add_game("TicTacToe", self.on_tic_tac_toe_clicked, "../GUI/images/play-svgrepo-com.png")
        self.add_game("Schere Stein Papier", self.on_tic_tac_toe_clicked, "../GUI/images/play-svgrepo-com.png")

        self.hide()  # Anfangs versteckt

    def add_game(self, game_name, callback, imgpath):
        item = QListWidgetItem()
        game_label = GameLabel(game_name, callback, imgpath, self)

        # Füge einen minimalen Abstand hinzu
        item_size = game_label.sizeHint()
        item_size.setHeight(item_size.height() + 10)  # 10px Abstand hinzufügen
        item.setSizeHint(item_size)

        self.gamesList.addItem(item)
        self.gamesList.setItemWidget(item, game_label)

    def on_tic_tac_toe_clicked(self):
        print("TicTacToe ausgewählt")

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
