from random import randint

from .field import Field


class Snake:
    def __init__(self, head_position, start_length, direction):
        self.TURNS = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
        }
        self.head = head_position
        self.len = start_length
        self.direction = direction
        return

    def update(self, game):
        self.set_next_position()
        x, y = self.head
        cell = game.field.get_cell(x, y)

        if cell is not None and cell.type == 'SnakeCell':
            cell.on_bump(game)

        x, y = self.head
        cell = game.field.get_cell(x, y)

        if cell is not None and cell.type == 'MirrorWallCell':
            cell.on_bump(game)

        x, y = self.head
        cell = game.field.get_cell(x, y)

        if cell is not None and cell.type == 'MirrorWallCell':
            self.direction = self.invert_direction(self.direction)
            self.set_next_position()
            self.direction = self.invert_direction(self.direction)
            self.snake_plus_plus(game)
            return

        if cell is not None and cell.type == 'TeleportWallCell':
            cell.on_bump(game)

        x, y = self.head
        cell = game.field.get_cell(x, y)

        if cell is not None:
            cell.on_bump(game)
        return

    def snake_plus_plus(self, game):
        for x in range(game.field.width):
            for y in range(game.field.height):
                cell = game.field.get_cell(x, y)

                if cell is not None and cell.type == "SnakeCell":
                    game.field.cells[x][y].time_to_live += 1

        return

    def check_cell(self, game, x, y):
        cell = game.field.get_cell(x, y)
        head_cell = game.field.get_cell(self.head[0], self.head[1])

        if (cell is not None and 
            cell.type == "SnakeCell" and 
            (cell.time_to_live == self.len - 1 or
             cell.time_to_live == 1 and self.len == 2)):
            return True

        else:
            return False

    def choose_direction(self, game, x, y):
        if self.check_cell(game, x, y + 1):
            self.direction = 'up'

        elif self.check_cell(game, x, y - 1):
            self.direction = 'down'

        elif self.check_cell(game, x + 1, y):
            self.direction = 'left'

        elif self.check_cell(game, x - 1, y):
            self.direction = 'right'

        return

    def invert_direction(self, direction):
        if direction == 'up':
            return 'down'

        elif direction == 'down':
            return 'up'

        elif direction == 'left':
            return 'right'

        elif direction == 'right':
            return 'left'

    def turn_around(self, game):
        if self.len < 2:
            self.direction = self.invert_direction(self.direction)
            self.set_next_position()
            return
            
        tmp = []

        for x in range(game.field.width):
            for y in range(game.field.height):
                cell = game.field.get_cell(x, y)

                if (cell is not None and 
                    cell.type == 'SnakeCell'):
                    tmp.append((cell.time_to_live, x, y))

        tmp.sort()           
            
        for i in range(len(tmp)):
            x, y = tmp[i][1], tmp[i][2]
            game.field.cells[x][y].time_to_live = tmp[-1 - i][0]

        x, y = tmp[0][1], tmp[0][2]
        self.head = x, y
        self.choose_direction(game, x, y)
        return

    def turn(self, game, direction): 
        self.direction = direction
        return

    def set_next_position(self):
        x, y = self.TURNS[self.direction]
        self.head = self.head[0] + x, self.head[1] + y
        return