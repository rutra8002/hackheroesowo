import pyray as pr
from menu import Menu
from segregation_game import SegregationGame

def show_intro():
    pr.init_window(800, 600, "Intro")
    pr.set_target_fps(60)
    alpha = 255

    while not pr.window_should_close() and alpha > 5:
        pr.begin_drawing()
        pr.clear_background(pr.GREEN)
        text = "Help our climate!"
        text_width = pr.measure_text(text, 40)
        pr.draw_text(text, (pr.get_screen_width() - text_width) // 2, pr.get_screen_height() // 2, 40, pr.Color(0, 0, 0, alpha))
        pr.end_drawing()

        alpha -= 2


    pr.close_window()

def main():
    show_intro()
    while True:
        menu = Menu()
        selected_option = menu.run()

        if selected_option == "quit":
            break
        elif selected_option == 0:
            game = SegregationGame()
            result = game.run()
            if result == "menu":
                continue
        elif selected_option == 1:
            # Placeholder for another game
            print("Another game selected")

if __name__ == "__main__":
    main()