from sys import exit
from PyQt5.QtWidgets import QApplication

from snake.game import Game


if __name__ == '__main__':
    app = QApplication([])
    game = Game(16, 16)
    exit(app.exec_())