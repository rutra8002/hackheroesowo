import pyray as pr
from button import Button

class Menu:
    def __init__(self):
        self.buttons = [
            Button("Segregation Game", 300, 200, 200, 50, pr.DARKGRAY, pr.YELLOW),
            Button("Another Game", 300, 260, 200, 50, pr.DARKGRAY, pr.YELLOW)
        ]
        self.selected_option = 0

    def run(self):
        pr.init_window(800, 600, "Main Menu")
        pr.set_target_fps(60)

        while not pr.window_should_close():
            self.update()
            self.draw()

            if any(button.is_clicked for button in self.buttons):
                pr.close_window()
                return self.selected_option

        pr.close_window()
        return None

    def update(self):
        mouse_pos = pr.get_mouse_position()
        for i, button in enumerate(self.buttons):
            button.update(mouse_pos)
            if button.is_clicked:
                self.selected_option = i

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.SKYBLUE)

        for button in self.buttons:
            button.draw()

        pr.draw_text("Click to select and confirm", 250, 500, 20, pr.BLACK)

        pr.end_drawing()