"""
The "game" module provides the necessary components to run a Pac-Man game.

This module defines the `Game` class and the `main` function. The `Game` class represents the game itself and handles the game logic, including managing the game screen, menu, and game state. The `main` function serves as the entry point for running the game.

Classes:
    - Game: Represents the Pac-Man game and manages the game logic.

Functions:
    - main: Entry point for running the Pac-Man game.
"""

import os
import sys
import time
import pygame



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.src.menu.menu import Menu
from app.src.settings.settings import screen_width, screen_height
class Game:
    """
    The `Game` class represents the Pac-Man game.

    This class encapsulates the game's functionality, including managing the game screen, menu, and game state. It provides methods for initializing the game, running the game loop, and handling various game events.
    """

    def __init__(self, screen, testing: bool = False, test: str = None):
        self.screen = screen
        self.testing = testing
        self.test = test
        self.menu = Menu(screen, testing)
        self.testing = testing
        self.menu = Menu(screen, testing)
        self.win = False
        self.stop = True

    def run(self):
        """
        Run the game loop and handle game events.

        This method is responsible for running the game loop, which continuously updates the game state and renders the
        game on the screen. It handles various game events, such as keyboard inputs and quitting the game. The method
        interacts with the `Menu` class to display the game menu and manages the game state, including checking if the
        player has won the game.
        """
        if self.testing:
            self.menu = Menu(self.screen, self.testing, self.test)
            return self.menu.run()
        self.menu.run()
        if self.menu.win and self.stop:
            self.win = True
            self.stop = False


def main(test: str = None):
    """
    Main function for running the game.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('../music/8-bit-dream-land-142093.mp3')
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Pac-Man")
    game = Game(screen)
    end = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        if test:
            match test:
                case "menu":
                    game = Game(screen, testing=True, test='menu')
                case "start":
                    game = Game(screen, testing=True, test='start')
                case "collision":
                    game = Game(screen, testing=True, test='collision')
                case "score":
                    game = Game(screen, testing=True, test='score')
                case "ghost_collision":
                    game = Game(screen, testing=True, test='ghost_collision')
                case "powerup_collision":
                    game = Game(screen, testing=True, test='powerup_collision')
            return game.run()

        try:
            screen.fill((113, 116, 168))
            game.run()
            if game.win:
                end = time.time()
                game.win = False
            if end and time.time() - end > 3:
                game = Game(screen)
                end = None
            pygame.display.update()
            clock.tick(60)
        except pygame.error:
            pygame.quit()
            return


if __name__ == '__main__':
    main()
