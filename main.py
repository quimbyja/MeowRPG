import curses
import time
import threading
from ui import TerminalUI, MusicManager, CreateCharacter


class Game:
    def __init__(self):
        self.music_manager = MusicManager()
        self.ui = None

    def run(self, stdscr):
        curses.curs_set(0)
        self.ui = TerminalUI(stdscr, self.music_manager)

        if self.music_manager.is_music_available():
            threading.Thread(
                target=self.music_manager.play, daemon=True
            ).start()
            time.sleep(0.1)

        while True:
            self.ui.draw()
            char = self.ui.stdscr.getch()
            # Управление в окне создания персонажа
            if self.ui.state == "create_character":
                if char == 27:  #Esc
                    self.ui.state("menu")
                elif char == curses.KEY_RIGHT:
                    self.ui.creator.set_class(+1)
                elif char == curses.KEY_LEFT:
                    self.ui.creator.set_class(-1)
                elif char == 9:
                    char_data = self.ui.creator.get_character_data()
                    self.ui.show_message(
                        f"Персонаж {char_data['name']} ({char_data['class']}) создан!", 2)
                    self.ui.set_state("game")
            # Управление в меню
            if self.ui.state == "menu":
                if char == curses.KEY_UP:
                    self.ui.current_menu_index = max(0, self.ui.current_menu_index - 1)
                elif char == curses.KEY_DOWN:
                    self.ui.current_menu_index = min(
                        len(self.ui.MENU_ITEMS) - 1, self.ui.current_menu_index + 1
                    )
                elif char in [10, 13]: #ENTER
                    selected = self.ui.MENU_ITEMS[self.ui.current_menu_index]
                    if selected == "Новая игра":
                        self.ui.set_state("create_character")
                        self.ui.show_message("Игра началась!", 1.5)
                    elif selected == "Звук Вкл/выкл":
                        self.music_manager.toggle()
                    elif selected == "Выйти из игры":
                        if self.ui._show_confirmation_window("Выйти из игры?"):
                            break
                    else:
                        self.ui.set_state("menu")


            # Управление в режиме игра
            elif self.ui.state == "game":
                if char == ord("q") or char == ord("Q"):
                    self.ui.state = "menu"
                if char == ord("w") or char == ord("W"):
                    self.ui.show_message("Вы идете вперед", 3)

def main(stdscr):
    game = Game()
    game.run(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)