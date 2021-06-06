class Cell:
    def __init__(self):
        self.color = ''
        self.type = ''
        return

    def update(self, game):
        return self

    def on_bump(self, game):
        return


class SnakeCell(Cell):
    def __init__(self, time_to_live):
        self.color = '020'
        self.type = 'SnakeCell'
        self.time_to_live = time_to_live
        return

    def update(self, game):
        if self.time_to_live == 1:
            return None

        return SnakeCell(self.time_to_live - 1)

    def on_bump(self, game):
        if (self.time_to_live == 1 and game.snake.len == 2 or
            self.time_to_live == game.snake.len - 1):
            game.snake.turn_around(game)
            game.snake.set_next_position()

        elif self.time_to_live > 1:
            game.is_dead = True
            game.death_type = 'sc'

        return


class AppleCell(Cell):
    def __init__(self):
        self.color = '200'
        self.type = 'AppleCell'
        self.is_eaten = False
        return

    def on_bump(self, game):
        self.is_eaten = True
        game.snake.len += 1
        game.score += 1

        for x in range(game.field.width):
            for y in range(game.field.height):
                cell = game.field.get_cell(x, y)

                if (cell is not None and 
                    cell.type == 'SnakeCell' and
                    cell.time_to_live != 1):
                    cell.time_to_live += 1

        game.spawn_food()
        game.DeathFruitCellCounter += 1
        return

    def update(self, game):
        if self.is_eaten:
            return None

        else:
            return self


class LemonCell(Cell):
    def __init__(self):
        self.color = '220'
        self.type = 'LemonCell'
        self.is_eaten = False
        return

    def on_bump(self, game):
        self.is_eaten = True
    
        if game.snake.len > 1:
            game.snake.len -= 1

        game.score += 1

        for x in range(game.field.width):
            for y in range(game.field.height):
                cell = game.field.get_cell(x, y)

                if (cell is not None and 
                    cell.type == 'SnakeCell' and
                    cell.time_to_live != 1):
                    cell.time_to_live -= 1

        game.spawn_food()
        game.DeathFruitCellCounter += 1
        return

    def update(self, game):
        if self.is_eaten:
            return None

        else:
            return self


class PlumCell(Cell):
    def __init__(self):
        self.color = '002'
        self.type = "PlumCell"
        self.is_eaten = False
        return

    def on_bump(self, game):
        self.is_eaten = True
        game.snake.len += 2
        game.score += 1

        for x in range(game.field.width):
            for y in range(game.field.height):
                cell = game.field.get_cell(x, y)

                if (cell is not None and 
                    cell.type == 'SnakeCell' and
                    cell.time_to_live != 1):
                    cell.time_to_live += 2

        game.spawn_food()
        game.DeathFruitCellCounter += 1
        return

    def update(self, game):
        if self.is_eaten:
            return None

        else:
            return self


class DeathFruitCell(Cell):
    def __init__(self):
        self.color = '011'
        self.type = 'DeathFruitCell' 
        return

    def on_bump(self, game):
        game.is_dead = True
        game.death_type = 'dfc'
        return


class MaxTimeFruitCell(Cell):
    def __init__(self):
        self.color = '022'
        self.type = 'TimeFruitCell'
        self.is_eaten = False
        return

    def on_bump(self, game):
        self.is_eaten = True
        game.window.board.UPDATE_INTERVAL += 50
        game.window.board.timer.start(
            game.window.board.UPDATE_INTERVAL,
            game.window.board)
        game.score += 1
        game.spawn_max_time_food()
        return

    def update(self, game):
        if self.is_eaten:
            return None

        else:
            return self


class MinTimeFruitCell(Cell):
    def __init__(self):
        self.color = '202'
        self.type = 'TimeFruitCell'
        self.is_eaten = False
        return

    def on_bump(self, game):
        self.is_eaten = True

        if game.window.board.UPDATE_INTERVAL > 50:
            game.window.board.UPDATE_INTERVAL -= 50

        game.window.board.timer.start(
            game.window.board.UPDATE_INTERVAL,
            game.window.board)
        game.score += 1
        game.spawn_min_time_food()
        return

    def update(self, game):
        if self.is_eaten:
            return None

        else:
            return self


class DeathWallCell(Cell):
    def __init__(self):
        self.color = '000'
        self.type = 'DeathWallCell'
        return

    def on_bump(self, game):
        game.is_dead = True
        game.death_type = 'dwc'
        return


class TeleportWallCell(Cell):
    def __init__(self, x, y):
        self.color = '102'
        self.type = 'TeleportWallCell'
        self.x = x
        self.y = y
        return

    def on_bump(self, game):
        game.snake.head = self.x, self.y
        return


class MirrorWallCell(Cell):
    def __init__(self):
        self.color = '111'
        self.type = 'MirrorWallCell'
        return

    def on_bump(self, game):
        game.snake.turn_around(game)
        game.snake.set_next_position()
        return