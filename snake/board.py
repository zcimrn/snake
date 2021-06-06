from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter

from snake.renderer import Renderer


class Board(QFrame):
    statusUpdated = pyqtSignal(str)

    def __init__(self, game, parent):
        self.UPDATE_INTERVAL = 200
        super().__init__(parent)
        self.game = game
        self.timer = QBasicTimer()
        self.timer.start(self.UPDATE_INTERVAL, self)
        self.setFocusPolicy(Qt.StrongFocus)
        return

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.game.update()
            self.update()
            self.update_status()

        else:
            super().timerEvent(event)

        return

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setViewport(self.contentsRect())
        renderer = Renderer(painter)
        renderer.render(self.game.field)
        return

    def get_turn(self):
        return self.game.snake.direction

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Space:
            self.game.pause()
            return

        if self.game.is_paused:
            return

        if key == Qt.Key_Up:
            self.game.turn('up')

        elif key == Qt.Key_Down:
            self.game.turn('down')

        elif key == Qt.Key_Left:
            self.game.turn('left')

        elif key == Qt.Key_Right:
            self.game.turn('right')

        else:
            super().keyPressEvent(event)

        return

    def update_status(self):
        status = ('Score: {0}'.format(self.game.score) + '    ' + 
                  'Size: {0}'.format(self.game.snake.len))

        if self.game.is_paused:
            status = 'PAUSED'

        elif self.game.is_dead:
            status = 'GAME OVER. ' + status

        self.statusUpdated.emit(status)
        return