from menu import Menu
from game import Game

def main():
    while True:
        menu = Menu()
        selected_option = menu.run()

        if selected_option == "quit":
            break
        elif selected_option == 0:
            game = Game()
            result = game.run()
            if result == "menu":
                continue
        elif selected_option == 1:
            # Placeholder for another game
            print("Another game selected")

if __name__ == "__main__":
    main()