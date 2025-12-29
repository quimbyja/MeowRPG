import curses
import time
import threading
from ui import MusicManager, TerminalUI


class Game:
    def __init__(self):
        self.music_manager = MusicManager()
        self.ui = None

    def run(self, stdscr):
        curses.curs_set(0)
        self.ui = TerminalUI(stdscr, self.music_manager)

        if self.music_manager.is_music_available():
            threading.Thread(
                target=self.music_manager.play, daemon=True
            ).start()
            time.sleep(0.1)

        while True:
            self.ui.draw()
            char = self.ui.stdscr.getch()
            if self.ui.state == "menu":
                if char == ord("q") or char == ord("Q"):
                    break
                if char == ord("s") or char == ord("S"):
                    self.ui.set_state("game")
                    self.ui.show_message("Игра началась!", 1.5)
                elif char == ord("z") or char == ord("Z"):
                    msg = self.music_manager.toggle()
                    self.ui.show_message(msg, 1)
            elif self.ui.state == "game":
                if char == ord("q") or char == ord("Q"):
                    self.ui.state = "menu"
                if char == ord("w") or char == ord("W"):
                    self.ui.show_message("Вы идете вперед", 3)

def main(stdscr):
    game = Game()
    game.run(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)