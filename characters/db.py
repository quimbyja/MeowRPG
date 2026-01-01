import sqlite3
import json


class CharacterDB:
    def __init__(self, db_path="game.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        """Создаёт таблицу персонажей, если её нет"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    class TEXT NOT NULL,
                    stats TEXT NOT NULL,  -- JSON-строка с характеристиками
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def save_character(self, char_data: dict) -> bool:
        """
        Сохраняет персонажа в БД (перезаписывает существующую запись)
        Возвращает True при успехе, False при ошибке
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    class TEXT NOT NULL,
                    stats TEXT NOT NULL,  -- JSON-строка с характеристиками
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def save_character(self, char_data: dict) -> bool:
        """Сохраняет персонажа в БД (перезаписывает запись с id=1)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                stats_json = json.dumps(char_data['stats'])
                conn.execute('''
                    INSERT OR REPLACE INTO characters 
                    (id, name, class, stats)
                    VALUES (1, ?, ?, ?)
                ''', (char_data['name'], char_data['class'], stats_json))
                conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка сохранения в БД: {e}")
            return False
    
    def load_character(self) -> dict | None:
        """Загружает персонажа из БД (id=1) или возвращает None"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                row = conn.execute(
                    'SELECT name, class, stats FROM characters WHERE id = 1'
                ).fetchone()
                if row:
                    return {
                        'name': row[0],
                        'class': row[1],
                        'stats': json.loads(row[2])
                    }
        except Exception as e:
            print(f"Ошибка загрузки из БД: {e}")
        return None
    
    def has_save(self) -> bool:
        """Проверяет, есть ли сохранённый персонаж"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                count = conn.execute(
                    'SELECT COUNT(*) FROM characters WHERE id = 1'
                ).fetchone()[0]
                return count > 0
        except:
            return False