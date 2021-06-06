from random import randint
from PyQt5.QtWidgets import QMessageBox

from .field import Field
from .cells import SnakeCell 
from .cells import MaxTimeFruitCell, MinTimeFruitCell
from .cells import AppleCell, LemonCell, PlumCell, DeathFruitCell
from .cells import DeathWallCell, TeleportWallCell, MirrorWallCell
from .snake import Snake
from .snakewindow import SnakeWindow


class Game:
    def __init__(self, width=16, height=16):
        self.field = Field(width, height)
        self.snake = Snake((1,1), 1, 'right')
        self.is_paused = True
        self.is_dead = False
        self.score = 0
        self.init_level()
        self.window = SnakeWindow(self)
        self.DeathFruitCellCounter = 0
        self.death_type = ''
        return

    def init_level(self):
        self.field.set_cell(1, 1, SnakeCell(time_to_live=1))

        for x in range(self.field.width - 2):
            self.field.set_cell(x + 1, 0, self.choose_cell(x + 1, 0))
            self.field.set_cell(x + 1, self.field.height - 1, 
                self.choose_cell(x + 1, self.field.height - 1))

        for y in range(self.field.height - 2):
            self.field.set_cell(0, y + 1, self.choose_cell(0, y + 1))
            self.field.set_cell(self.field.width - 1, y + 1, 
                self.choose_cell(self.field.width - 1, y + 1))

        self.field.set_cell(0, 0, DeathWallCell())
        self.field.set_cell(0, self.field.height - 1, 
                            DeathWallCell())
        self.field.set_cell(self.field.width - 1, 0,
                            DeathWallCell())
        self.field.set_cell(self.field.width - 1, self.field.height - 1,
                            DeathWallCell())
        self.spawn_food()
        self.spawn_food()
        self.spawn_death_food()
        self.spawn_max_time_food()
        self.spawn_min_time_food()
        return

    def choose_cell(self, x, y):
        cell = None
        if x == self.field.width - 1:
            cell = self.field.get_cell(0, y)

        elif y == self.field.height - 1:
            cell = self.field.get_cell(x, 0)            

        cell_type = randint(0, 2)

        if (cell is not None and 
            cell.type == 'TeleportWallCell' or
            cell_type == 0):
            if x == 0:
                return TeleportWallCell(self.field.width - 2, y)

            elif x == self.field.width - 1:
                return TeleportWallCell(1, y)

            elif y == 0:
                return TeleportWallCell(x, self.field.height - 2)           

            elif y == self.field.height - 1:
                return TeleportWallCell(x, 1) 

        elif cell_type == 1:
            return DeathWallCell()

        elif cell_type == 2:
            return MirrorWallCell()


    def spawn_food(self):
        x, y = self.field.get_random_empty_cell()
        food_type = randint(0, 2);

        if food_type == 0:
            self.field.set_cell(x, y, AppleCell())

        elif food_type == 1:
            self.field.set_cell(x, y, LemonCell())

        elif food_type == 2:
            self.field.set_cell(x, y, PlumCell())

        return

    def spawn_death_food(self):
        x, y = self.field.get_random_empty_cell()
        self.field.set_cell(x, y, DeathFruitCell())
        return

    def spawn_max_time_food(self):
        x, y = x, y = self.field.get_random_empty_cell()
        self.field.set_cell(x, y, MaxTimeFruitCell())
        return

    def spawn_min_time_food(self):
        x, y = x, y = self.field.get_random_empty_cell()
        self.field.set_cell(x, y, MinTimeFruitCell())
        return

    def pause(self):
        self.is_paused = not self.is_paused
        return

    def turn(self, side):
        self.snake.turn(self, side)
        return

    def choose_string(self):
        if self.death_type == 'sc':
            return 'Кажется, наступил такой голод, что ты каннибалист!..'

        elif self.death_type == 'dfc':
            return 'Щас бы протухшую еду есть!..'

        elif self.death_type == 'dwc':
            return 'Наверное, так сложно стену увидеть!..'

    def update(self):
        if self.is_paused or self.is_dead:
            return

        self.snake.update(game=self)
        
        if self.is_dead:
            game_over_info = QMessageBox.warning(self.window,
                'Да как так-то а?!', 
                self.choose_string())
            self.reset()
            return

        self.field.update(game=self)
        x, y = self.snake.head
        self.field.set_cell(x, y, 
                            SnakeCell(time_to_live=self.snake.len))
        return

    def reset(self):
        self.field.clear()
        self.snake = Snake((1,1), 1, 'right')
        self.is_paused = True
        self.is_dead = False
        self.score = 0
        self.init_level()
        self.DeathFruitCellCounter = 0
        self.death_type = ''
        self.window.board.UPDATE_INTERVAL = 200
        self.window.board.timer.start(
                self.window.board.UPDATE_INTERVAL,
                self.window.board)
