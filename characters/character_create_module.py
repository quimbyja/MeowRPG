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
        """Рассчитать базовые характеристики на основе класса (единый набор для всех)"""
        base_stats = {
            "Воин": {
                "здоровье": 120,
                "мана": 20,
                "сила": 16,
                "интеллект": 4,
                "выносливость": 14,
                "ловкость": 8
            },
            "Маг": {
                "здоровье": 60,
                "мана": 150,
                "сила": 4,
                "интеллект": 18,
                "выносливость": 8,
                "ловкость": 6
            },
            "Лучник": {
                "здоровье": 80,
                "мана": 40,
                "сила": 8,
                "интеллект": 6,
                "выносливость": 10,
                "ловкость": 16
            },
            "Разбойник": {
                "здоровье": 90,
                "мана": 30,
                "сила": 10,
                "интеллект": 8,
                "выносливость": 12,
                "ловкость": 14
            }
        }
        # Добавляем уровень и опыт к базовым характеристикам
        stats = base_stats.get(self.char_class, {})
        stats["уровень"] = 1
        stats["опыт"] = 0  # текущий опыт
        stats["опыт_до_следующего_уровня"] = 100  # порог для повышения
        return stats
