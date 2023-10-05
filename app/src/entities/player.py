"""
This module defines a Player class used in a game.
"""

import pygame
from app.src.settings.tiles import AnimatedTile


class Player(AnimatedTile):
    """
    This class represents a player character in the game.
    """
    def __init__(self, size, x, y, skin):
        """
        Constructs a new Player object.

        Args:
            size (tuple): The size of the player sprite.
            x (int): The initial x-coordinate of the player.
            y (int): The initial y-coordinate of the player.
            skin (str): The filename of the player sprite.
        """
        super().__init__(size, x, y, '../images/pacman/' + skin)
        self.origin_x = x
        self.origin_y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.nextMove = None
        self.possibleMoves = [1, 1, 1, 1]
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1

    def reverseImage(self):
        """
        Reverses the player sprite image if the player is moving to the left or up.
        """
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.direction.y > 0:
            self.image = pygame.transform.rotate(self.image, -90)
        if self.direction.y < 0:
            self.image = pygame.transform.rotate(self.image, 90)

    def move(self):
        """
        Handles the movement of the player based on the input keys.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.nextMove = 'left'
        elif keys[pygame.K_RIGHT]:
            self.nextMove = 'right'
        elif keys[pygame.K_UP]:
            self.nextMove = 'up'
        elif keys[pygame.K_DOWN]:
            self.nextMove = 'down'

        if self.possibleMoves[0] and self.nextMove == 'up':
            self.direction.y = -1
            self.direction.x = 0
        elif self.possibleMoves[1] and self.nextMove == 'right':
            self.direction.x = 1
            self.direction.y = 0
        elif self.possibleMoves[2] and self.nextMove == 'down':
            self.direction.y = 1
            self.direction.x = 0
        elif self.possibleMoves[3] and self.nextMove == 'left':
            self.direction.x = -1
            self.direction.y = 0

    def update(self):
        """
        Updates the state of the player sprite.
        """
        self.move()
        self.animation()
        self.reverseImage()
