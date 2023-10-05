"""Module containing additional utility functions for the game."""

import os
from csv import reader

import pygame.image

from app.src.settings.settings import tile_size


def csv_layout(path):
    """Return the layout of the terrain from a CSV file.

    Args:
        path (str): The path to the CSV file.

    Returns:
        list: The layout of the terrain as a list of lists of strings.
    """
    terrain_map = []
    with open(path, encoding='utf-8') as map_file:
        level = reader(map_file, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def slicingImage(path):
    """Slice an image into tiles.

    Args:
        path (str): The path to the image file.

    Returns:
        list: The list of tiles as Pygame surfaces.
    """
    surface = pygame.image.load(path).convert_alpha()
    tile_size_x = int(surface.get_size()[0] / tile_size)
    tile_size_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []

    for row in range(tile_size_y):
        for col in range(tile_size_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles


def importFolder(path):
    """Import a folder of images as Pygame surfaces.

    Args:
        path (str): The path to the folder.

    Returns:
        list: The list of Pygame surfaces.
    """
    surface_list = []
    for _, __, files in os.walk(path):
        for file in files:
            full_path = os.path.join(path, file)
            image = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image)
    return surface_list
