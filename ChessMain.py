"""
Main driver file. Responsible for handling user input and displaying game state.
"""

from myChessEngine import ChessEngine
import pygame as p

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

"""
Initialize a global dictionary of images. Called exactly once in the main
"""
def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    IMAGES = {piece: p.transform.scale(p.image.load("images/{}.png".format(piece)), (SQ_SIZE, SQ_SIZE) ) for piece in pieces}


"""
Main driver. This will handle user input and updating the graphics
"""
def main():
    p.init()
    

