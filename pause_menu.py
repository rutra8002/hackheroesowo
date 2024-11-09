import pyray as pr
from button import Button

class PauseMenu:
    def __init__(self):
        self.buttons = [
            Button("Resume", 300, 200, 200, 50, pr.GREEN, pr.YELLOW, pr.BLACK),
            Button("Return to Menu", 300, 260, 200, 50, pr.RED, pr.YELLOW, pr.BLACK)
        ]
        self.selected_option = None

    def update(self):
        mouse_pos = pr.get_mouse_position()
        for button in self.buttons:
            button.update(mouse_pos)
            if button.is_clicked:
                if button.text == "Resume":
                    self.selected_option = "resume"
                elif button.text == "Return to Menu":
                    self.selected_option = "menu"

    def draw(self):
        pr.draw_rectangle(0, 0, 800, 600, pr.Color(0, 0, 0, 200))
        for button in self.buttons:
            button.draw()