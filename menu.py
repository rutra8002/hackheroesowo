import pyray as pr
from button import Button

class Menu:
    def __init__(self):
        self.buttons = []
        self.selected_option = None
        self.current_index = 0
        self.animating = False
        self.animation_progress = 0
        self.animation_speed = 0.05
        self.animation_direction = 0

    def run(self):
        pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
        pr.init_window(800, 600, "Main Menu")
        pr.set_target_fps(60)
        self.update_buttons()

        while not pr.window_should_close():
            self.update()
            self.draw()

            if self.selected_option is not None:
                pr.close_window()
                return self.selected_option

        pr.close_window()
        return "quit"

    def update_buttons(self):
        width = pr.get_screen_width()
        height = pr.get_screen_height()
        button_width = int(width * 0.75)
        button_height = int(height * 0.1)
        button_x = (width - button_width) // 2
        button_y = int(height * 0.2)

        self.buttons = [
            Button("Segregation Game", button_x, button_y, button_width, button_height, pr.RED, pr.YELLOW, pr.BLACK),
            Button("Another Game", button_x, button_y + button_height + 20, button_width, button_height, pr.ORANGE, pr.YELLOW, pr.BLACK),
            Button("Quit", button_x, button_y + 2 * (button_height + 20), button_width, button_height, pr.VIOLET, pr.YELLOW, pr.BLACK)
        ]
        self.left_arrow = Button("<", 50, height // 2 - 25, 50, 50, pr.GRAY, pr.DARKGRAY, pr.BLACK)
        self.right_arrow = Button(">", width - 100, height // 2 - 25, 50, 50, pr.GRAY, pr.DARKGRAY, pr.BLACK)

    def update(self):
        if pr.is_window_resized():
            self.update_buttons()

        mouse_pos = pr.get_mouse_position()
        self.buttons[self.current_index].update(mouse_pos)
        self.left_arrow.update(mouse_pos)
        self.right_arrow.update(mouse_pos)

        if not self.animating:
            if self.buttons[self.current_index].is_clicked:
                if self.buttons[self.current_index].text == "Quit":
                    self.selected_option = "quit"
                else:
                    self.selected_option = self.current_index

            if self.left_arrow.is_clicked:
                self.animation_direction = -1
                self.animating = True
            elif self.right_arrow.is_clicked:
                self.animation_direction = 1
                self.animating = True
        else:
            self.animation_progress += self.animation_speed
            if self.animation_progress >= 0.9:
                self.animation_progress = 0
                self.animating = False
                self.current_index = (self.current_index + self.animation_direction) % len(self.buttons)

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.SKYBLUE)

        if self.animating:
            offset = int(pr.get_screen_width() * self.animation_progress * self.animation_direction)
            self.buttons[self.current_index].rect.x = (pr.get_screen_width() - self.buttons[self.current_index].rect.width) // 2 - offset
            next_index = (self.current_index + self.animation_direction) % len(self.buttons)
            self.buttons[next_index].rect.x = pr.get_screen_width() - offset if self.animation_direction == 1 else -self.buttons[next_index].rect.width - offset
            self.buttons[next_index].draw()
        else:
            self.buttons[self.current_index].rect.x = (pr.get_screen_width() - self.buttons[self.current_index].rect.width) // 2

        self.buttons[self.current_index].draw()
        self.left_arrow.draw()
        self.right_arrow.draw()

        pr.end_drawing()