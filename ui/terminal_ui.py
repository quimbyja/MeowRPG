import curses
import time
from characters import CreateCharacter
from characters import (WARRIOR,
                        MAGE,
                        ARCHER,
                        ROGUE)
from ASCII_arts import (MENU_ITEMS,
                        MENU_ART,
                        GAME_MENU_ITEMS,
                        CHARACTER_CREATION,
                        CHARACTER_ICON,
                        LAUNCH_ART)


class TerminalUI:
    GAME_DATA = {
        "Воин": WARRIOR,
        "Маг": MAGE,
        "Лучник": ARCHER,
        "Разбойник": ROGUE
    }
    menu_art = MENU_ART
    menu_items = MENU_ITEMS
    character_icon = CHARACTER_ICON
    character_creation_art = CHARACTER_CREATION
    game_version = "v 1.0.0"

    def __init__(self, stdscr, music_manager):
        self.stdscr = stdscr
        self.music_manager = music_manager
        self.width, self.height = self.stdscr.getmaxyx()
        self.state = "menu"
        self.current_menu_index = 0
        self.creator = CreateCharacter()
        self.sound_enabled = True

    def set_state(self, new_state):
        """Переключаем состояние UI:
        'menu' или 'game' или 'create_character' или 'launch' """
        if new_state in ["menu", "game", "create_character", "launch"]:
            self.state = new_state
        else:
            raise ValueError("Smth went wrong")

    def _fade_launch_art(self, fade_in=True, steps=40, delay=0.03):
        """
        Плавно показать (fade_in=True) или скрыть (fade_in=False) заставку.
        :param steps: количество шагов перехода (больше = плавнее).
        :param delay: пауза между шагами (в секундах).
        """
        # Определяем начальную и конечную «яркость» (от 0 до 255)
        if fade_in:
            alphas = list(range(0, 256, 256 // steps))
        else:
            alphas = list(range(255, -1, -256 // steps))

        for alpha in alphas:
            self.stdscr.clear()
            self.stdscr.border()

        # Рассчитываем смещение по горизонтали
        max_art_width = max(len(line) for line in LAUNCH_ART)
        x = (self.width - 2 - max_art_width) // 2
        start_y = (self.height - len(LAUNCH_ART)) // 2
        for idx, line in enumerate(LAUNCH_ART):
            y = start_y + idx
            if y < self.height - 1 and len(line) <= self.width - 2:
                # Основной текст
                attr = curses.A_BOLD if alpha > 120 else curses.A_NORMAL
                self.stdscr.addstr(y, x, line, attr)

                # «Тень» со смещением (эффект размытия)
                shadow_attr = curses.A_DIM
                self.stdscr.addstr(y + 1, x + 1, line, shadow_attr)

        self.stdscr.refresh()
        time.sleep(delay)

    def _draw_launch(self):
        # Сброс всех атрибутов
        self.stdscr.bkgd(' ')        # Фон — пробел, без атрибутов
        self.stdscr.attrset(0)     # Все атрибуты — сбросить

        self._fade_launch_art(fade_in=True, steps=40, delay=0.05)
        time.sleep(1.5)  # Держим яркий текст 1.5 сек
        self._fade_launch_art(fade_in=False, steps=40, delay=0.05)

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
        
        # Вопрос
        title = question
        dialogue.addstr(2, ((dialogue_width - len(question)) // 2), title)

        # Подсказка с вариантами
        promt = "[Y/N]"
        dialogue.addstr(4, (dialogue_width - len(promt)) // 2, promt)

        # Обновляем
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
                dialogue.clear()
                dialogue.refresh()
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
            x = self.width - 2 - len(line.lstrip())
            if y < self.height - 1:
                self.stdscr.addstr(y, x, line.lstrip())
        # Выбор класса
        self._safe_addstr(8, 4, "Класс:")
        for i, cls in enumerate(self.creator.classes):
            y = 10 + i
            if y < self.height - 1:
                attr = curses.A_NORMAL
                if i == self.creator.selected_class_idx:
                    attr = curses.A_REVERSE
                self.stdscr.addstr(y, 8, cls, attr)
        
        # Описание класса
        selected_idx = self.creator.selected_class_idx
        class_name = self.creator.classes[selected_idx]
        description_lines = [""]
        if class_name in self.GAME_DATA:
            description_lines = self.GAME_DATA[class_name]
        else:
            description_lines = [f"Описание для '{class_name}' отсутствует."]
        for i, line in enumerate(description_lines):
            y = 17 + i
            if y < self.height - 1:
                self._safe_addstr(y, 1, line)
        
        # Блок статистики справа
        stats = self.creator._calculate_status()
        if stats:
            stats_y = 7  # Начало вывода статистики
            stats_x = 30  # Правая половина экрана

            # Заголовок
            self._safe_addstr(stats_y, stats_x, "ХАРАКТЕРИСТИКИ:", curses.A_BOLD)

            # Порядок вывода: здоровье → мана → остальные
            stat_order = ["здоровье", "мана", "сила", "интеллект", "выносливость", "ловкость"]

            for i, stat_name in enumerate(stat_order):
                if stat_name in stats:
                    y = stats_y + 2 + i  # Смещение по вертикали
                    if y < self.height - 1:  # Проверка границ экрана
                        display_name = stat_name.capitalize()
                        value = stats[stat_name]
                        # Форматирование: название слева, значение справа
                        line = f"{display_name:<12}: {value:>4}"
                        self._safe_addstr(y, stats_x, line)

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
        start_y = 5
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

        self.stdscr.addstr(self.height - 2, 1, self.game_version)

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

    def _draw_game_menu_window(self):
        h, w = self.stdscr.getmaxyx()
        menu_height = 15
        menu_width = 20

        start_y = (h - menu_height) // 2
        start_x = (w - menu_width) // 2
        game_menu = curses.newwin(menu_height,
                                  menu_width,
                                  start_y,
                                  start_x)
        game_menu.box()

        menu_items = GAME_MENU_ITEMS
        selected_idx = 0

        while True:
            title = "Меню"
            title_height = 3
            title_width = len(title) + 4
            title_y = 1
            title_x = (menu_width - title_width) // 2
            title_win = game_menu.derwin(title_height, title_width, title_y, title_x)
            title_win.box()
            title_win.addstr(1, 2, title, curses.A_BOLD)

            sound_item = "Звук ВКЛ" if self.sound_enabled else "Звук ВЫКЛ"
            display_items = menu_items[:]
            display_items[1] = sound_item

            for idx, item in enumerate(display_items):
                attr = curses.A_REVERSE
                if idx != selected_idx:
                    attr = curses.A_NORMAL
                game_menu.addstr(5 + idx * 2, (menu_width - len(item)) // 2, item, attr)

            game_menu.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                selected_idx = (selected_idx - 1) % len(menu_items)
            elif key == curses.KEY_DOWN:
                selected_idx = (selected_idx + 1) % len(menu_items)
            elif key in [10, 13]:
                if selected_idx == 1:
                    self.sound_enabled = not self.sound_enabled
                    continue
                elif selected_idx == 2:
                    if self._show_confirmation_window("Выйти в главное меню?"):
                        return 2  # Закрываем меню, передаём сигнал
                    else:
                        game_menu.clear()
                        game_menu.box()
                        continue  # Остаёмся в меню после отмены
                elif selected_idx == 3:  # "Выйти из игры"
                    if self._show_confirmation_window("Выйти из игры?"):
                        return 3  # Закрываем меню, передаём сигнал
                    else:
                        game_menu.clear()
                        game_menu.box()
                        continue  # Остаёмся в меню после отмены
                else:
                    return selected_idx  # "Продолжить" — закрываем меню           
            elif key == 27:
                return None

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
        elif self.state == "launch":
            self._draw_launch()
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
