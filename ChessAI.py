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


knightScores = [[-50,-40,-30,-30,-30,-30,-40,-50],
[-40,-20,  0,  0,  0,  0,-20,-40],
[-30,  0, 10, 15, 15, 10,  0,-30],
[-30,  5, 15, 20, 20, 15,  5,-30],
[-30,  0, 15, 20, 20, 15,  0,-30],
[-30,  5, 10, 15, 15, 10,  5,-30],
[-40,-20,  0,  5,  5,  0,-20,-40],
[-50,-40,-30,-30,-30,-30,-40,-50]]

bishopScores = [[-20,-10,-10,-10,-10,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5, 10, 10,  5,  0,-10,],
[-10,  5,  5, 10, 10,  5,  5,-10],
[-10,  0, 10, 10, 10, 10,  0,-10],
[-10, 10, 10, 10, 10, 10, 10,-10],
[-10,  5,  0,  0,  0,  0,  5,-10],
[-20,-10,-10,-10,-10,-10,-10,-20]]

rookScores = [[0,  0,  0,  0,  0,  0,  0,  0],
  [5, 10, 10, 10, 10, 10, 10,  5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
 [-5,  0,  0,  0,  0,  0,  0, -5],
  [0,  0,  0,  5,  5,  0,  0,  0]]


queenScores = [
[-20,-10,-10, -5, -5,-10,-10,-20],
[-10,  0,  0,  0,  0,  0,  0,-10],
[-10,  0,  5,  5,  5,  5,  0,-10],
[ -5,  0,  5,  5,  5,  5,  0, -5],
[  0,  0,  5,  5,  5,  5,  0, -5],
[-10,  5,  5,  5,  5,  5,  0,-10],
[-10,  0,  5,  0,  0,  0,  0,-10],
[-20,-10,-10, -5, -5,-10,-10,-20]]

kingScores = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-30,-40,-40,-50,-50,-40,-40,-30],
[-20,-30,-30,-40,-40,-30,-30,-20],
[-10,-20,-20,-20,-20,-20,-20,-10],
[ 20, 20,  0,  0,  0,  0, 20, 20],
[ 20, 30, 10,  0,  0, 10, 30, 20]
]

whitePawnScores = [[50, 50, 50, 50, 50, 50, 50, 50],
[50, 50, 50, 50, 50, 50, 50, 50],
[10, 10, 20, 30, 30, 20, 10, 10],
[ 5,  5, 10, 25, 25, 10,  5,  5],
[ 0,  0,  0, 20, 20,  0,  0,  0],
[ 5, -5,-10,  0,  0,-10, -5,  5],
[ 5, 10, 10,-20,-20, 10, 10,  5],
 [0,  0,  0,  0,  0,  0,  0,  0]]

blackPawnScores = [[ 0,  0,  0,  0,  0,  0,  0,  0],
[ 5, 10, 10,-20,-20, 10, 10,  5],
[ 5, -5,-10,  0,  0,-10, -5,  5],
[ 0,  0,  0, 20, 20,  0,  0,  0],
[ 5,  5, 10, 25, 25, 10,  5,  5],
[10, 10, 20, 30, 30, 20, 10, 10],
[50, 50, 50, 50, 50, 50, 50, 50],
 [50, 50, 50, 50, 50, 50, 50, 50]]



piecePositionScores = {
    "N": knightScores,
    "B": bishopScores,
    "R": rookScores,
    "Q": queenScores,
    "bp": blackPawnScores,
    "wp": whitePawnScores,
    "K": kingScores
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
nextMove = None


def findRandomMove(validMoves):
    i = random.randint(0, len(validMoves)-1)
    return validMoves[i]


def findBestMove(gs, validMoves, returnQueue):
    global nextMove
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

    
    
    returnQueue.put( nextMove)


'''
Minimax algorithm
'''
def minimax(gs, validMoves, depth, alpha, beta, maximizingPlayer):
    global nextMove
    if depth == 0:
        return score(gs)

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
def score(gs):
    
    score = 0
    weight = 1./50
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            
            if square != '--':
                #score it positionally
                piecePositionScore = 0
                if square[1] == 'p':
                    piecePositionScore = piecePositionScores[square][row][col]
                else:
                    piecePositionScore = piecePositionScores[square[1]][row][col]
                
                if square[0] == 'w':
                    score += pieceScores[square[1]] + weight * piecePositionScore 
                elif square[0] =='b':
                    score -= pieceScores[square[1]] + weight * piecePositionScore 
    return score


