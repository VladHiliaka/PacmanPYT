"""
This module defines the Screen class, which displays a title and description for a boss level in a Pygame window.
"""

import pygame

class Screen:
    """
    The Screen class represents the screen that displays the title and description for a boss level.

    Args:
        bossLevel (int): The level of the boss to display. Can be 1 or 2.

    Attributes:
        titleFont (pygame.font.Font): The font used for the title.
        descriptionFont (pygame.font.Font): The font used for the description.
        title (pygame.Surface): The rendered title text.
        titleRect (pygame.Rect): The rectangle that defines the position and size of the title text.
        description (pygame.Surface): The rendered description text.
        descriptionRect (pygame.Rect): The rectangle that defines the position and size of the description text.
    """

    def __init__(self, bossLevel, score: int = None):
        """Initializes the Screen object with the given boss level."""
        self.titleFont = pygame.font.Font('../fonts/Retro Gaming.ttf', 30)
        self.descriptionFont = pygame.font.Font('../fonts/Retro Gaming.ttf', 20)
        if bossLevel == 1:
            self.title = self.titleFont.render('The Spiritual King', False, 'white')
            self.titleRect = self.title.get_rect(topleft=(160, 220))
            self.description = self.descriptionFont.render('Use power-ups to kill the boss', False, 'white')
            self.descriptionRect = self.description.get_rect(topleft=(130, 320))
        elif bossLevel == 2:
            self.title = self.titleFont.render('The Devil', False, 'white')
            self.titleRect = self.title.get_rect(topleft=(230, 220))
            self.description = self.descriptionFont.render("Get close to the boss to kill him", False, 'white')
            self.descriptionRect = self.description.get_rect(topleft=(130, 320))
        elif bossLevel == 3:
            self.title = self.titleFont.render('WIN', False, 'white')
            self.description = self.titleFont.render(f'Score: {score}', False, 'white')
            self.titleRect = self.title.get_rect(topleft=(270, 220))
            self.descriptionRect = self.description.get_rect(topleft=(220, 270))


    def run(self, surface):
        """
        Displays the title and description on the given surface.

        Args:
            surface (pygame.Surface): The surface to display the title and description on.
        """
        surface.fill((113, 116, 168))
        surface.blit(self.title, self.titleRect)
        if self.description:
            surface.blit(self.description, self.descriptionRect)
