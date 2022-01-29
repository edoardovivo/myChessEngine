"""
Main driver file. Responsible for handling user input and displaying game state.
"""

from ChessEngine import GameState
import pygame as p
import os
#os.environ["SDL_VIDEODRIVER"] = "dummy"

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
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./images/{}.png".format( piece)), (SQ_SIZE, SQ_SIZE) )


"""
Main driver. This will handle user input and updating the graphics
"""
def main():
    p.init()
    print(os.getcwd())
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    load_images()
    running = True

    while running:
        for e in p.event.get():
            if e.type == 'QUIT':
                running = False
            draw_game_state(screen, gs)
            clock.tick(MAX_FPS)
            p.display.flip()

'''
Resppnsible for all the graphics within a current game state
'''
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


'''
Draw the squares on the board- The top left square is light
'''
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # If r+x is even, then light square, else dark
            rem = (r+c)%2
            color = colors[rem]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) 




'''
Draw the pieces on the board given the game state
'''
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()










