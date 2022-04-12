"""
Responsible for storing all the info about the state of a chess game. Also responsible for determining valid moves at the current states and a move log.
"""

import string

from matplotlib.pyplot import pie

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
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = () ##coordinates for the square when an en-passant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                            self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)] 




    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        self.whiteToMove = not self.whiteToMove 

        #Is pawn promotion?
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #En-passant
        if move.isEnpassantMove:
            #move.pieceCaptured = self.board[move.startRow][move.endCol]
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn
            
        #else:
        #    move.pieceCaptured = self.board[move.endRow][move.endCol]
        
        #update enpassantpossible variable.
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ( (move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        

        #Castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                #move the rook
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                #remove the rook from old square
                self.board[move.endRow][move.endCol+1] = '--'
            else:
                #move the rook
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                #remove the rook from old square
                self.board[move.endRow][move.endCol-2] = '--'


        self.enpassantPossibleLog.append(self.enpassantPossible)

        #update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                            self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))



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

            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                #self.enpassantPossible = (move.endRow, move.endCol)
                
            
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            
            #undo 2 square pawn advance
            #if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            #    self.enpassantPossible = ()

            #undo castling rights
            self.castleRightsLog.pop()
            self.currentCastlingRights = self.castleRightsLog[-1]

            #undo castlemove
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside castle
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
            
            
            self.checkMate = False
            self.staleMate = False



    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved[1] == 'R':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.wks = False
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.bks = False
        
        #if a rook is captured
        if move.pieceCaptured[1] == 'R':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                if move.endCol == 7:
                    self.currentCastlingRights.wks = False
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                if move.endCol == 7:
                    self.currentCastlingRights.bks = False
                





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
        '''



        ### TODO: If in check, it does not allow to capture the piece that is checking!!


        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        print(self.inCheck)

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol][1]
                validSquares = []
                if pieceChecking == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #you get to the piece that checks
                            break
                # get rid of moves that do not deal with the check
                #print(moves)
                #print(validSquares)
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K': #Move does not move the king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
                print(moves)
            else: #Double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: #not in check so all moves are fine
            moves = self.getAllPossibleMoves()


        if len(moves) == 0: #Either checkmate or stalemate
            if self.inCheck:
                self.checkMate = True
                print("CheckMate")
            else:
                self.staleMate = True
                print("StaleMate")
        else:
            self.checkMate = False
            self.staleMate = False


        return moves


    def checkForPinsAndChecks(self, is_king=True, r=None, c=None):

        #print("Check for pins and checks")
        #print(self.whiteKingLocation, self.blackKingLocation)
        pins = []
        checks = []
        inCheck = False
        if is_king:
            if self.whiteToMove:
                allyColor = "w"
                enemyColor = "b"
                startRow = self.whiteKingLocation[0]
                startCol = self.whiteKingLocation[1]
            else:
                allyColor = "b"
                enemyColor = "w"
                startRow = self.blackKingLocation[0]
                startCol = self.blackKingLocation[1]
        else:
            if self.whiteToMove:
                allyColor = "w"
                enemyColor = "b"
                startRow = r
                startCol = c
            else:
                allyColor = "b"
                enemyColor = "w"
                startRow = r
                startCol = c
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for j in range(len(directions)):
            d  = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                #print(endRow, endCol)
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K' : 
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                            #print("possiblePin: ", possiblePin, startRow, startCol, endRow, endCol)
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        #print("End piece: ", endPiece)
                        type = endPiece[1]
                        if (0 <= j <= 3 and type=='R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'p' and ((enemyColor=='w' and 6 <= j <= 7) or (enemyColor=='b' and 4 <= j <= 5)   )) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break

                else:
                    break


        #knight checks
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, d[0], d[1]))
        

        #print (inCheck, pins, checks)

        return (inCheck, pins, checks)





    '''
    Is the current player in check?
    
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
        
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.whiteToMove:
            if self.board[r-1][c] == '--': #1 square advance
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r,c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == '--': #2 squares advance
                        moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0:
                isEnpassantMove = ((r-1, c-1) == self.enpassantPossible)
                if self.board[r-1][c-1][0] == 'b' or isEnpassantMove: #enemy piece to capture diagonally to the left
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r,c), (r-1, c-1), self.board, isEnpassantMove))
            if c+1 <= 7:
                isEnpassantMove = ((r-1, c+1) == self.enpassantPossible)
                if self.board[r-1][c+1][0] == 'b' or isEnpassantMove: #enemy piece to capture diagonally to the right
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r,c), (r-1, c+1), self.board, isEnpassantMove))
        else: #black pawn moves
            if self.board[r+1][c] == '--': #1 square advance
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r,c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == '--': #2 squares advance
                        moves.append(Move((r,c), (r+2, c), self.board))
            if c-1 >= 0:
                isEnpassantMove = ((r+1, c-1) == self.enpassantPossible)
                if self.board[r+1][c-1][0] == 'w' or isEnpassantMove: #enemy piece to capture diagonally to the left
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r,c), (r+1, c-1), self.board, isEnpassantMove))
            if c+1 <= 7:
                isEnpassantMove = ((r+1, c+1) == self.enpassantPossible)
                if self.board[r+1][c+1][0] == 'w' or isEnpassantMove: #enemy piece to capture diagonally to the right
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r,c), (r+1, c+1), self.board, isEnpassantMove))


    def getRookMoveOffset(self, r, c, direction, k):
        offsets = {
            'east': (r, c+1+k),
            'west': (r, c-1-k),
            'north': (r-1-k, c),
            'south': (r+1+k, c)
        }
        return offsets[direction]

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                if (self.board[r][c][1] != 'Q'): #Can't remove queen from pin on rook moves
                    self.pins.remove(self.pins[i])
                break


        conds_east = [self.board[r][x] == '--' for x in range(c+1,8)]
        conds_west = [self.board[r][x] == '--' for x in range(c-1, -1, -1)]
        conds_north = [self.board[x][c] == '--' for x in range(r-1, -1, -1)]
        conds_south = [self.board[x][c] == '--' for x in range(r+1, 8)]

        conds = [conds_east, conds_west, conds_north, conds_south]
        directions = ['east', 'west', 'north', 'south']
        directions_dict = {
            'east': (0, 1),
            'west': (0, -1),
            'north': (1, 0),
            'south': (-1, 0)
        }
        
        for direction, cond in zip(directions, conds):
            #print(r,c, direction, cond)
            d = directions_dict[direction]
            for k, v in enumerate(cond):
                offset = self.getRookMoveOffset( r, c, direction, k)
                if cond[k]:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        moves.append(Move((r,c), offset, self.board))
                else:
                    if self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                        if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
               
                self.pins.remove(self.pins[i])
                break
        
        conds_ne = [self.board[r-x][c+x] == '--' for x in range(1,8) if (r-x >= 0) and (c+x <= 7)]
        conds_nw = [self.board[r-x][c-x] == '--' for x in range(1,8) if (r-x >= 0) and (c-x >= 0)]
        conds_se = [self.board[r+x][c+x] == '--' for x in range(1,8) if (r+x <= 7) and (c+x <= 7)]
        conds_sw = [self.board[r+x][c-x] == '--' for x in range(1, 8) if (r+x <= 7) and (c-x >= 0)]

        conds = [conds_ne, conds_nw, conds_se, conds_sw]
        directions = ['ne', 'nw', 'se', 'sw']
        directions_dict = {
            'ne': (1, 1),
            'nw': (1, -1),
            'se': (-1, 1),
            'sw': (-1, -1)
        }


        for direction, cond in zip(directions, conds):
            d = directions_dict[direction]
            for k, v in enumerate(cond):
                offset = self.getBishopMoveOffset( r, c, direction, k)
                if cond[k]:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        moves.append(Move((r,c), offset, self.board))
                else:
                    if self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                        if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                            moves.append(Move((r,c), offset, self.board))
                    break
        
       

    def getKnightMoves(self, r, c, moves):

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        all_moves = [(r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2),
                          (r+1, c-2), (r+1, c+2), (r+2, c-1), (r+2, c+1)]
        possible_moves = [x for x in all_moves if x[0] >= 0 and x[0] <= 7 and x[1] >= 0 and x[1] <= 7]
        for offset in possible_moves:
            if (self.board[offset[0]][offset[1]]) == '--':
                if not piecePinned:
                    moves.append(Move((r,c), offset, self.board))
            else:
                if self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                    if not piecePinned:
                        moves.append(Move((r,c), offset, self.board))

    

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self, r, c, moves):
        all_moves = [(r+x, c+y) for x in [-1,0,1] for y in [-1, 0, 1]]
        possible_moves = [x for x in all_moves if x[0] >= 0 and x[0] <= 7 and x[1] >= 0 and x[1] <= 7 and (x[0], x[1]) != (r,c)]
        
        for offset in possible_moves:
            if self.board[offset[0]][offset[1]] == '--' or self.board[offset[0]][offset[1]][0] == self.enemyPiece[self.whiteToMove]:
                if self.whiteToMove:
                    self.whiteKingLocation = offset
                else:
                    self.blackKingLocation = offset
                inCheck, pins, checks = self.checkForPinsAndChecks()
                
                if not inCheck:
                    moves.append(Move((r,c), offset, self.board))
                if self.whiteToMove:
                    self.whiteKingLocation = (r, c)
                else:
                    self.blackKingLocation = (r, c)
        
        self.getCastleMoves(r,c,moves)
    

    def getCastleMoves(self, r, c, moves):
        if self.inCheck:
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)
        
    
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            is_under_attack1, _, _ = self.checkForPinsAndChecks(is_king=False, r=r, c=c+1)
            is_under_attack2, _, _ = self.checkForPinsAndChecks(is_king=False, r=r, c=c+2)
            if not is_under_attack1 and not is_under_attack2:
                moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True))


    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            is_under_attack1, _, _ = self.checkForPinsAndChecks(is_king=False, r=r, c=c-1)
            is_under_attack2, _, _ = self.checkForPinsAndChecks(is_king=False, r=r, c=c-2)
            if  not is_under_attack1 and not is_under_attack2:
                moves.append(Move((r,c), (r, c-2), self.board, isCastleMove=True))

class CastleRights():

    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs



class Move():


    rankToRows = {str(i):8-i for i in range(1, 9)}
    rowToRanks = {v:k for k,v in rankToRows.items()}
    filesToCols = {x: i for i,x in enumerate(list(string.ascii_lowercase[0:8]))}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        #Pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        
        #En-passant
        self.isEnpassantMove = isEnpassantMove
        #(self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == enpassantPossible)
        if isEnpassantMove:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'
        
        self.isCapture = self.pieceCaptured != '--'
        self.isCastleMove = isCastleMove
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
    
    
    '''
    Overriding str and use proper chess notation
    '''
    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow, self.endCol)
        #pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
            
            #pawn promotions
            #TODO
            
        #two of the same type of piece moving to a square
        #TODO
        
        #Add + for check move, # for checkmate
        #TODO
        
        #Piece Moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare
        
        
        





        
        

