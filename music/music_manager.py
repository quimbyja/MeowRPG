import pygame
import threading
import os

class MusicManager:
    def __init__(self, music_filename="music/menu_music.mp3"):
        pygame.mixer.init()
        self.music_on = True
        self.music_filename = music_filename
        self.music_path = self._get_music_path()
    
    def _get_music_path(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, "..", self.music_filename)
    
    def is_music_available(self):
        return os.path.exists(self.music_path)
    
    def play(self):
        if not self.is_music_available():
            return f"Ошибка: файл {self.music_filename} не найден!"
        
        try:
            pygame.mixer.music.load(self.music_path)
            while self.music_on:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(loops=0)
                pygame.time.wait(100)
        except Exception as e:
            return f"Ошибка воспроизведения: {e}"
        
    def toggle(self):
        if self.music_on:
            self.music_on = False
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
            return "Music turned off"
        else:
            self.music_on = True
            threading.Thread(target=self.play, daemon=True).start()
            return "Music turned on"