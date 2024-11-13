import pyray as pr

class Item:
    def __init__(self, item_type, x, y, width, height, color=None, image_path=None):
        self.type = item_type
        self.rect = pr.Rectangle(x, y, width, height)
        self.color = color
        self.image = pr.load_texture(image_path) if image_path else None
        self.locked = False

    def draw(self):
        if self.image:
            scale_x = self.rect.width / self.image.width
            scale_y = self.rect.height / self.image.height
            pr.draw_texture_ex(self.image, pr.Vector2(self.rect.x, self.rect.y), 0, scale_x, pr.WHITE)
        else:
            pr.draw_rectangle_rec(self.rect, self.color)