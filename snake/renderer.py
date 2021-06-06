from PyQt5.QtGui import QColor


class Renderer:
    def __init__(self, painter):
        BRIGHTNESS = 64
        self.COLOR_TABLE = {}

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    color = str(i) + str(j) + str(k)
                    r = i * 64 + BRIGHTNESS
                    g = j * 64 + BRIGHTNESS
                    b = k * 64 + BRIGHTNESS
                    self.COLOR_TABLE[color] = QColor(r, g, b)

        self.painter = painter
        return

    def render(self, field):
        square_size = self.get_square_size(field)
        self.draw_background(0, 0, field, '222')

        for x in range(field.width):
            for y in range(field.height):
                cell = field.get_cell(x, y)

                if cell is not None:
                    self.draw_square(x * square_size[0], 
                                     y * square_size[1], 
                                     square_size, cell.color)
        return

    def get_square_size(self, field):
        rect = self.painter.window()
        return (rect.width() // field.width, 
                rect.height() // field.height)

    def draw_square(self, x, y, size, color_index):
        width, height = size
        color = QColor(self.COLOR_TABLE[color_index])
        painter = self.painter
        px = 1
        painter.fillRect(x + px, y + px, 
                         width - 2 * px, height - 2 * px, color)
        painter.fillRect(x + 2 * px, y, 
                         width - 4 * px, px, color.lighter())
        painter.fillRect(x + 2 * px, y + height - px, 
                         width - 4 * px, px, color.darker())
        painter.fillRect(x, y + 2 * px, 
                         px, height - 4 * px, color.lighter())
        painter.fillRect(x + width - px, y + 2 * px, 
                         px, height - 4 * px, color.darker())
        painter.fillRect(x + px, y + px, 
                         px, px, color.lighter())
        painter.fillRect(x + px, y + height - 2 * px, 
                         px, px, color.darker())
        painter.fillRect(x + width - 2 * px, y + px, 
                         px, px, color.lighter())
        painter.fillRect(x + width - 2 * px, y + height - 2 * px, 
                         px, px, color.darker())
        return

    def draw_background(self, x, y, field, color_index):
        width, height = self.get_square_size(field)
        self.painter.fillRect(x, y, 
                              width * field.width, 
                              height * field.height, 
                              QColor(self.COLOR_TABLE[color_index]))   
        return