import random
import numpy as np

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
DEPTH = 4
nextMove = None


def findRandomMove(validMoves):
    i = random.randint(0, len(validMoves)-1)
    return validMoves[i]


def findBestMove(gs, validMoves):
    '''
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
    '''
    
    maximizingPlayer = gs.whiteToMove
    random.shuffle(validMoves)
    bestScore = minimax(gs, validMoves, DEPTH, -np.inf, np.inf, maximizingPlayer)

    
    
    return nextMove


'''
Minimax algorithm
'''
def minimax(gs, validMoves, depth, alpha, beta, maximizingPlayer):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if maximizingPlayer:
        maxEval = -np.inf
        for playerMove in validMoves: #for each child of position
            gs.makeMove(playerMove)
            opponentsMoves = gs.getValidMoves()
            random.shuffle(opponentsMoves)
            evaluation = minimax(gs, opponentsMoves, depth - 1,alpha, beta, False)
            alpha = max(alpha, evaluation)
            if evaluation > maxEval:
                maxEval = evaluation
                if depth == DEPTH:
                    nextMove = playerMove
            gs.undoMove()
            if beta <= alpha:
                break
            
        return maxEval
    else:
        minEval = +np.inf
        for playerMove in validMoves: #for each child of position
            gs.makeMove(playerMove)
            opponentsMoves = gs.getValidMoves()
            random.shuffle(opponentsMoves)
            evaluation = minimax(gs, opponentsMoves, depth - 1, alpha, beta, True)
            beta = min(beta, evaluation)
            if evaluation < minEval:
                minEval = evaluation
                if depth == DEPTH:
                    nextMove = playerMove
            gs.undoMove()
            if beta <= alpha:
                break
            
        return minEval



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


