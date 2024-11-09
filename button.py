import pyray as pr

class Button:
    def __init__(self, text, x, y, width, height, normal_color, hover_color):
        self.text = text
        self.rect = pr.Rectangle(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_clicked = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.normal_color
        pr.draw_rectangle_rec(self.rect, color)
        pr.draw_text(self.text, int(self.rect.x) + 10, int(self.rect.y) + 10, 20, pr.BLACK)

    def update(self, mouse_pos):
        self.is_hovered = pr.check_collision_point_rec(mouse_pos, self.rect)
        if self.is_hovered and pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
            self.is_clicked = True
        else:
            self.is_clicked = False