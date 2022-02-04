"""
Main driver file. Responsible for handling user input and displaying game state.
"""

import ChessEngine
import pygame as p
import os

#os.environ["SDL_VIDEODRIVER"] = "dummy"

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 100
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
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable
    load_images()
    running = True
    sqSelected = ()
    playerClicks = [] #At most two sqSelected tuples
    while running:
        for e in p.event.get():
            if e.type == 'QUIT':
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo move
                    gs.undoMove()
                    moveMade = True
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() 
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                #print(row, col)
                if sqSelected == (row, col): #User click the same sq twice
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                # was that the user second click? if so, move
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = ()
                        playerClicks = []
                    if moveMade:
                        validMoves = gs.getValidMoves()
                        moveMade = False



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










