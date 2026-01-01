" Импортируем классы в пространство пакета "
from music.music_manager import MusicManager
from .terminal_ui import TerminalUI

"""from characters.monster import Monster"""

__all__ = ["MusicManager",
           "TerminalUI",
           ]
