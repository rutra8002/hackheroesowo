import pyray as pr

# Initialize the window
pr.init_window(800, 600, b"Segregation Game")

# Set the target FPS
pr.set_target_fps(60)

# Define bins
bins = {
    "paper": pr.Rectangle(100, 500, 150, 80),
    "plastic": pr.Rectangle(300, 500, 150, 80),
    "glass": pr.Rectangle(500, 500, 150, 80)
}

# Define items
items = [
    {"type": "paper", "rect": pr.Rectangle(100, 100, 50, 50), "color": pr.BLUE},
    {"type": "plastic", "rect": pr.Rectangle(200, 100, 50, 50), "color": pr.RED},
    {"type": "glass", "rect": pr.Rectangle(300, 100, 50, 50), "color": pr.GREEN}
]

# Dragging state
dragging_item = None
offset_x = 0
offset_y = 0

while not pr.window_should_close():
    mouse_pos = pr.get_mouse_position()
    mouse_pos.x = int(mouse_pos.x)
    mouse_pos.y = int(mouse_pos.y)
    # Check for dragging
    if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
        for item in items:
            if pr.check_collision_point_rec(mouse_pos, item["rect"]):
                dragging_item = item
                offset_x = mouse_pos.x - item["rect"].x
                offset_y = mouse_pos.y - item["rect"].y
                break

    if pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT) and dragging_item:
        dragging_item["rect"].x = mouse_pos.x - offset_x
        dragging_item["rect"].y = mouse_pos.y - offset_y

    if pr.is_mouse_button_released(pr.MouseButton.MOUSE_BUTTON_LEFT) and dragging_item:
        for bin_type, bin_rect in bins.items():
            if pr.check_collision_recs(dragging_item["rect"], bin_rect):
                if dragging_item["type"] == bin_type:
                    print(f"Correct! {dragging_item['type']} item placed in {bin_type} bin.")
                else:
                    print(f"Wrong! {dragging_item['type']} item should not be placed in {bin_type} bin.")
        dragging_item = None

    # Start drawing
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)

    # Draw bins
    pr.draw_rectangle_rec(bins["paper"], pr.LIGHTGRAY)
    pr.draw_text("Paper", int(bins["paper"].x) + 20, int(bins["paper"].y) + 20, 20, pr.BLACK)
    pr.draw_rectangle_rec(bins["plastic"], pr.LIGHTGRAY)
    pr.draw_text("Plastic", int(bins["plastic"].x) + 20, int(bins["plastic"].y) + 20, 20, pr.BLACK)
    pr.draw_rectangle_rec(bins["glass"], pr.LIGHTGRAY)
    pr.draw_text("Glass", int(bins["glass"].x) + 20, int(bins["glass"].y) + 20, 20, pr.BLACK)

    # Draw items
    for item in items:
        pr.draw_rectangle_rec(item["rect"], item["color"])

    # End drawing
    pr.end_drawing()

# Close the window
pr.close_window()