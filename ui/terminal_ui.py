import curses
import time

class TerminalUI:
    # ASCII‑арт для главного меню
    MENU_ART = [
        r"______  ___                     ",
        r"___   |/  /_____________      __",
        r"__  /|_/ /_  _ \  __ \_ | /| / /",
        r"_  /  / / /  __/ /_/ /_ |/ |/ / ",
        r"/_/  /_/  \___/\____/____/|__/  ",
        r"                 ____ ____ ____ ",
        r"                ||R |||P |||G ||",
        r"                ||__|||__|||__||",
        r"                |/__\|/__\|/__\|",
    ]

    # Пункты меню
    MENU_ITEMS = [
        "Press S to Start new game",
        "Press Q to Quit game",
        "Press Z to turn on/off music",
    ]

    def __init__(self, stdscr, music_manager):
        self.stdscr = stdscr
        self.music_manager = music_manager
        self.width, self.height = self.stdscr.getmaxyx()
        self.state = "menu" #Текущее состояние - меню

    def set_state(self, new_state):
        """Переключаем состояние UI: 'menu' или 'game'"""
        if new_state in ["menu", "game"]:
            self.state = new_state
        else:
            raise ValueError("State must be 'menu' or 'game'")
        
    def _draw_menu(self):
        """Рисуем главное меню"""
        # Очищаем экран
        self.stdscr.clear()

        if self.height < 6 or self.width < 10:
            self.stdscr.addstr(0, 0, "Терминал слишком мал!")
            self.stdscr.refresh()
            return
        
        #Рамка
        self.stdscr.border()

        # ASCII art of menu
        start_y = 1
        max_art_width = max(len(line) for line in self.MENU_ART)
        x_offset = (self.width - 2 - max_art_width) // 2 + 1

        for i, line in enumerate(self.MENU_ART):
            y = start_y + i
            if y < self.height - 1:
                try:
                    self.stdscr.addstr(y, x_offset, line)
                except curses.error:
                    pass
        
        # Меню под арт
        menu_start_y = start_y + len(self.MENU_ART) + 2
        for i, item in enumerate(self.MENU_ITEMS):
            y = menu_start_y + i
            x = (self.width - len(item)) // 2
            if y < self.height - 1:
                self.stdscr.addstr(y, x, item)

        # Меню под арт
        status = (
            "Фоновая музыка: ВКЛЮЧЕНА"
            if self.music_manager.music_on
            else "Фоновая музыка: ВЫКЛЮЧЕНА"
        )
        
        y_status = self.height - 1
        x_status = (self.width - len(status)) // 2
        if y_status > menu_start_y + len(self.MENU_ITEMS):
            self._safe_addstr(y_status, x_status, status, curses.A_BOLD)

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
        else:
            self.stdscr.clear()
            self.stdscr._safe_addstr(0, 0, f"Неизвестное состояние UI: {self.state}")

        self.stdscr.refresh()

    def show_message(self, msg, duration=1, attr=None):
        """Показываем временное сообщение по центру экрана"""
        y = self.height // 2
        x = (self.width - len(msg)) // 2
        attr = attr or curses.A_BOLD
        self.stdscr.addstr(y, x, msg, attr)
        self.stdscr.refresh()
        time.sleep(duration)
