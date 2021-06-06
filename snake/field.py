from random import randint


class Field:
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.cells = [[None for y in range(height)]
                       for x in range(width)]
        return
        
    def is_empty(self, x, y):
        return self.cells[x][y] is None

    def get_random_empty_cell(self):
        tmp = []

        for x in range(self.width):
            for y in range(self.height):
                if self.is_empty(x, y):
                    tmp.append((x, y))

        return tmp[randint(0, len(tmp) - 1)]   

    def set_cell(self, x, y, cell):
        self.cells[x][y] = cell
        return

    def get_cell(self, x, y):
        return self.cells[x][y]

    def update(self, game):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(x, y)

                if (cell is not None and
                    cell.type == 'SnakeCell'):
                        self.set_cell(x, y, cell.update(game))

        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(x, y)

                if (cell is not None and
                    cell.type != 'SnakeCell' and
                    cell.type != 'DeathFruitCell'):
                    self.set_cell(x, y, cell.update(game))

        exit = False

        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(x, y)

                if (cell is not None and 
                    cell.type == 'DeathFruitCell' and
                    game.DeathFruitCellCounter == 3):
                    self.set_cell(x, y, None)
                    game.spawn_death_food()
                    game.DeathFruitCellCounter = 0
                    exit = True
                    break

            if exit:
                break

        return

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.cells[x][y] = None
                
        return