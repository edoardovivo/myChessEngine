"""
Responsible for storing all the info about the state of a chess game. Also responsible for determining valid moves at the current states and a move log.
"""

import string

class GameState():

    def __init__(self):
        # board is a 8x8 2d list. Each element has 2 characters. The first characters is the color, 'b' or 'w'. The second character represent the type of the piece.
        # '--' represent a square with no pieces on it.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove 


class Move():


    rankToRows = {str(i):8-i for i in range(1, 9)}
    rowToRanks = {v:k for k,v in rankToRows.items()}
    filesToCols = {x: i for i,x in enumerate(list(string.ascii_lowercase[0:8]))}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]


    def getChessNotation(self):
        #Make this more chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)



    def getRankFile(self, r, c ):
        return self.colsToFiles[c] + self.rowToRanks[r]





        
        

