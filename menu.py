import pyray as pr

class Menu:
    def __init__(self):
        self.options = ["Segregation Game", "Another Game"]
        self.selected_option = 0

    def run(self):
        pr.init_window(800, 600, "Main Menu")
        pr.set_target_fps(60)

        while not pr.window_should_close():
            self.update()
            self.draw()

            if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
                pr.close_window()
                return self.selected_option

        pr.close_window()
        return None

    def update(self):
        if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN):
            self.selected_option = (self.selected_option + 1) % len(self.options)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_UP):
            self.selected_option = (self.selected_option - 1) % len(self.options)

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        for i, option in enumerate(self.options):
            color = pr.RED if i == self.selected_option else pr.BLACK
            pr.draw_text(option, 350, 200 + i * 40, 20, color)

        pr.end_drawing()