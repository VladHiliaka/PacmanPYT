"""
The module represents the configuration settings for a game level.

The module contains the following variables:

    tile_size: An integer representing the size of a single tile in pixels.
    numberOfTileX: An integer representing the number of tiles in the X direction.
    numberOfTileY: An integer representing the number of tiles in the Y direction.
    screen_height: An integer representing the height of the game screen in pixels, calculated by multiplying numberOfTileY with tile_size.
    screen_width: An integer representing the width of the game screen in pixels, calculated by multiplying numberOfTileX with tile_size.

The module also includes the startLevel dictionary, which maps various elements of the start level to their corresponding
file paths. The keys in the dictionary represent the elements, and the values represent the file paths.
"""

tile_size = 32

numberOfTileX = 19
numberOfTileY = 22
screen_height = numberOfTileY * tile_size
screen_width = numberOfTileX * tile_size

startLevel = {
    'cherry': '../levels/start_level/start_level_cherry.csv',
    'coin': '../levels/start_level/start_level_coins.csv',
    'BasicPower': '../levels/start_level/start_level_power_up.csv',
    'walls': '../levels/start_level/start_level_walls.csv',
    'ghost': '../levels/start_level/start_level_ghost.csv',
    'pacman': '../levels/start_level/start_level_pacman.csv',
    'bossGhost': '../levels/start_level/start_level_bossGhost.csv',
    'speed':  '../levels/start_level/start_level_speed.csv',
    'shield': '../levels/start_level/start_level_shield.csv',
}
