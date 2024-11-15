import pyray as pr
from item import Item
from button import Button
from pause_menu import PauseMenu

class RecyclingSorterGame:
    def __init__(self):
        pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
        pr.init_window(800, 600, "Recycling Sorter Game")
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
                        message = {"text": "CORRECT", "color": pr.GREEN, "alpha": 255, "timer": 0, "duration": 60}
                        self.dragging_item.locked = True
                    else:
                        message = {"text": "WRONG", "color": pr.RED, "alpha": 255, "timer": 0, "duration": 60}
                    self.messages.append(message)
            self.dragging_item = None

        if all(item.locked for item in self.items) and not any(msg["text"] == "COMPLETED" for msg in self.messages):
            self.messages.append({"text": "COMPLETED", "color": pr.YELLOW, "alpha": 255, "timer": 0, "duration": 180})

        for message in self.messages:
            message["timer"] += 1
            if message["timer"] > message["duration"]:
                message["alpha"] -= 5
                if message["alpha"] < 0:
                    message["alpha"] = 0

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.LIGHTGRAY)

        for bin_type, bin_rect in self.bins.items():
            pr.draw_rectangle_rec(bin_rect, pr.DARKGRAY)
            text_width = pr.measure_text(bin_type.capitalize(), 20)
            pr.draw_text(bin_type.capitalize(), int(bin_rect.x + (bin_rect.width - text_width) / 2),
                         int(bin_rect.y + 20), 20, pr.WHITE)

        for item in self.items:
            item.draw()

        self.pause_button.draw()

        text = "Drag and drop items into the correct bins"
        text_width = pr.measure_text(text, 20)
        pr.draw_text(text, (pr.get_screen_width() - text_width) // 2, 20, 20, pr.BLACK)

        for message in self.messages[-5:]:
            color = pr.Color(message["color"][0], message["color"][1], message["color"][2], message["alpha"])
            text_width = pr.measure_text(message["text"], 40)
            text_height = 40
            text_x = (pr.get_screen_width() - text_width) // 2
            text_y = (pr.get_screen_height() - text_height) // 2

            rect_color = pr.Color(50, 50, 50, message["alpha"])
            pr.draw_rectangle(text_x - 10, text_y - 5, text_width + 20, text_height + 10, rect_color)

            # Draw text
            pr.draw_text(message["text"], text_x, text_y, 40, color)

        if self.is_paused:
            self.pause_menu.draw()

        pr.end_drawing()