from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDesktopWidget

from .board import Board

class SnakeWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.board = Board(game, self)
        self.status_bar = self.statusBar()
        self.initUI(game.field)
        return

    def initUI(self, field):
        self.setCentralWidget(self.board)
        self.board.statusUpdated[str].connect(
            self.status_bar.showMessage)
        self.setWindowTitle('Snake    updated by PomodorCat')
        screen = QDesktopWidget().screenGeometry()
        square_size = min(screen.width() // field.width,
                          (screen.height() - 128) // field.height)      
        self.resize(square_size * field.width, 
                    square_size * field.height)
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, 
                  (screen.height() - size.height()) / 2)
        self.show()
        return