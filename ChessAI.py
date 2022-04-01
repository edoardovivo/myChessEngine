import random

pieceScores = {
    "K": 0,
    "Q": 10,
    "R": 5,
    "B": 3,
    "N": 3,
    "p": 1,
}

CHECKMATE = 1000
STALEMATE = 0


def findRandomMove(validMoves):
    i = random.randint(0, len(validMoves)-1)
    return validMoves[i]


def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentMove in opponentsMoves:
            gs.makeMove(opponentMove)
            if gs.checkMate:
                score = -turnMultiplier*CHECKMATE
            elif gs.staleMate:
                score = STALEMATE
            score = -turnMultiplier*scoreMaterial(gs.board)
            if (score > opponentMaxScore):
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore :
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()

    
    
    return bestPlayerMove



'''
Score the game state based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] =='b':
                score -= pieceScores[square[1]]
    return score


