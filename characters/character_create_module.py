class CreateCharacter:
    count = 0
    def __init__(self):
        self.char_name = ""
        self.char_class = "Воин"
        self.classes = ["Воин", "Маг", "Лучник", "Разбойник"]

    def set_name(self, name: str):
        """Установить имя персонажа (с ограничением длины)"""
        max_length = 20
        self.char_name = name.strip()[:max_length]

    def set_class(self, direction: int):
        """
        Сменить класс на следующий/предыдущий
        direction: +1 — вправо, -1 — влево
        """
        idx = self.classes.index(self.char_class)
        new_idx = (idx + direction) % len(self.classes)
        self.char_class = self.classes[new_idx]
    
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