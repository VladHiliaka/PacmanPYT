"""
Enemy module contains classes for the enemies in the game
"""
import csv
import time
from random import choice

import pygame


from app.src.settings.settings import tile_size, numberOfTileX, numberOfTileY
from app.src.settings.tiles import AnimatedTile, StaticTile


class Ghost(AnimatedTile):
    """
    A ghost enemy that moves randomly around the screen
    """

    def __init__(self, size, x, y):
        """
        Constructor for the Ghost class

        :param size: The size of the tile
        :param x: The x position of the Ghost
        :param y: The y position of the Ghost
        """
        super().__init__(size, x, y, '../images/ghost')
        self.origin_x = x
        self.origin_y = y
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.possibleMoves = [1, 1, 1, 1]
        self.direction = pygame.math.Vector2(0, 0)
        self.previousWay = 2
        self.speed = 2

    def move(self):
        """
        Moves the Ghost in a random direction
        """
        if self.rect.x > 605:
            self.rect.x = -25
        elif self.rect.x < -25:
            self.rect.x = 605

        if not self.rect.x % 32 and not self.rect.y % 32:
            indices = [i for i in range(len(self.possibleMoves)) if self.possibleMoves[i] == 1]
            if self.rect.y != 320 or not 256 <= self.rect.x <= 352:
                if (self.previousWay + 2) % 4 in indices:
                    indices.remove((self.previousWay + 2) % 4)
                if not indices:
                    indices.append(4)
            randomIndex = choice(indices)
            self.previousWay = randomIndex
            if randomIndex == 0:
                self.direction.y = -1
                self.direction.x = 0
            elif randomIndex == 1:
                self.direction.x = 1
                self.direction.y = 0
            elif randomIndex == 2:
                self.direction.y = 1
                self.direction.x = 0
            elif randomIndex == 3:
                self.direction.x = -1
                self.direction.y = 0

    def update(self):
        """
        Updates the Ghost's position
        """
        self.move()


class GhostBoss(StaticTile):
    """
    A Ghost boss enemy that spawns Ghost enemies
    """

    def __init__(self, size, x, y):
        """
        Constructor for the GhostBoss class

        :param size: The size of the tile
        :param x: The x position of the GhostBoss
        :param y: The y position of the GhostBoss
        """
        self.origin_x = x
        self.origin_y = y
        super().__init__(size, x, y, pygame.image.load('../images/GhostBoss/0.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.lives = 4

    def spawnEnemy(self, group):
        """
        Spawns a Ghost enemy

        :param group: The group to add the Ghost to
        """
        sprite = Ghost(tile_size, 288, 320)
        group.add(sprite)

    def update(self):
        """
        Updates the GhostBoss's position
        """
        if self.lives == 3:
            self.rect = self.image.get_rect(topleft=((numberOfTileX - 2) * tile_size, self.origin_y))
        elif self.lives == 2:
            self.rect = self.image.get_rect(topleft=((numberOfTileX - 2) * tile_size, (numberOfTileY - 2) * tile_size))
        elif self.lives == 1:
            self.rect = self.image.get_rect(topleft=(self.origin_x, (numberOfTileY - 2) * tile_size))


class Devil(StaticTile):
    """
    A Devil boss enemy that spawns fireballs
    """

    def __init__(self, size, x, y):
        """
        Constructor for the Devil class

        :param size: The size of the tile
        :param x: The x position of the GhostBoss
        :param y: The y position of the GhostBoss
        """
        self.origin_x = x
        self.origin_y = y
        super().__init__(size, x, y, pygame.image.load('../images/devil/0.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.impact = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()

    def castFireball(self, playerX, playerY):
        """Cast fireball based on player position"""
        self.impact.add(ImpactPoint(tile_size, playerX, playerY))

    def update(self, surface):
        """Updates the Devil"""
        self.impact.draw(surface)
        self.impact.update(self.fireballs)
        self.fireballs.update()
        self.fireballs.draw(surface)


class ImpactPoint(StaticTile):
    """A point of impact that does not harm the player but turns into a fireball"""
    def __init__(self, size, playerX, playerY):
        """
        Constructor for the Devil class

        :param size: The size of the tile
        :param playerX: The x position of the player
        :param playerY: The y position of the player
        """
        self.posX = None
        self.posY = None
        self.choosePosition(playerX, playerY)
        super().__init__(size, self.posX, self.posY,
                         pygame.image.load('../images/fireball/caution.png').convert_alpha())
        self.rect = self.image.get_rect(topleft=(self.posX, self.posY))
        self.time = time.time()

    def choosePosition(self, player_x, player_y):
        """Choose nearest point based on random and player position"""
        with open('../levels/start_level/start_level_walls.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        player_col = player_x // tile_size
        player_row = player_y // tile_size

        min_col = max(0, player_col - 2)
        max_col = min(len(rows[0]) - 1, player_col + 2)
        min_row = max(0, player_row - 2)
        max_row = min(len(rows) - 1, player_row + 2)

        open_spaces = []
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if rows[row][col] == '-1':
                    open_spaces.append((col, row))
        impactPos = tuple(choice(open_spaces))
        self.posX = impactPos[0] * tile_size
        self.posY = impactPos[1] * tile_size

    def update(self, group):
        """Update impact"""
        if time.time() - self.time > 1:
            group.add(Fireball(self.posX, self.posY))
            self.kill()

class Fireball(StaticTile):
    """
    A fireball that randomly appears on the screen
    """
    def __init__(self, x, y):
        """Constructor for the fireball class"""
        super().__init__(tile_size, x, y,
                         pygame.image.load('../images/fireball/fireball.png').convert_alpha())
        self.time = time.time()

    def update(self):
        """Update fireball"""
        if time.time() - self.time > 0.5:
            self.kill()
