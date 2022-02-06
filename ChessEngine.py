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
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        self.whiteToMove = not self.whiteToMove 


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            self.whiteToMove = not self.whiteToMove


    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        '''
        1. Generate all possible moves
        2. Make all moves one by one
        3. For each move, generate opponent moves
        4. See if any one of those attacks the king
        5. If they do, it is not a valid move   
        '''
        moves = self.getAllPossibleMoves()
        
        for i in range(len(moves)-1, -1, -1): #go backwards
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if (self.inCheck()):
                #print(moves[i].startRow, moves[i].startCol, moves[i].endRow, moves[i].endCol )
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        if len(moves) == 0: #Either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
                print("CheckMate")
            else:
                self.staleMate = True
                print("StaleMate")
        else:
            self.checkMate = False
            self.staleMate = False

        return moves


    '''
    Is the current player in check?
    '''
    def inCheck(self):
        if (self.whiteToMove):
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])



    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False


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
                if r == 1 and self.board[r+2][c] == '--': #2 squares advance
                    moves.append(Move((r,c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture diagonally to the left
                    moves.append(Move((r,c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture diagonally to the right
                    moves.append(Move((r,c), (r+1, c+1), self.board))


    def getRookMoveOffset(self, r, c, direction, k):
        offsets = {
            'east': (r, c+1+k),
            'west': (r, c-1-k),
            'north': (r-1-k, c),
            'south': (r+1+k, c)
        }
        return offsets[direction]

    def getRookMoves(self, r, c, moves):
        conds_east = [self.board[r][x] == '--' for x in range(c+1,8)]
        conds_west = [self.board[r][x] == '--' for x in range(c-1, -1, -1)]
        conds_north = [self.board[x][c] == '--' for x in range(r-1, -1, -1)]
        conds_south = [self.board[x][c] == '--' for x in range(r+1, 8)]

        conds = [conds_east, conds_west, conds_north, conds_south]
        directions = ['east', 'west', 'north', 'south']
        
        for direction, cond in zip(directions, conds):
            #print(r,c, direction, cond)
            for k, v in enumerate(cond):
                offset = self.getRookMoveOffset( r, c, direction, k)
                if cond[k]:
                    moves.append(Move((r,c), offset, self.board))
                else:
                    if self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                        moves.append(Move((r,c), offset, self.board))
                    break
                    
        
    
    def getBishopMoveOffset(self, r, c, direction, k):
        offsets = {
            'ne': (r-1-k, c+1+k),
            'nw': (r-1-k, c-1-k),
            'se': (r+1+k, c+1+k),
            'sw': (r+1+k, c-1-k)
        }
        return offsets[direction]

    def getBishopMoves(self, r, c, moves):
        conds_ne = [self.board[r-x][c+x] == '--' for x in range(1,8) if (r-x >= 0) and (c+x <= 7)]
        conds_nw = [self.board[r-x][c-x] == '--' for x in range(1,8) if (r-x >= 0) and (c-x >= 0)]
        conds_se = [self.board[r+x][c+x] == '--' for x in range(1,8) if (r+x <= 7) and (c+x <= 7)]
        conds_sw = [self.board[r+x][c-x] == '--' for x in range(1, 8) if (r+x <= 7) and (c-x >= 0)]

        conds = [conds_ne, conds_nw, conds_se, conds_sw]
        directions = ['ne', 'nw', 'se', 'sw']
        
        for direction, cond in zip(directions, conds):
            for k, v in enumerate(cond):
                offset = self.getBishopMoveOffset( r, c, direction, k)
                if cond[k]:
                    moves.append(Move((r,c), offset, self.board))
                else:
                    if self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                        moves.append(Move((r,c), offset, self.board))
                    break
        
       

    def getKnightMoves(self, r, c, moves):
        all_moves = [(r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2),
                          (r+1, c-2), (r+1, c+2), (r+2, c-1), (r+2, c+1)]
        possible_moves = [x for x in all_moves if x[0] >= 0 and x[0] <= 7 and x[1] >= 0 and x[1] <= 7]
        for offset in possible_moves:
            if (self.board[offset[0]][offset[1]]) == '--':
                moves.append(Move((r,c), offset, self.board))
            else:
                if self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                    moves.append(Move((r,c), offset, self.board))

    

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        all_moves = [(r+x, c+y) for x in [-1,0,1] for y in [-1, 0, 1]]
        possible_moves = [x for x in all_moves if x[0] >= 0 and x[0] <= 7 and x[1] >= 0 and x[1] <= 7 and (x[0], x[1]) != (r,c)]
        for offset in possible_moves:
            if (self.board[offset[0]][offset[1]]) == '--':
                moves.append(Move((r,c), offset, self.board))
            else:
                if self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                    moves.append(Move((r,c), offset, self.board))

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





        
        

