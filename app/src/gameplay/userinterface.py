"""
This module contains the UI class that displays the coin and coin amount on the pygame surface.
"""

import pygame

from app.src.settings.settings import tile_size


class UI:
    """
    This class manages the UI of the game.
    """

    def __init__(self, surface):
        """
        Initializes the UI class.

        Args:
            surface (pygame.Surface): The surface to display the UI on.
        """
        self.display = surface

        # coin
        self.coin = pygame.image.load('../images/PacDot.png').convert_alpha()
        self.coin = pygame.transform.scale(self.coin, (tile_size * 2, tile_size * 2))
        self.coinRect = self.coin.get_rect(topleft=(0, 230))
        self.font = pygame.font.Font('../fonts/Retro Gaming.ttf', 20)

    def showCoin(self, amount):
        """
        Displays the coin image and coin amount on the pygame surface.

        Args:
            amount (int): The amount of coins to display.
        """
        self.display.blit(self.coin, self.coinRect)
        coinAmountSurface = self.font.render(str(amount), False, 'white')
        coinAmountRect = coinAmountSurface.get_rect(topleft=(50, 250))
        self.display.blit(coinAmountSurface, coinAmountRect)
