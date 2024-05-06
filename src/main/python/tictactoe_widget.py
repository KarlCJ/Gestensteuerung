# TicTacToeWidget.py

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QApplication, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

from src.main.python.constants import WIDTH, HEIGHT, TICTACTOE_SIZE


class GameLabel(QFrame):
    def __init__(self, text, callback, parent=None):
        super().__init__(parent)
        self.text = text
        self.callback = callback
        self.initUI()

    def mousePressEvent(self, event):
        self.callback()


class TicTacToeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.currentPlayer = "X"
        self.winner = None
        self.initUI()

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.setFixedSize(TICTACTOE_SIZE,TICTACTOE_SIZE)
        self.setLayout(self.gridLayout)
        self.cells = {}
        self.setWindowTitle("TicTacToe")

        for row in range(3):
            for col in range(3):
                button = QPushButton(' ')
                button.setFixedSize(TICTACTOE_SIZE//3, TICTACTOE_SIZE//3)
                button.setFont(QFont('Arial', 24))
                button.setStyleSheet("background-color: rgba(255, 255, 255, 150)")
                self.gridLayout.addWidget(button, row, col)
                self.cells[(row, col)] = button
                button.clicked.connect(lambda _, r=row, c=col: self.cellClicked(r, c))

        self.overlayWidget = QWidget(self)
        self.overlayWidget.setFixedSize(TICTACTOE_SIZE, TICTACTOE_SIZE)
        self.overlayWidget.setStyleSheet("background-color: rgba(0, 0, 0, 150)")
        self.overlayLayout = QVBoxLayout(self.overlayWidget)
        self.overlayWidget.hide()

    def cellClicked(self, row, col):
        button = self.cells[(row, col)]
        if button.text() == ' ' and not self.winner:
            button.setText(self.currentPlayer)
            self.checkWinner()
            self.currentPlayer = "O" if self.currentPlayer == "X" else "X"

    def checkWinner(self):
        winning_positions = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
        ]
        for positions in winning_positions:
            if all(self.cells[pos].text() == self.currentPlayer for pos in positions):
                self.winner = self.currentPlayer
                self.showOverlay(self.winner + " hat gewonnen!")
                return
        if all(self.cells[pos].text() != ' ' for pos in self.cells):
            self.showOverlay("Unentschieden!")

    def showOverlay(self, text):
        self.overlayWidget.show()
        self.overlayWidget.move((self.width() - self.overlayWidget.width()) // 2,
                                (self.height() - self.overlayWidget.height()) // 2)
        for i in reversed(range(self.overlayLayout.count())):
            self.overlayLayout.itemAt(i).widget().deleteLater()

        winnerLabel = QLabel(text)
        winnerLabel.setFont(QFont('Arial', 20))
        winnerLabel.setFixedHeight(100)
        winnerLabel.setStyleSheet("color: white; border-radius: 15px;")
        winnerLabel.setAlignment(Qt.AlignCenter)
        self.overlayLayout.addWidget(winnerLabel)

        replayButton = QPushButton("Nochmal spielen")
        replayButton.setFont(QFont('Arial', 20))
        replayButton.setFixedHeight(50)
        replayButton.setStyleSheet("color: white; border-radius: 15px;")
        replayButton.clicked.connect(self.resetGame)
        self.overlayLayout.addWidget(replayButton)

    def resetGame(self):
        for pos, button in self.cells.items():
            button.setText(' ')
        self.currentPlayer = "X"
        self.winner = None
        self.overlayWidget.hide()



if __name__ == "__main__":
    app = QApplication([])
    ticTacToe = TicTacToeWidget()
    ticTacToe.show()
    app.exec_()
