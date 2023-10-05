"""
tiles.py

This module contains classes for various tiles used in a game.

"""
import pygame
from app.src.settings.additional import importFolder


class Tile(pygame.sprite.Sprite):
    """
    A base class for tiles.

    Args:
        size (int): The size of the tile.
        x (int): The x-coordinate of the tile's position.
        y (int): The y-coordinate of the tile's position.

    Attributes:
        image (pygame.Surface): The image of the tile.
        rect (pygame.Rect): The rectangle representing the tile's position and size.

    """

    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))


class StaticTile(Tile):
    """
    A class for static tiles.

    Args:
        size (int): The size of the tile.
        x (int): The x-coordinate of the tile's position.
        y (int): The y-coordinate of the tile's position.
        surface (pygame.Surface): The image of the static tile.

    """

    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class AnimatedTile(Tile):
    """
    A class for animated tiles.

    Args:
        size (int): The size of the tile.
        x (int): The x-coordinate of the tile's position.
        y (int): The y-coordinate of the tile's position.
        path (str): The path to the folder containing the frames of the animation.

    Attributes:
        frames (List[pygame.Surface]): The list of frames of the animation.
        frameIndex (int): The index of the current frame.
    """

    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = importFolder(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]

    def animation(self):
        """
        Advances the animation to the next frame.

        """
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def update(self):
        """
        Updates the tile's image based on the current animation frame.

        """
        self.animation()


class Coin(StaticTile):
    """
    A class for coins.

    Args:
        size (int): The size of the coin.
        x (int): The x-coordinate of the coin's position.
        y (int): The y-coordinate of the coin's position.

    """

    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../images/PacDot.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))


class BasicPower(StaticTile):
    """
    A class for basic power tiles.

    Args:
        size (int): The size of the power tile.
        x (int): The x-coordinate of the power tile's position.
        y (int): The y-coordinate of the power tile's position.

    """

    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../images/PowerPellet.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))


class Cherry(StaticTile):
    """
    A class for cherry tiles.

    Args:
        size (int): The size of the cherry tile.
        x (int): The x-coordinate of the cherry tile's position.
        y (int): The y-coordinate of the cherry tile's position.

    """

    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../images/SimpleCherry.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))


class Speed(StaticTile):
    """
    A class for speed tiles.

    Args:
        size (int): The size of the speed tile.
        x (int): The x-coordinate of the speed tile's position.
        y (int): The y-coordinate of the speed tile's position.

    """

    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../images/speed.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))


class Shield(StaticTile):
    """
    A class for shield tiles.

    Args:
        size (int): The size of the shield tile.
        x (int): The x-coordinate of the shield tile's position.
        y (int): The y-coordinate of the shield tile's position.

    """

    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('../images/shield/0.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))


class Fake(Tile):
    """
    A class for fake tiles.

    Args:
        size (int): The size of the fake tile.
        x (int): The x-coordinate of the fake tile's position.
        y (int): The y-coordinate of the fake tile's position.
        origin (Tuple[int, int]): The coordinates of the original tile.

    Attributes:
        deviationX (int): The deviation in the x-coordinate from the original tile.
        deviationY (int): The deviation in the y-coordinate from the original tile.
        location (str): The location of the fake tile relative to the original tile.
    """

    def __init__(self, size, x, y, origin):
        super().__init__(size, x, y)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.deviationX = origin[0] - x
        self.deviationY = origin[1] - y
        if self.deviationY < 0:
            self.location = 'up'
        elif self.deviationY > 0:
            self.location = 'down'
        elif self.deviationX < 0:
            self.location = 'left'
        elif self.deviationX > 0:
            self.location = 'right'
