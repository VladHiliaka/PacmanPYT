"""This module contains unit tests for the game functionality."""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.src.game import main

def test_menu():
    """
    Test the 'menu' functionality of the game.
    """
    response = main("menu")
    assert response == 'Menu is running'


def test_start():
    """
    Test the 'start' functionality of the game.
    """
    response = main("start")
    assert response == 'Game started'


def test_collision():
    """
    Test the collision detection functionality of the game.
    """
    response = main("collision")
    assert response != []


def test_coin_collision():
    """
    Test the coin collision functionality of the game.
    """
    response = main("score")
    assert response == 1


def test_ghost_collision():
    """
    Test the ghost collision functionality of the game.
    """
    response = main("ghost_collision")
    assert response is False


def test_basic_powerup():
    """
    Test the basic powerup collision functionality of the game.
    """
    response = main("powerup_collision")
    assert response is True
