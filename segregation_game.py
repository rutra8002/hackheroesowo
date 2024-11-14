import pyray as pr
from item import Item
from button import Button
from pause_menu import PauseMenu

class SegregationGame:
    def __init__(self):
        pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
        pr.init_window(800, 600, "Segregation Game")
        pr.set_target_fps(60)
        self.update_layout()

        self.dragging_item = None
        self.offset_x = 0
        self.offset_y = 0

        self.pause_menu = PauseMenu()
        self.is_paused = False
        self.messages = []

    def update_layout(self):
        width = pr.get_screen_width()
        height = pr.get_screen_height()
        bin_width = int(width * 0.15)
        bin_height = int(height * 0.1)
        bin_y = height - bin_height - 20

        self.bins = {
            "paper": pr.Rectangle(int(width * 0.1), bin_y, bin_width, bin_height),
            "plastic": pr.Rectangle(int(width * 0.4), bin_y, bin_width, bin_height),
            "glass": pr.Rectangle(int(width * 0.7), bin_y, bin_width, bin_height)
        }

        item_size = int(min(width, height) * 0.1)
        self.items = [
            Item("paper", int(width * 0.1), int(height * 0.1), item_size, item_size, image_path="images/paper.png"),
            Item("plastic", int(width * 0.3), int(height * 0.1), item_size, item_size, image_path="images/plastic.png"),
            Item("glass", int(width * 0.5), int(height * 0.1), item_size, item_size, image_path="images/glass.png")
        ]

        self.pause_button = Button("| |", width - 50, 10, 40, 40, pr.DARKGRAY, pr.YELLOW, pr.WHITE)

    def run(self):
        while not pr.window_should_close():
            self.update()
            self.draw()

            if self.pause_menu.selected_option == "menu":
                pr.close_window()
                return "menu"
            elif self.pause_menu.selected_option == "resume":
                self.is_paused = False
                self.pause_menu.selected_option = None

        pr.close_window()

    def update(self):
        if pr.is_window_resized():
            self.update_layout()

        mouse_pos = pr.get_mouse_position()
        self.pause_button.update(mouse_pos)

        if self.pause_button.is_clicked:
            self.is_paused = True

        if self.is_paused:
            self.pause_menu.update()
            return

        mouse_pos.x = int(mouse_pos.x)
        mouse_pos.y = int(mouse_pos.y)

        if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
            for item in self.items:
                if not item.locked and pr.check_collision_point_rec(mouse_pos, item.rect):
                    self.dragging_item = item
                    self.offset_x = mouse_pos.x - item.rect.x
                    self.offset_y = mouse_pos.y - item.rect.y
                    break

        if pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT) and self.dragging_item:
            self.dragging_item.rect.x = mouse_pos.x - self.offset_x
            self.dragging_item.rect.y = mouse_pos.y - self.offset_y

        if pr.is_mouse_button_released(pr.MouseButton.MOUSE_BUTTON_LEFT) and self.dragging_item:
            for bin_type, bin_rect in self.bins.items():
                if pr.check_collision_recs(self.dragging_item.rect, bin_rect):
                    if self.dragging_item.type == bin_type:
                        message = f"Correct! {self.dragging_item.type} item placed in {bin_type} bin."
                        self.dragging_item.locked = True
                    else:
                        message = f"Wrong! {self.dragging_item.type} item should not be placed in {bin_type} bin."
                    self.messages.append({"text": message, "alpha": 255, "timer": 0})
            self.dragging_item = None

        for message in self.messages:
            message["timer"] += 1
            if message["timer"] > 60:
                message["alpha"] -= 5
                if message["alpha"] < 0:
                    message["alpha"] = 0

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.LIGHTGRAY)

        for bin_type, bin_rect in self.bins.items():
            pr.draw_rectangle_rec(bin_rect, pr.DARKGRAY)
            text_width = pr.measure_text(bin_type.capitalize(), 20)
            pr.draw_text(bin_type.capitalize(), int(bin_rect.x + (bin_rect.width - text_width) / 2), int(bin_rect.y + 20), 20, pr.WHITE)

        for item in self.items:
            item.draw()

        self.pause_button.draw()

        text = "Drag and drop items into the correct bins"
        text_width = pr.measure_text(text, 20)
        pr.draw_text(text, (pr.get_screen_width() - text_width) // 2, 20, 20, pr.BLACK)

        for i, message in enumerate(self.messages[-5:]):
            color = pr.Color(0, 0, 0, message["alpha"])
            pr.draw_text(message["text"], 10, 60 + i * 20, 20, color)

        if self.is_paused:
            self.pause_menu.draw()

        pr.end_drawing()