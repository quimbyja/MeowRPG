class CreateCharacter:
    count = 0
    def __init__(self):
        self.char_name = ""
        self.selected_class_idx = 0
        self.classes = ["Воин", "Маг", "Лучник", "Разбойник"]
        self.char_class = self.classes[self.selected_class_idx]
        

    def set_name(self, name: str):
        """Установить имя персонажа (с ограничением длины)"""
        max_length = 20
        self.char_name = name.strip()[:max_length]

    def set_class(self, delta: int):
        """Изменить выбранный класс на delta (-1 или +1)"""
        self.selected_class_idx += delta
        # Ограничиваем индекс границами списка
        self.selected_class_idx = max(0, min(len(self.classes) - 1, self.selected_class_idx))
        # Обновляем текущий класс
        self.char_class = self.classes[self.selected_class_idx]
    
    def get_character_data(self) -> dict:
        """Вернуть данные персонажа для использования в игре"""
        return {
            "name": self.char_name or "Мявка",
            "class": self.char_class,
            "stats": self._calculate_status()
        }

    def _calculate_status(self) -> dict:
        """Рассчитать базовые характеристики на основе класса"""
        base_stats = {
            "Воин": {"сила": 15, "ловкость": 8, "интеллект": 5},
            "Маг": {"сила": 5, "ловкость": 8, "интеллект": 15},
            "Лучник": {"сила": 8, "ловкость": 15, "интеллект": 6},
            "Разбойник": {"сила": 7, "ловкость": 14, "интеллект": 7}
        }
        return base_stats.get(self.char_class)