"""This module contains the Level class, which represents a level in the game."""
import time

from app.src.settings.tiles import *
from app.src.settings.additional import csv_layout, slicingImage, importFolder
from app.src.settings.settings import startLevel, tile_size
from app.src.entities.enemy import Ghost, GhostBoss, Devil
from app.src.entities.player import Player
from app.src.gameplay.userinterface import UI
from app.src.menu.screensplash import Screen


class Level:
    """
    This class represents a level in the game.
    """

    def __init__(self, surface, skin, testing: bool = False, test: str = None):
        self.testing = testing
        self.test = test
        self.powerup_start_time = None
        self.bossScreenTimer = None
        self.surface = surface
        self.previousSkin = None
        self.skin = skin
        self.invincible = None
        self.invincible_start_time = None
        self.coins = 0
        self.win = False
        self.spawnRate = 5
        self.fireballSpawnRate = 0.5
        self.fireballTimer = None
        self.spawnTimer = time.time()
        self.speedupTimer = None
        self.speedup = False
        self.alive = True
        self.boss = 0
        self.godMode = False
        self.godMode_start_time = None
        self.font = pygame.font.Font('../fonts/Retro Gaming.ttf', 30)
        self.UI = UI(self.surface)

        player_layout = csv_layout(startLevel['pacman'])
        self.player = pygame.sprite.GroupSingle()
        self.fakePlayer = pygame.sprite.Group()
        self.playerSetup(player_layout)

        self.walls_layout = csv_layout(startLevel['walls'])
        self.walls_sprites = self.create_tile_group(self.walls_layout, 'walls')

        coins_layout = csv_layout(startLevel['coin'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coin')

        self.basic_powerup_layout = csv_layout(startLevel['BasicPower'])
        self.basic_powerup_sprites = self.create_tile_group(self.basic_powerup_layout, 'BasicPower')

        self.cherry_layout = csv_layout(startLevel['cherry'])
        self.cherry_sprites = self.create_tile_group(self.cherry_layout, 'cherry')

        ghost_layout = csv_layout(startLevel['ghost'])
        self.ghost_sprites = self.create_tile_group(ghost_layout, 'ghost')

        speed_layout = csv_layout(startLevel['speed'])
        self.speed_sprites = self.create_tile_group(speed_layout, 'speed')

        shield_layout = csv_layout(startLevel['shield'])
        self.shield_sprites = self.create_tile_group(shield_layout, 'shield')

        bossGhost_layout = csv_layout(startLevel['bossGhost'])
        self.bossGhost = pygame.sprite.GroupSingle()
        self.bossGhostSetup(bossGhost_layout)

        self.devil = pygame.sprite.GroupSingle()
        self.devil.add(Devil(tile_size, 288, 320))

    def playerSetup(self, layout):
        """Set up the player."""
        for indexY, row in enumerate(layout):
            for indexX, value in enumerate(row):
                x = indexX * tile_size
                y = indexY * tile_size
                if value != '-1':
                    sprite = Player(tile_size, x, y, self.skin)
                    self.player.add(sprite)
                    self.fakePlayer.add(Fake(tile_size, x, y - tile_size, sprite.rect))
                    self.fakePlayer.add(Fake(tile_size, x, y + tile_size, sprite.rect))
                    self.fakePlayer.add(Fake(tile_size, x - tile_size, y, sprite.rect))
                    self.fakePlayer.add(Fake(tile_size, x + tile_size, y, sprite.rect))

    def bossGhostSetup(self, layout):
        """Set up the Ghost Boss."""
        for indexY, row in enumerate(layout):
            for indexX, value in enumerate(row):
                x = indexX * tile_size
                y = indexY * tile_size
                if value != '-1':
                    sprite = GhostBoss(tile_size, x, y)
                    self.bossGhost.add(sprite)

    def wallCollision(self):
        """ Check for collisions between player and walls """
        player = self.player.sprite
        if player.rect.x > 605:
            player.rect.x = -25
        elif player.rect.x < -25:
            player.rect.x = 605
        player.rect.x += player.direction.x * player.speed
        player.rect.y += player.direction.y * player.speed
        next_pos = player.rect.move(player.direction.x * player.speed, player.direction.y * player.speed)
        for wall in self.walls_sprites.sprites():
            if wall.rect.clipline(player.rect.center, next_pos.center):
                player.rect.x -= player.direction.x * player.speed
                player.rect.y -= player.direction.y * player.speed
                break
        else:
            player.rect = next_pos
        for sprite in self.walls_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top

    def wallCollisionGhosts(self):
        """ Check for collisions between ghost and walls """
        for sprite in self.ghost_sprites.sprites():
            sprite.rect.x += sprite.direction.x * sprite.speed
            sprite.rect.y += sprite.direction.y * sprite.speed
            for wall in self.walls_sprites.sprites():
                if wall.rect.colliderect(sprite.rect):
                    if sprite.direction.x < 0:
                        sprite.rect.left = wall.rect.right
                    elif sprite.direction.x > 0:
                        sprite.rect.right = wall.rect.left
                    elif sprite.direction.y < 0:
                        sprite.rect.top = wall.rect.bottom
                    elif sprite.direction.y > 0:
                        sprite.rect.bottom = wall.rect.top

    def fakeMove(self):
        """Move rectangle around player"""
        for sprite in self.fakePlayer.sprites():
            sprite.rect.x = self.player.sprite.rect.x + sprite.deviationX
            sprite.rect.y = self.player.sprite.rect.y + sprite.deviationY

    def fakeCollisions(self):
        """ Check for collisions between rectangles around player and walls """
        collisions = pygame.sprite.groupcollide(self.fakePlayer, self.walls_sprites, False, False)
        for fake in self.fakePlayer.sprites():
            if fake in collisions:
                if fake.location == 'up':
                    self.player.sprite.possibleMoves[0] = 0
                elif fake.location == 'right':
                    self.player.sprite.possibleMoves[1] = 0
                elif fake.location == 'down':
                    self.player.sprite.possibleMoves[2] = 0
                elif fake.location == 'left':
                    self.player.sprite.possibleMoves[3] = 0
            else:
                if fake.location == 'up':
                    self.player.sprite.possibleMoves[0] = 1
                elif fake.location == 'right':
                    self.player.sprite.possibleMoves[1] = 1
                elif fake.location == 'down':
                    self.player.sprite.possibleMoves[2] = 1
                elif fake.location == 'left':
                    self.player.sprite.possibleMoves[3] = 1

    def fakeCollisionsGhost(self):
        """Check for possible moves for a ghost"""
        for sprite in self.ghost_sprites.sprites():
            cal = sprite.rect.x // 32
            row = sprite.rect.y // 32
            if 0 < sprite.rect.x < 576:
                if not sprite.rect.x % 32 and not sprite.rect.y % 32:
                    if self.walls_layout[row + 1][cal] == '-1':
                        sprite.possibleMoves[2] = 1
                    else:
                        sprite.possibleMoves[2] = 0
                    if self.walls_layout[row - 1][cal] == '-1':
                        sprite.possibleMoves[0] = 1
                    else:
                        sprite.possibleMoves[0] = 0
                    if self.walls_layout[row][cal + 1] == '-1':
                        sprite.possibleMoves[1] = 1
                    else:
                        sprite.possibleMoves[1] = 0
                    if self.walls_layout[row][cal - 1] == '-1':
                        sprite.possibleMoves[3] = 1
                    else:
                        sprite.possibleMoves[3] = 0

    def enemyCollision(self):
        """Check for collisions between ghost and player"""
        collide = pygame.sprite.spritecollide(self.player.sprite, self.ghost_sprites, False)
        if collide and not self.godMode:
            self.alive = False
        elif collide and self.godMode:
            self.coins += 50
            for ghosts in collide:
                ghosts.rect.x = 256
                ghosts.rect.y = 320

    def deadOrNot(self):
        """Check if player is alive"""
        if not self.alive:
            self.win = True
            self.coins_sprites.empty()
            self.surface.fill((113, 116, 168))
            TheEnd = self.font.render('BUSTED', False, 'white')
            Coins = self.font.render(f'Score: {self.coins}', False, 'white')
            CoinsRect = Coins.get_rect(topleft=(230, 270))
            TheEndRect = TheEnd.get_rect(topleft=(250, 320))
            self.surface.blit(TheEnd, TheEndRect)
            self.surface.blit(Coins, CoinsRect)

    def coinCollision(self):
        """Check for collisions between player and coins"""
        if not self.coins_sprites.sprites() and not self.boss:
            self.boss = 1
            self.bossScreenTimer = time.time()
        collide = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if collide:
            self.coins += 1

    def cherryCollision(self):
        """Check for collisions between player and cherry"""
        collide = pygame.sprite.spritecollide(self.player.sprite, self.cherry_sprites, True)
        if collide:
            self.coins += 50

    def powerUp(self):
        """Check for collisions between player and powerup"""
        collide = pygame.sprite.spritecollide(self.player.sprite, self.basic_powerup_sprites, True)
        if collide:
            self.godMode = True
            self.previousSkin = importFolder('../images/pacman/' + self.skin)
            self.player.sprite.frames = importFolder('../images/PowerPelletEffect')
            self.powerup_start_time = time.time()

    def firstBossCollision(self):
        """Check for collisions between player and Ghost boss"""
        if self.player.sprite.rect.colliderect(self.bossGhost.sprite.rect) and self.godMode:
            if not self.bossGhost.sprite.lives:
                self.coins += 100
                self.bossGhost.sprite.kill()
                self.boss = 2
                self.bossScreenTimer = time.time()
            else:
                self.bossGhost.sprite.lives -= 1
        elif self.player.sprite.rect.colliderect(self.bossGhost.sprite.rect) and not self.godMode:
            self.alive = False

    def fireballCollision(self):
        """Check for collisions between player and fireball"""
        collide = pygame.sprite.spritecollide(self.player.sprite, self.devil.sprite.fireballs, True)
        if collide and not self.invincible:
            self.alive = False

    def create_tile_group(self, layout, sprite_type):
        """Create a group of tiles"""
        sprite_group = pygame.sprite.Group()
        for indexY, row in enumerate(layout):
            for indexX, value in enumerate(row):
                if value != '-1':
                    x = indexX * tile_size
                    y = indexY * tile_size
                    if sprite_type == 'walls':
                        walls_tile_list = slicingImage('../images/tiles set.png')
                        tileSurface = walls_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tileSurface)
                    elif sprite_type == 'coin':
                        sprite = Coin(tile_size, x, y)
                    elif sprite_type == 'BasicPower':
                        sprite = BasicPower(tile_size, x, y)
                    elif sprite_type == 'cherry':
                        sprite = Cherry(tile_size, x, y)
                    elif sprite_type == 'ghost':
                        sprite = Ghost(tile_size, x, y)
                    elif sprite_type == 'speed':
                        sprite = Speed(tile_size, x, y)
                    elif sprite_type == 'shield':
                        sprite = Shield(tile_size, x, y)
                    sprite_group.add(sprite)
        return sprite_group

    def secondBossCollision(self):
        """Check for collisions between player and Devil boss"""
        if self.player.sprite.rect.colliderect(self.devil.sprite.rect) and self.godMode:
            self.coins += 100
            self.boss = 3
        elif self.player.sprite.rect.colliderect(self.devil.sprite.rect) and not self.godMode and not self.invincible:
            self.alive = False

    def speedCollision(self):
        """Check for collisions between player and speed boost"""
        collide = pygame.sprite.spritecollide(self.player.sprite, self.speed_sprites, True)
        if collide:
            self.speedup = True
            self.player.sprite.speed = 2
            self.speedupTimer = time.time()

    def shieldCollision(self):
        """Check for collisions between player and powerup"""
        collide = pygame.sprite.spritecollide(self.player.sprite, self.shield_sprites, True)
        if collide:
            self.invincible = True
            self.previousSkin = importFolder('../images/pacman/' + self.skin)
            self.player.sprite.frames = importFolder('../images/shield')
            self.invincible_start_time = time.time()
    def firstBossUpdate(self):
        """Updating the first boss"""
        self.bossGhost.update()
        self.bossGhost.draw(self.surface)
        self.firstBossCollision()
        if time.time() - self.spawnTimer > self.spawnRate:
            self.spawnTimer = time.time()
            self.bossGhost.sprite.spawnEnemy(self.ghost_sprites)
    def firstBossScreen(self):
        """Updating the screen of first boss"""
        self.player.sprite.direction = pygame.math.Vector2(0, 0)
        self.player.sprite.rect.x = self.player.sprite.origin_x
        self.player.sprite.rect.y = self.player.sprite.origin_y
        self.ghost_sprites.empty()
        screen = Screen(self.boss)
        screen.run(self.surface)
        self.cherry_sprites.empty()
        self.basic_powerup_sprites = self.create_tile_group(self.basic_powerup_layout, 'BasicPower')
    def secondBossUpdate(self):
        """Updating the second boss"""
        self.shield_sprites.draw(self.surface)
        self.speed_sprites.draw(self.surface)
        self.devil.update(self.surface)
        self.devil.draw(self.surface)
        self.speedCollision()
        self.shieldCollision()
        if self.invincible and time.time() - self.invincible_start_time > 5:
            self.invincible = False
            self.player.sprite.frames = self.previousSkin
        if self.speedup and time.time() - self.speedupTimer > 5:
            self.speedup = False
            self.player.sprite.speed = 1
        if time.time() - self.fireballTimer > self.fireballSpawnRate:
            self.devil.sprite.castFireball(self.player.sprite.rect.x, self.player.sprite.rect.y)
            self.fireballTimer = time.time()
        self.fireballCollision()
        self.secondBossCollision()
    def secondBossScreen(self):
        """Updating the screen of second boss"""
        self.fireballTimer = time.time()
        self.player.sprite.direction = pygame.math.Vector2(0, 0)
        self.player.sprite.rect.x = self.player.sprite.origin_x
        self.player.sprite.rect.y = self.player.sprite.origin_y
        self.bossGhost.empty()
        self.ghost_sprites.empty()
        self.cherry_sprites.empty()
        self.basic_powerup_sprites.empty()
        self.basic_powerup_sprites = self.create_tile_group(self.cherry_layout, 'BasicPower')
        screen = Screen(self.boss)
        screen.run(self.surface)
    def run(self):
        """Run the level"""
        if self.testing and self.test == 'start':
            return 'Game started'
        if self.godMode and time.time() - self.powerup_start_time > 5:
            self.godMode = False
            self.player.sprite.frames = self.previousSkin
        self.powerUp()
        self.fakeMove()
        self.fakeCollisions()
        self.player.update()
        if self.testing:
            match self.test:
                case 'collision':
                    self.coins_sprites.add(Coin(tile_size, self.player.sprite.origin_x, self.player.sprite.origin_y))
                    return pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
                case 'score':
                    self.coins_sprites.add(Coin(tile_size, self.player.sprite.origin_x, self.player.sprite.origin_y))
                    self.coinCollision()
                    return self.coins
                case 'ghost_collision':
                    self.ghost_sprites.add(Ghost(tile_size, self.player.sprite.origin_x, self.player.sprite.origin_y))
                    self.ghost_sprites.draw(self.surface)
                    self.ghost_sprites.update()
                    self.enemyCollision()
                    return self.alive
                case 'powerup_collision':
                    self.basic_powerup_sprites.add(
                        BasicPower(tile_size, self.player.sprite.origin_x, self.player.sprite.origin_y))
                    self.basic_powerup_sprites.draw(self.surface)
                    self.powerUp()
                    return self.godMode
        self.wallCollision()
        self.coinCollision()
        self.cherryCollision()
        self.fakeCollisionsGhost()
        self.fakePlayer.draw(self.surface)
        self.walls_sprites.draw(self.surface)
        self.coins_sprites.draw(self.surface)
        self.basic_powerup_sprites.draw(self.surface)
        self.cherry_sprites.draw(self.surface)
        self.player.draw(self.surface)
        self.ghost_sprites.draw(self.surface)
        self.ghost_sprites.update()
        self.enemyCollision()
        self.wallCollisionGhosts()
        self.UI.showCoin(self.coins)
        if self.boss == 1 and time.time() - self.bossScreenTimer > 2:
            self.firstBossUpdate()
        elif self.boss == 1 and time.time() - self.bossScreenTimer < 2:
            self.firstBossScreen()
        elif self.boss == 2 and time.time() - self.bossScreenTimer > 2:
            self.secondBossUpdate()
        elif self.boss == 2 and time.time() - self.bossScreenTimer < 2:
            self.secondBossScreen()
        elif self.boss == 3:
            self.win = True
            self.devil.empty()
            screen = Screen(self.boss, self.coins)
            screen.run(self.surface)
        self.deadOrNot()
