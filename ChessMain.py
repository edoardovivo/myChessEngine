"""
Main driver file. Responsible for handling user input and displaying game state.
"""

from matplotlib import colors
import ChessEngine
import pygame as p
import os

#os.environ["SDL_VIDEODRIVER"] = "dummy"

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 100
IMAGES = {}
colors = [p.Color("white"), p.Color("gray")]




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
    animate = False
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == 'QUIT':
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
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
                        
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                print(move.getChessNotation())
                                
                                
                                sqSelected = ()
                                playerClicks = []
                                animate = True
                    if not moveMade:
                        playerClicks = [sqSelected]
                
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo move
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reset game
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

            
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            print("WhiteToMove: " + str(gs.whiteToMove) )
            print("In Check: " + str(gs.inCheck) )
                
                #else:
                #    sqSelected = ()
                #    playerClicks = []
                #if moveMade:
                #    validMoves = gs.getValidMoves()
                #    moveMade = False


        draw_game_state(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate!')
            else:
                drawText(screen, 'White wins by checkmate!')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate!')

        clock.tick(MAX_FPS)
        p.display.flip()


'''
Highlight square selected and possible moves
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #higlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))



'''
Resppnsible for all the graphics within a current game state
'''
def draw_game_state(screen, gs, validMoves, sqSelected):
    draw_board(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    draw_pieces(screen, gs.board)


'''
Draw the squares on the board- The top left square is light
'''
def draw_board(screen):
    global colors
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


'''
Animating of the pieces
'''
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of coordinates that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        draw_board(screen)
        draw_pieces(screen, board)
        #erase piece moved from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    font = p.font.SysFont('Helvitica', 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))

    





if __name__ == "__main__":
    main()










