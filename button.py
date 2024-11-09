import pyray as pr

class Button:
    def __init__(self, text, x, y, width, height, normal_color, hover_color, text_color):
        self.text = text
        self.rect = pr.Rectangle(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.is_clicked = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.normal_color
        pr.draw_rectangle_rec(self.rect, color)
        text_width = pr.measure_text(self.text, 20)
        text_x = int(self.rect.x + (self.rect.width - text_width) / 2)
        text_y = int(self.rect.y + (self.rect.height - 20) / 2)
        pr.draw_text(self.text, text_x, text_y, 20, self.text_color)

    def update(self, mouse_pos):
        self.is_hovered = pr.check_collision_point_rec(mouse_pos, self.rect)
        if self.is_hovered and pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
            self.is_clicked = True
        else:
            self.is_clicked = False