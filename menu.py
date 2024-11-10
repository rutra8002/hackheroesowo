import pyray as pr
from button import Button

class Menu:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.buttons = [
            Button("Segregation Game", 100, 100, 600, 400, pr.RED, pr.YELLOW, pr.BLACK),
            Button("Another Game", 100, 100, 600, 400, pr.ORANGE, pr.YELLOW, pr.BLACK),
            Button("Quit", 100, 100, 600, 400, pr.VIOLET, pr.YELLOW, pr.BLACK)
        ]
        self.selected_option = None
        self.current_index = 0
        self.left_arrow = Button("<", 50, 300, 50, 50, pr.GRAY, pr.DARKGRAY, pr.BLACK)
        self.right_arrow = Button(">", 700, 300, 50, 50, pr.GRAY, pr.DARKGRAY, pr.BLACK)
        self.animating = False
        self.animation_progress = 0
        self.animation_speed = 0.05
        self.animation_direction = 0

    def run(self):
        pr.init_window(self.width, self.height, "Main Menu")
        pr.set_target_fps(60)

        while not pr.window_should_close():
            self.update()
            self.draw()

            if self.selected_option is not None:
                pr.close_window()
                return self.selected_option

        pr.close_window()
        return "quit"

    def update(self):
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
            if self.animation_progress >= 1:
                self.animation_progress = 0
                self.animating = False
                self.current_index = (self.current_index + self.animation_direction) % len(self.buttons)

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.SKYBLUE)

        if self.animating:
            offset = int(self.width * self.animation_progress * self.animation_direction)
            self.buttons[self.current_index].rect.x = 100 - offset
            next_index = (self.current_index + self.animation_direction) % len(self.buttons)
            self.buttons[next_index].rect.x = 900 - offset if self.animation_direction == 1 else -700 - offset
            self.buttons[next_index].draw()
        else:
            self.buttons[self.current_index].rect.x = 100

        self.buttons[self.current_index].draw()
        self.left_arrow.draw()
        self.right_arrow.draw()

        pr.end_drawing()