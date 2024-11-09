import pyray as pr
from item import Item
from button import Button

class Game:
    def __init__(self):
        pr.init_window(800, 600, "Segregation Game")
        pr.set_target_fps(60)

        self.bins = {
            "paper": pr.Rectangle(100, 500, 150, 80),
            "plastic": pr.Rectangle(300, 500, 150, 80),
            "glass": pr.Rectangle(500, 500, 150, 80)
        }

        self.items = [
            Item("paper", 100, 100, 50, 50, pr.BLUE),
            Item("plastic", 200, 100, 50, 50, pr.RED),
            Item("glass", 300, 100, 50, 50, pr.GREEN)
        ]

        self.dragging_item = None
        self.offset_x = 0
        self.offset_y = 0

        self.return_button = Button("Return to Menu", 650, 10, 140, 40, pr.DARKGRAY, pr.YELLOW)
        self.messages = []

    def run(self):
        while not pr.window_should_close():
            self.update()
            self.draw()

            if self.return_button.is_clicked:
                pr.close_window()
                return "menu"

        pr.close_window()

    def update(self):
        mouse_pos = pr.get_mouse_position()
        self.return_button.update(mouse_pos)

        if self.return_button.is_clicked:
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

        self.return_button.draw()

        text = "Drag and drop items into the correct bins"
        text_width = pr.measure_text(text, 20)
        pr.draw_text(text, (800 - text_width) // 2, 20, 20, pr.BLACK)

        for i, message in enumerate(self.messages[-5:]):
            color = pr.Color(0, 0, 0, message["alpha"])
            pr.draw_text(message["text"], 10, 60 + i * 20, 20, color)

        pr.end_drawing()