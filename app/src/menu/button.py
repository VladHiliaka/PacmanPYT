"""
This module provides a Button class for creating clickable buttons with images using the Pygame library.

Usage:
    To create a new button, instantiate the Button class and provide the image and position as arguments.
    Then, call the update() method in a Pygame loop to update the button's image and position on the screen.
    Finally, check the clicked attribute to determine if the button was clicked.
"""
import pygame


class Button:
    """
    A clickable button with an image and a position on the screen.

    Attributes:
        image (pygame.Surface): The image to be displayed on the button.
        rect (pygame.Rect): The rectangular area occupied by the button on the screen.
        clicked (bool): Whether the button has been clicked.

    """

    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(image, (139, 62.5))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def update(self, screen):
        """
        Updates the button's image and position on the screen.
        """
        action = False
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action
