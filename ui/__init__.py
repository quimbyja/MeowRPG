" Импортируем классы в пространство пакета "
from music.music_manager import MusicManager
from .terminal_ui import TerminalUI
from character.character_create_module import CreateCharacter

__all__ = ["MusicManager",
           "TerminalUI",
           "CreateCharacter"
           ]