import curses
import time
from ui import TerminalUI, MusicManager
from characters import CharacterDB
"""from ASCII_arts import MENU_ITEMS as MENU_ITEMS"""


class Game:
    def __init__(self):
        self.music_manager = MusicManager()
        self.ui = None
        # Инициализация БД
        self.db = CharacterDB()
        self.current_character = None

    def load_player(self):
        """Загружает персонажа из БД и сохраняет в self.current_character"""
        self.current_character = self.db.load_character()
        if self.current_character is None:
            print("Нет сохранённого персонажа.")
        else:
            print(f"Загружен персонаж: {self.current_character['name']}")

    def run(self, stdscr):
        curses.curs_set(0)
        self.ui = TerminalUI(stdscr, self.music_manager, self)

        # Загружаем персонажа из БД
        self.load_player()

        # Проверяем наличие сохранения
        if self.db.has_save():
            self.current_character = self.db.load_character()

        # Обновляем меню (добавляем "Продолжить", если есть сохранение)
        self.ui._update_menu()

        self.ui.set_state("launch")
        self.ui.draw()
        self.music_manager.play_track("launch")
        """stdscr.refresh()"""
        time.sleep(0.5)

        # Запускаем музыку меню при старте
        if self.music_manager.is_track_available("menu"):
            self.music_manager.play_track("menu")

        self.ui.set_state("menu")

        while True:
            self.ui.draw()
            char = self.ui.stdscr.getch()
            # Управление в окне создания персонажа
            if self.ui.state == "create_character":
                if char == 27:  # Esc
                    self.ui.set_state("menu")
                elif char == curses.KEY_UP:
                    self.ui.creator.set_class(-1)
                elif char == curses.KEY_DOWN:
                    self.ui.creator.set_class(+1)
                elif char in [10, 13]:
                    char_data = self.ui.creator.get_character_data()
                    if self.db.save_character(char_data):
                        self.current_character = char_data
                        self.ui._update_menu()  # Обновляем меню после сохранения
                    self.ui.show_message(
                        f"Персонаж {char_data["name"]} ({char_data["class"]}) создан!",2)
                    self.ui.set_state("game")
                    self.music_manager.play_track("game")
                elif char in [curses.KEY_BACKSPACE, 127]:  # Backspace
                    if self.ui.creator.char_name:
                        self.ui.creator.char_name = self.ui.creator.char_name[:-1]
                # Печатные символы (ASCII)
                elif 32 <= char <= 126:
                    self.ui.creator.char_name += chr(char)
                """self.ui.draw()"""
            # Управление в меню
            if self.ui.state == "menu":
                if char == curses.KEY_UP:
                    self.ui.current_menu_index = max(0, self.ui.current_menu_index - 1)
                elif char == curses.KEY_DOWN:
                    self.ui.current_menu_index = min(
                        len(self.ui.menu_items) - 1,
                        self.ui.current_menu_index + 1
                    )
                elif char in [10, 13]:  # ENTER
                    selected = self.ui.menu_items[self.ui.current_menu_index]
                    if selected == "Новая игра":
                        if self.db.has_save():
                            # Показываем окно подтверждения с предупреждением
                            confirm = self.ui._show_confirmation_window(
                                 "Начать новую игру?")
                            if not confirm:
                                # Пользователь отменил действие — остаёмся в меню
                                continue
                        self.ui.set_state("create_character")
                        self.ui.show_message("Игра началась!", 1.5)
                    elif selected == "Продолжить":
                        if self.current_character:
                            self.ui.set_state("game")
                            self.music_manager.play_track("game")
                    elif selected == "Звук Вкл/выкл":
                        self.music_manager.toggle()
                    elif selected == "Выйти из игры":
                        if self.ui._show_confirmation_window("Выйти из игры?"):
                            break
                    else:
                        self.ui.set_state("menu")

            # Управление в режиме игра
            elif self.ui.state == "game":
                if char == 27:
                    selected_option = self.ui._draw_game_menu_window()
                    if selected_option is not None:
                        if selected_option == 0:
                            pass
                        elif selected_option == 1:
                            pass
                        elif selected_option == 2:
                            self.ui.state = "menu"
                            self.music_manager.play_track('menu')
                        elif selected_option == 3:
                            raise SystemExit("Игра завершена")
                elif char == 9:  # Tab — открыть инвентарь
                    self.ui._draw_inventory()
                

def main(stdscr):
    game = Game()
    game.run(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
