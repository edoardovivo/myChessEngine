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
            ["--","bR","--","--","--","wB","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }
        self.enemyPiece = {
            True: 'b', #if it is white turn, then the enemy piece is black and viceversa
            False: 'w'
        }

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove 


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = '--'
            self.whiteToMove = not self.whiteToMove


    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves()


    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves



    def getPawnMoves(self, r, c, moves):
        
        if self.whiteToMove:
            if self.board[r-1][c] == '--': #1 square advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 squares advance
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture diagonally to the left
                    moves.append(Move((r,c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture diagonally to the right
                    moves.append(Move((r,c), (r-1, c+1), self.board))
        else: #black pawn moves
            if self.board[r+1][c] == '--': #1 square advance
                
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 2 and self.board[r+2][c] == '--': #2 squares advance
                    moves.append(Move((r,c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture diagonally to the left
                    moves.append(Move((r,c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture diagonally to the right
                    moves.append(Move((r,c), (r+1, c+1), self.board))


    def getRookMoves(self, r, c, moves):
        conds_east = [self.board[r][x] == '--' for x in range(c+1,8)]
        conds_west = [self.board[r][x] == '--' for x in range(c-1, 0, -1)]
        for k, v in enumerate(conds_east):
            if conds_east[k]:
                print("Appending move ({}, {}) to ({},{})".format(r,c, r, c+1+k))
                moves.append(Move((r,c), (r, c+1+k), self.board))
            else:
                if self.board[r][c+1+k][0] == self.enemyPiece[self.whiteToMove]:
                    moves.append(Move((r,c), (r, c+1+k), self.board))
                    break
        #print(moves)
        '''
        moves_east = [ (x, Move((r,c), (r, x), self.board) ) for x in range(c+1, 8) if self.board[r][x] == '--' ]
        if (len(moves_east) > 0):
            last_col = moves_east[-1][0]
            if self.board[r][last_col+1][0] == 'b':
                moves_east.append(Move( (r,c), (r, last_col+1) ))
        '''
        
    


    def getKnightMoves(self, r, c, moves):
        pass

    def getBishopMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass

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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    '''
    Overriding equal method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False





    def getChessNotation(self):
        #Make this more chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)



    def getRankFile(self, r, c ):
        return self.colsToFiles[c] + self.rowToRanks[r]





        
        

