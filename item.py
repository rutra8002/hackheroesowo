import pyray as pr

class Item:
    def __init__(self, item_type, x, y, width, height, color):
        self.type = item_type
        self.rect = pr.Rectangle(x, y, width, height)
        self.color = color
        self.locked = False

    def draw(self):
        pr.draw_rectangle_rec(self.rect, self.color)