import sqlite3
import json

class CharacterDB:
    def __init__(self, db_path="game.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        """Создаёт таблицу персонажей, если её нет"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("")
            conn.commit()