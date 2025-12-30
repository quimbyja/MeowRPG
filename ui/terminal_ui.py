import curses
import time
from characters.character_create_module import CreateCharacter
from ASCII_arts import (MENU_ITEMS,
                        MENU_ART,
                        CHARACTER_CREATION, 
                        CHARACTER_ICON)


class TerminalUI:
    menu_art = MENU_ART
    menu_items = MENU_ITEMS
    character_icon = CHARACTER_ICON
    character_creation_art = CHARACTER_CREATION

    def __init__(self, stdscr, music_manager):
        self.stdscr = stdscr
        self.music_manager = music_manager
        self.width, self.height = self.stdscr.getmaxyx()
        self.state = "menu"
        self.current_menu_index = 0
        self.creator = CreateCharacter()

    def set_state(self, new_state):
        """Переключаем состояние UI: 'menu' или 'game'"""
        if new_state in ["menu", "game", "create_character"]:
            self.state = new_state
        else:
            raise ValueError("State must be 'menu' or 'game'")

    def _show_confirmation_window(self,
                                  question="Вы уверены?"):
        """
        Показать диалоговое окно с подтверждением.
        Возвращает: True (если Y), False (если N)
        """
        
        # Получаем размеры экрана
        h, w = self.stdscr.getmaxyx()

        # Размеры диалогового окна (можно настроить)
        dialogue_height = 6
        dialogue_width = 40

        # Координаты центра экрана
        start_y = (h - dialogue_height) // 2
        start_x = (w - dialogue_width) // 2

        # Создаём окно
        dialogue = curses.newwin(dialogue_height,
                                 dialogue_width,
                                 start_y,
                                 start_x,)
        
        dialogue.box()
        
        #Вопрос
        title = question
        dialogue.addstr(2, ((dialogue_width - len(question)) // 2), title)

        # Подсказка с вариантами
        promt = "[Y/N]"
        dialogue.addstr(4, (dialogue_width - len(promt)) // 2, promt)

        #Обновляем
        dialogue.refresh()

        # Настраиваем ввод
        curses.cbreak()           # мгновенный отклик
        self.stdscr.keypad(True)  # поддержка спецклавиш
        curses.noecho()           # не отображать введённый символ
        
        while True:
            key = dialogue.getch()  # ждём ввода в диалоговом окне
            if key in (ord('y'), ord('Y'), ord("н"), ord("Н"), 10, 13):
                return True
            elif key in (ord('n'), ord('N'), ord("т"), ord("Т"), 27):
                return False

    def _draw_create_character(self):
        self.stdscr.clear()
        """Отрисовка экрана создания персонажа"""
        title = "СОЗДАНИЕ ПЕРСОНАЖА"
        self._safe_addstr(2, (self.width - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))

        # Поле ввода имени
        self._safe_addstr(3, 4, "Имя персонажа:")
        name_display = self.creator.char_name or "_"
        self._safe_addstr(4, 15, name_display)
        # Линия разделитель
        self._safe_addstr(5, 1, "-" * (self.width - 2))
        # Рисунок персонажа при создании
        for i, line in enumerate(self.character_creation_art):
            y = 6 + i
            x = self.width - 2 - len(line)
            if y < self.height - 1:
                self.stdscr.addstr(y, x, line)
        # Выбор класса
        self._safe_addstr(8, 4, "Класс:")
        for i, cls in enumerate(self.creator.classes):
            y = 10 + i
            if y < self.height - 1:
                if i == self.creator.selected_class_idx:
                    attr = curses.A_REVERSE
                else:
                    curses.A_NORMAL
                self.stdscr.addstr(y, 8, cls, attr)

        self.stdscr.refresh()

    def _draw_menu(self):
        """Рисуем главное меню"""
        # Очищаем экран
        self.stdscr.clear()

        if self.height < 6 or self.width < 10:
            self.stdscr.addstr(0, 0, "Терминал слишком мал!")
            self.stdscr.refresh()
            return

        self.stdscr.border()

        # ASCII art of menu
        start_y = 1
        max_art_width = max(len(line) for line in self.menu_art)
        x_offset = (self.width - 2 - max_art_width) // 2 + 1

        for i, line in enumerate(self.menu_art):
            y = start_y + i
            if y < self.height - 1:
                try:
                    self.stdscr.addstr(y, x_offset, line)
                except curses.error:
                    pass

        # Меню под арт
        menu_start_y = start_y + len(self.menu_art) + 2
        for i, item in enumerate(self.menu_items):
            y = menu_start_y + i
            x = (self.width - len(item)) // 2
            if y < self.height - 1:
                if i == self.current_menu_index:
                    self.stdscr.attron(curses.A_REVERSE)
                    self.stdscr.addstr(y, x, item)
                    self.stdscr.attroff(curses.A_REVERSE)
                else:
                    self.stdscr.addstr(y, x, item)

        # Статус музыки
        status = (
            "Фоновая музыка: ВКЛЮЧЕНА"
            if self.music_manager.music_on
            else "Фоновая музыка: ВЫКЛЮЧЕНА"
        )

        y_status = self.height - 1
        x_status = (self.width - len(status)) // 2
        if y_status > menu_start_y + len(self.menu_items):
            self._safe_addstr(y_status, x_status, status, curses.A_BOLD)

        self.stdscr.refresh()

    def _safe_addstr(self, y, x, text, attr=None):
        """Безопасно вывести текст в координаты (y, x)"""
        try:
            max_y, max_x = self.stdscr.getmaxyx()  # актуальные размеры

            # Проверка: координаты в пределах экрана?
            if y < 0 or x < 0 or y >= max_y or x >= max_x:
                return False

            # Обрезаем текст, если он выходит за правый край
            visible_width = max_x - x - 1  # -1: запас на край экрана
            if visible_width <= 0:
                return False
            truncated_text = text[:visible_width]

            # Выводим с атрибутами или без
            if attr is not None:
                self.stdscr.addstr(y, x, truncated_text, attr)
            else:
                self.stdscr.addstr(y, x, truncated_text)
                return True
        except curses.error:
            return False  # ошибка вывода — молча игнорируем

    def _draw_game(self):
        """Рисуем игровой экран (пример)"""
        self.stdscr.clear()
        self.stdscr.border()

        title = "RPG game"
        x = (self.width - len(title)) // 2
        self.stdscr.addstr(3, x, title)
        """
        Логику игры придумаем потом
        """

    def draw(self):
        self.height, self.width = self.stdscr.getmaxyx()
        """
        Основной метод отрисовки —
        выбирает экран по текущему state
        """
        if self.state == "menu":
            self._draw_menu()
        elif self.state == "game":
            self._draw_game()
        elif self.state == "create_character":
            self._draw_create_character()
        else:
            self.stdscr.clear()
            self._safe_addstr(0, 0, f"Неизвестное состояние UI: {self.state}")

        self.stdscr.refresh()

    def show_message(self, msg, duration=1, attr=None):
        """Показываем временное сообщение по центру экрана"""
        self.stdscr.clear()
        y = self.height // 2
        x = (self.width - len(msg)) // 2
        attr = attr or curses.A_BOLD
        self.stdscr.addstr(y, x, msg, attr)
        self.stdscr.refresh()
        time.sleep(duration)
