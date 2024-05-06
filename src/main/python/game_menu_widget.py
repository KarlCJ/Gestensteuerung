from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QHBoxLayout, QLabel, QListWidgetItem, \
    QListWidget, QApplication
from PyQt5.QtCore import Qt

from src.main.python.constants import WIDTH, HEIGHT
from src.main.python.tictactoe_widget import TicTacToeWidget
from gamelabel import GameLabel



class GamesMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setup_ui()


    def setup_ui(self):
        layout= QVBoxLayout()
        layout.setContentsMargins(WIDTH//3, 100, 100, 100)
        self.setLayout(layout)
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
        self.ticTacToeWidget = TicTacToeWidget()
        self.layout().addWidget(self.ticTacToeWidget)
        self.ticTacToeWidget.show()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()



