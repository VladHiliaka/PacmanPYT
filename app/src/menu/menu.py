"""
This module implements the main menu of the game.
"""

import os
import pygame

from app.src.gameplay.level import Level
from app.src.menu.button import Button
from app.src.settings.settings import tile_size
from app.src.settings.tiles import AnimatedTile


class Menu:
    """
    The main menu of the game.
    """

    def __init__(self, surface, testing: bool = False, test: str = None):
        """
        Initialize the menu.
        """
        self.testing = testing
        self.test = test
        self.start = False
        self.level = None
        self.display = surface
        self.skin = 'original'
        self.win = False
        self.skinShop = Skins(self.display)
        self.skinClick = False
        self.startButton = Button(pygame.image.load('../images/buttons/start_btn.png').convert_alpha(), 234, 100)
        self.exitButton = Button(pygame.image.load('../images/buttons/exit_btn.png').convert_alpha(), 234, 200)
        self.skinsButton = Button(pygame.image.load('../images/buttons/skins_btn.png').convert_alpha(), 234, 300)

    def run(self):
        """
        Run the menu.
        """
        if self.testing and self.test == 'menu':
            return 'Menu is running'
        if self.testing and self.test != 'menu':
            self.level = Level(self.display, self.skin, self.testing, self.test)
            return self.level.run()
        if self.startButton.update(self.display) and not self.start and not self.skinClick:
            self.start = True
            self.level = Level(self.display, self.skin)
        elif self.exitButton.update(self.display) and not self.start and not self.skinClick:
            pygame.quit()
        elif self.skinsButton.update(self.display) and not self.start and not self.skinClick:
            self.skinClick = True
        elif self.start and not self.skinClick:
            self.display.fill('black')
            self.level.run()
        elif self.skinClick and not self.start:
            self.display.fill((113, 116, 168))
            self.skinShop.run()
            if self.skinShop.getClicked():
                self.skin = self.skinShop.getSelected()
                self.skinClick = False
                self.start = True
                self.level = Level(self.display, self.skin)
        if self.level and self.level.win:
            self.win = True


class ShowCase(AnimatedTile, Button):
    """
    A button that displays an animated tile and returns the name of the selected skin when clicked.
    """

    def __init__(self, size, x, y, title):
        """
        Initialize the button.

        Args:
            size (int): The size of the button.
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            title (str): The title of the skin.
        """
        AnimatedTile.__init__(self, size, x, y, '../images/pacman/' + title)
        Button.__init__(self, self.image, x, y)
        self.name = title
        self.clicked = False
        self.rect = self.image.get_rect(topleft=(x, y))
        self.selected = False

    def animation(self):
        """
        Animate the tile.
        """
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]
        self.image = pygame.transform.scale(self.image, (tile_size * 2, tile_size * 2))

    def click(self):
        """
        Handle the click event.

        Args:
            screen (pygame.Surface): The surface where the button will be displayed.

        Returns:
            str: The name of the selected skin.
        """
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                self.selected = True
        return self.name


class Skins:
    """A class for managing and displaying the available skins in the Pac-Man game."""

    def __init__(self, surface):
        """
        Initialize the Skins instance.

        Args:
            surface: A Pygame surface object representing the display surface.
        """
        self.display = surface
        self.clicked = False
        x = tile_size * 4
        y = tile_size * 4
        self.selected = 'original'
        self.skins = pygame.sprite.Group()
        for skins in next(os.walk('../images/pacman/'))[1]:
            sprite = ShowCase(tile_size, x, y, skins)
            x += tile_size * 4
            self.skins.add(sprite)

    def drawGroup(self):
        """
        Draw the available skins to the display surface and handle any click events.

        Updates the selected skin if a new skin is clicked.
        """
        for sprite in self.skins.sprites():
            selection = sprite.click()
            if selection:
                self.selected = selection
            if sprite.clicked:
                self.clicked = True

    def getSelected(self):
        """
        Get the currently selected skin.

        Returns:
            A string representing the name of the currently selected skin.
        """
        return self.selected

    def getClicked(self):
        """
        Get whether a skin has been clicked.

        Returns:
            A boolean value representing whether a skin has been clicked.
        """
        return self.clicked

    def run(self):
        """
        Update and draw the skins to the display surface.

        Returns:
            None
        """
        self.drawGroup()
        self.skins.update()
        self.skins.draw(self.display)
