import pyray as pr
from button import Button

class PauseMenu:
    def __init__(self):
        self.update_buttons()
        self.selected_option = None

    def update_buttons(self):
        width = pr.get_screen_width()
        height = pr.get_screen_height()
        button_width = int(width * 0.25)
        button_height = int(height * 0.08)
        button_x = (width - button_width) // 2
        button_y = int(height * 0.4)

        self.buttons = [
            Button("Resume", button_x, button_y, button_width, button_height, pr.GREEN, pr.YELLOW, pr.BLACK),
            Button("Return to Menu", button_x, button_y + button_height + 20, button_width, button_height, pr.RED, pr.YELLOW, pr.BLACK)
        ]

    def update(self):
        if pr.is_window_resized():
            self.update_buttons()

        mouse_pos = pr.get_mouse_position()
        for button in self.buttons:
            button.update(mouse_pos)
            if button.is_clicked:
                if button.text == "Resume":
                    self.selected_option = "resume"
                elif button.text == "Return to Menu":
                    self.selected_option = "menu"

    def draw(self):
        pr.draw_rectangle(0, 0, pr.get_screen_width(), pr.get_screen_height(), pr.Color(0, 0, 0, 200))
        for button in self.buttons:
            button.draw()