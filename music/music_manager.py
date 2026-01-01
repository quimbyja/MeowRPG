import pygame
import threading
import os


class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_on = True
        self.tracks = {
            "menu": "music/dark_fantasy_1.mp3",
            "game": "music/leave_me_here.mp3",
            "launch": "music/launch.wav",
        }
        self.current_track = None  # Текущий воспроизводимый трек

    def _get_full_path(self, relative_path):
        """Преобразует относительный путь в абсолютный."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, "..", relative_path)

    def is_track_available(self, track_key):
        """Проверяет, существует ли файл трека."""
        if track_key not in self.tracks:
            return False
        full_path = self._get_full_path(self.tracks[track_key])
        return os.path.exists(full_path)

    def play_track(self, track_key):
        """
        Запускает воспроизведение указанного трека.
        track_key: 'menu' или 'game'
        """
        if not self.music_on:
            return "Music is off"

        if track_key not in self.tracks:
            return f"Трек '{track_key}' не найден в настройках!"

        full_path = self._get_full_path(self.tracks[track_key])
        if not os.path.exists(full_path):
            return f"Ошибка: файл {full_path} не найден!"


        try:
            # Останавливаем текущий трек, если он играет
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # Загружаем и запускаем новый трек
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(loops=-1)  # loops=-1 → бесконечное повторение
            self.current_track = track_key
            return f"Воспроизводится {track_key}"
        except Exception as e:
            return f"Ошибка воспроизведения: {e}"

    def stop(self):
        """Останавливает музыку."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        self.current_track = None

    def toggle(self):
        """Включает/выключает музыку. При включении — возобновляет последний трек."""
        if self.music_on:
            self.music_on = False
            self.stop()
            return "Music turned off"
        else:
            self.music_on = True
            if self.current_track:
                # Если был трек — запускаем его
                self.play_track(self.current_track)
            else:
                # Иначе — запускаем меню по умолчанию
                self.play_track('menu')
            return "Music turned on"