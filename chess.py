#
# Chess king-queen endgame simulator
# Michael Irvine and Aviv Caspi

# Type in the following to start, and then follow the onscreen instructions:
    # b = Board()
    # b.startGame()

import random
import time

class Board:
    """ a datatype representing a chess board """

    def __init__(self):
        """ the constructor for objects of type Board
        """
        self.width = 8
        self.height = 8
        self.pieceList = []
        self.clear()


    def __repr__(self):
        """ returns a string representation of type Board
            later will return a graphical 2D representation
        """
        H = self.height+1
        W = self.width
        s = ''
        d = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        for row in range(H ):
            if row==0:
                s += ' '
            if row>0:
                s += d[row-1] +'|'
            for col in range( self.width ):
                x = self.data[col][row-1]
                if row>0 and x==' ':
                    if (row+col-1)%2!=0:
                        s += '__|'
                    else:
                        s += '//|'
                elif row==0:
                    s+= ' _' + str(col+1)
                elif isinstance(x, Queen) and x.color=='white':
                    if (row+col-1)%2!=0:
                        s+= '_Q|'
                    else:
                        s+= '/Q|'
                elif isinstance(x, Queen):
                    if (row+col-1)%2!=0:
                        s+= '_q|'
                    else:
                        s+= '/q|'
                elif isinstance(x, King) and x.color=='white':
                    if (row+col-1)%2!=0:
                        s+= '_K|'
                    else:
                        s+= '/K|'
                elif isinstance(x, King):
                    if (row+col-1)%2!=0:
                        s+= '_k|'
                    else:
                        s+= '/k|'
                    
            s += '\n'

        
        s += '\n'
        return s

    def addPiece(self, p):
        """ adds a piece p to the board """
        self.data[p.x][p.y] = p
        self.pieceList+=[p]

    def delPiece(self, p):
        """ deletes a piece p from the board """
        self.data[p.x][p.y] = " "
        p.alive = False
        for i in range(len(self.pieceList)):
            if self.pieceList[i]!='' and self.pieceList[i].x == p.x and self.pieceList[i].y == p.y:
                self.pieceList[i] = ''
                break
    

    def movePiece(self, p, x, y, disp):
        """ moves a piece p's position to [x,y] """
        while True:
            L = p.getLegalMoves(self)
            if [x, y] in L and p.alive:
                self.delPiece(p)
                for i in self.pieceList:
                    if i!='' and i.x==x and i.y==y:
                        self.delPiece(i)
                p.x = x
                p.y = y
                self.addPiece(p)
                p.alive = True
                if disp:
                    print b
                    time.sleep(1)
                return True
            else:
                return False

    def startGame(self):
        """ Starts the game by getting whether players should be human-controlled or computer-controlled from the user
            and setting up the board.
        """
        while True:
            whiteType = input('Welcome to King-Queen Endgame Simulatior \nWould you like a (1) Computer or (2) Human to play as White (the attacker with a queen and a king)?\n')
            if whiteType == (1 or 'computer' or 'Computer'):
                whiteType = 'comp'
                break
            elif whiteType == (2 or 'human' or 'Human'):
                whiteType = 'human'
                break
            else:
                print 'Please input 1 or 2.'
        while True:
            blackType = input('Would you like a (1) Computer or (2) Human to play as Black (the defender with a king)?\n')
            if blackType == 1 or blackType=='computer' or blackType=='Computer':
                blackType = 'comp'
                break
            elif blackType == 2 or blackType=='human' or blackType=='Human':
                blackType = 'human'
                break
            else:
                print 'Please input 1 or 2.'
        self.setBoard('Q')
        print b
        self.playGame(whiteType, blackType)

    def setBoard(self, pt):
        """ Adds pieces to the board while ensuring they do not overlap, put the
            king in check, or start the game with a stalemate
        """
        x = random.randint(0,7)
        y = random.randint(0,7)
        if self.data[x][y] == ' ':
            if pt=='Q':
                global Q
                Q = Queen('white', x, y)
                self.addPiece(Q)
                self.setBoard('K')
            elif pt=='K':
                global K
                K = King('white', x, y)
                self.addPiece(K)
                self.setBoard('k')
            else:
                global k
                k = King('black', x, y)
                if b.checkCheck(k)==False and b.checkStalemate(k)==False:
                    self.addPiece(k)
                else:
                    self.setBoard(pt)
        else:
            self.setBoard(pt)

    def checkCheck(self, k):
        """ Returns True if King k is in check"""
        self.dataMem = [ [' ']*self.width for row in range(self.height) ]
        for i in self.pieceList:
            if i!='' and i.color != k.color:
                i.isAttacking(self)
        if self.dataMem[k.x][k.y] == 'A':
            self.dataMem = [ [' ']*self.width for row in range(self.height) ]
            return True
        self.dataMem = [ [' ']*self.width for row in range(self.height) ]
        return False

    def checkCheckmate(self, k):
        """ Returns True if King k is in checkmate """
        if self.checkCheck(k):
            if k.getLegalMoves(b)==[[k.x, k.y]]:
                return True
        return False

    def checkStalemate(self, k):
        """ Returns True if King k is in stalemate """
        if self.checkCheck(k)==False and k.getLegalMoves(b)==[[k.x, k.y]]:
            return True
        return False

    def playGame(self, wt, bt):
        """ Plays a game given inputs wt and bt telling whether the white and black
            players are humans or computers
        """
        global M
        M = 5000
        while True: #Stage 1, or loops here if white is a human until the game ends
            self.moveWhite('KING', 1, wt)
            if self.checkCheckmate(k):
                print 'White has won.'
                self.endGame()
            if self.checkStalemate(k):
                print 'It is a stalemate.'
                self.endGame()
            self.moveBlack(bt)
            if wt=='comp' and (K.x == 0 or K.x == 7):
                break

        self.moveWhite('QUEEN', 1, wt)
        self.moveBlack(bt)

     
        while True: #Stage 2
            self.moveWhite('QUEEN', 2, wt)
            self.moveBlack(bt)
            if wt=='comp' and M[0] == 8:
                break

        while True: #Stage 3
            self.moveWhite('KING', 2, wt)
            self.moveBlack(bt)
            if wt=='comp' and M[0] == 0:
                break

        #Checkmate
        self.moveWhite('QUEEN', 3, wt)
        if self.checkCheckmate(k):
            print "White has won."

        self.endGame()

    def moveWhite(self, pt, stage, wt):
        """ A helper function that takes in the type of the piece to move pt,
            the 'stage' the game is at, and the type of the white player and
            moves the best move for white (if computer-played) or allows the
            user to input a move
        """
        disp = True
        if wt=='comp':
            if pt=='KING':
                p = K
            else:
                p = Q
            if stage==1 or stage==3:
                lm = p.getLegalMoves(self)
                newSquare = self.rankWhiteMoves(pt, lm, k.x, k.y, K.x, K.y, stage)
                self.movePiece(p, newSquare[0], newSquare[1], disp)
            else:
                global M
                M = self.rankWhiteMoves(pt, p.getLegalMoves(self), k.x, k.y, K.x, K.y, 2)
                move = M[1:]
                self.movePiece(p, move[0], move[1], disp)
                    
        else:
            self.playerMove('white')

    def moveBlack(self, bt):
        """ A helper function that takes in the type of the black player and
            moves randomly if computer-played or allows the
            user to input a move.
            
            Note that the reason for moving randomly is because if we programmed
            it to make the best move possible, every game would essentially be the
            same or very similar. Random movement tests the versatility of our algorithm
            for white.
        """
        disp = True
        if bt=='comp':
            newSquare2 = self.rankBlackMoves(k.getLegalMoves(self))
            self.movePiece(k, newSquare2[0], newSquare2[1], disp)
        else:
            self.playerMove('black')

    def playerMove(self,c):
        """ Allows the player to input a piece to move and a location to move it to
            in chess coordinates while handling possible input errors.
        """
        disp = True
        pl = [p for p in self.pieceList if (p!='' and p.color==c)]
        while True:
            try:
                pToMove = input('What piece would you like to move? Choices: ' + str(pl) + ' ')
                if pToMove in pl:
                    break
                else:
                    print 'That is not a valid piece. Try again.'
            except:
                print 'That is not a valid piece. Try again.'
                
        while True:
            try:
                newSquare = raw_input('What square would you like to move it to? (In format B3): ')
                d = {'A':0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
                if self.movePiece(pToMove, int(newSquare[1])-1, d[newSquare[0]], disp):
                    break
                else:
                    print newSquare[0]
                    print 'That is not a valid square. Try again.'
            except:
                print 'That is not a valid square. Try again.'
                
    def endGame(self):
        """ Asks if the user wants to play again and starts a new game, or quits. """
        cont = raw_input('Would you like to play again? (yes/no)\n')
        if cont=='yes':
            self.clear()
            self.startGame()
        else:
            quit()

    def clear(self):
        """ Clears all board data. """
        self.data = [ [' ']*self.width for row in range(self.height) ]
        self.dataMem = [ [' ']*self.width for row in range(self.height) ]
        self.pieceList = []
        

    def rankWhiteMoves(self, piece, legalMoves, kx, ky, Kx, Ky, stage):
        """ranks list of moves, legalMoves, given piece type and data on
            other piece locations, as well as the x and y coordinates of the black king.
            considers stage in game for differing strategies.
            returns best move"""
        L = legalMoves[1:]
        x = legalMoves[0][0]
        y = legalMoves[0][1]
        z = []

        if piece == 'KING' and stage == 1:
            if (7-x) < x:
                z = max(L)
                return z
            else:
                z = min(L)
                return z
        elif piece == 'QUEEN' and stage == 1:
            if kx > Kx:
                for col in range(len(L)):
                    if L[col][0] == kx - 1 and abs(L[col][1] - ky) > 1:
                        z += [L[col]]
                        
            elif kx < Kx:
                for col in range(len(L)):
                    if L[col][0] == kx + 1 and abs(L[col][1] - ky) > 1:
                        z += [L[col]]
            else:
                if ky > Ky:
                    for row in range(len(L)):
                        if L[row][1] == ky - 1 and abs(L[row][0] - kx) > 1:
                            z += [L[row]]

                else:
                    for row in range(len(L)):
                        if L[row][1] == ky + 1 and abs(L[row][0] - kx) > 1:
                            z += [L[row]]
            return z[0]


                        
        elif piece == 'QUEEN' and stage == 2:
            if kx < x and ky < y:
                for move in range(len(L)):
                    px = L[move][0]
                    py = L[move][1]
                    A = (px+1)*(py+1)
                    if L[move][0] > kx and L[move][1] > ky and (abs(L[move][0] - kx) + abs(L[move][1] - ky)) > 2 and A > 6:
                        qx = Q.x
                        qy = Q.y
                        disp = False
                        b.movePiece(Q, px, py, disp)
                        if b.checkStalemate(k)==False:
                            z += [[A, L[move][0], L[move][1]]]
                        b.movePiece(Q, qx, qy, disp)
                Z = min(z)
                return Z
            elif kx > x and ky < y:
                for move in range(len(L)):
                    px = 7 - L[move][0]
                    py = L[move][1]
                    A = (px+1)*(py+1)
                    if L[move][0] < kx and L[move][1] > ky and (abs(L[move][0] - kx) + abs(L[move][1] - ky)) > 2 and A > 6:
                        qx = Q.x
                        qy = Q.y
                        disp = False
                        b.movePiece(Q, px, py, disp)
                        if b.checkStalemate(k)==False:
                            z += [[A, L[move][0], L[move][1]]]
                        b.movePiece(Q, qx, qy, disp)
                Z = min(z)
                return Z
            elif kx > x and ky > y:
                for move in range(len(L)):
                    px = 7 - L[move][0]
                    py = 7 - L[move][1]
                    A = (px+1)*(py+1)
                    if L[move][0] < kx and L[move][1] < ky and (abs(L[move][0] - kx) + abs(L[move][1] - ky)) > 2 and A > 6:
                        qx = Q.x
                        qy = Q.y
                        disp = False
                        b.movePiece(Q, px, py, disp)
                        if b.checkStalemate(k)==False:
                            z += [[A, L[move][0], L[move][1]]]
                        b.movePiece(Q, qx, qy, disp)
                Z = min(z)
                return Z
            else:
                for move in range(len(L)):
                    px = L[move][0]
                    py = 7 - L[move][1]
                    A = (px+1)*(py+1)
                    if L[move][0] > kx and L[move][1] < ky and (abs(L[move][0] - kx) + abs(L[move][1] - ky)) > 2 and A > 6:
                        qx = Q.x
                        qy = Q.y
                        disp = False
                        b.movePiece(Q, px, py, disp)
                        if b.checkStalemate(k)==False:
                            z += [[A, L[move][0], L[move][1]]]
                        b.movePiece(Q, qx, qy, disp)
                Z = min(z)
                return Z
        elif piece == 'KING' and stage == 2:
            if kx < 2 and ky < 2:
                for move in range(len(L)):
                    A = ((L[move][0] - 2)**2) + ((L[move][1] - 2)**2)
                    z += [[A, L[move][0], L[move][1]]]
                Z = min(z)
                return Z
            elif kx > 2 and ky < 5:
                for move in range(len(L)):
                    A = ((L[move][0] - 5)**2) + ((L[move][1] - 2)**2)
                    z += [[A, L[move][0], L[move][1]]]
                Z = min(z)
                return Z
            elif kx > 2 and ky > 2:
                for move in range(len(L)):
                    A = ((L[move][0] - 5)**2) + ((L[move][1] - 5)**2)
                    z += [[A, L[move][0], L[move][1]]]
                Z = min(z)
                return Z
            elif kx < 2 and ky > 2:
                for move in range(len(L)):
                    A = ((L[move][0] - 2)**2) + ((L[move][1] - 5)**2)
                    z += [[A, L[move][0], L[move][1]]]
                Z = min(z)
                return Z
        elif piece == 'QUEEN' and stage == 3:
            if kx < 2 and ky < 2:
                z = [1,1]
                return z
            elif kx > 5 and ky < 2:
                z = [6,1]
                return z
            elif kx > 5 and ky > 5:
                z = [6,6]
                return z
            elif kx < 2 and ky > 5:
                z = [1,6]
                return z
                           
    def rankBlackMoves(self, legalMoves):
        """ Returns a random move of the possible moves for the black king """
        L = legalMoves[1:]
        m = random.choice(L)
        return m
        

class Piece:

    def __init__(self, color, x, y):
        """ the contstructor
            contains the piece's color, coordinates, whether it has been taken,
            and opposite color
        """
        self.color = color
        self.x = x
        self.y = y
        self.alive = True
        if self.color=='white':
            self.oc = 'black'
        else:
            self.oc = 'white'
            
    def getLegalMoves(self, b):
        """ Gets all moves that the piece can make on the board, plus its current location
            which is useful for ranking moves.
        """
        L = [[self.x, self.y]]
        return self.getSurroundingSpaces(b, L)

    def isAttacking(self, b):
        """ Sets all spaces that the piece is attacking in a secondary board data
            array equal to 'A', which is useful for determining where kings can move
            and whether they are in check.
        """
        L = []
        L = self.getSurroundingSpaces(b,L)
        for i in range(len(L)):
            b.dataMem[L[i][0]][L[i][1]] = 'A'

class King(Piece):
    """ a datatype representing a King """

    def __repr__(self):
        """ returns a K if white and k if black """
        if self.color=='white':
            return 'K'
        else:
            return 'k'

    def getSurroundingSpaces(self, b, L):
        """ Returns a list of the coordinates for every space the king can move to
            or is attacking, depending on input L
        """
        attackCheck = True
        if L != []:
            b.dataMem = [ [' ']*b.width for row in range(b.height) ]
            for i in b.pieceList:
                if i!='':
                    if i.color==self.oc:
                        i.isAttacking(b)
            attackCheck = False
        x = self.x
        y = self.y
        width = 8
        height = 8
        for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    if i>=0 and i<width and j>=0 and j<height and not (i==x and j==y):
                        if (b.data[i][j]==' ' and b.dataMem[i][j] == ' ') or (isinstance(b.data[i][j], Piece) and ((b.data[i][j].color==self.oc and b.dataMem[i][j]==' ') or (b.data[i][j].color==self.color and attackCheck==True))):
                                L += [[i,j]]
        return L

class Queen(Piece):
    """ a datatype representing a Queen """

    def __repr__(self):
        """ returns a Q if white and q if black """
        # currently will only be called as white, but i'm leaving this in here for the future
        if self.color=='white':
            return 'Q'
        else:
            return 'q'
        
    def getSurroundingSpaces(self, b, L):
        """ Returns every space that the queen can move to. """
        x = self.x
        y = self.y
        width = 8
        height = 8
        for a in range(2):
            looper = range(x,-1,-1)
            if a==1:
                looper = range(x,width)
            for i in looper:
                if not i==x:
                    if b.data[i][y]==' ':
                        L +=[[i,y]]
                    else:
                        if b.data[i][y].color==self.oc:
                            L +=[[i,y]]
                        break
                    
        for a in range(2):
            looper = range(y,-1,-1)
            if a==1:
                looper = range(y,height)
            for i in looper:
                if not i==y:
                    if b.data[x][i]==' ':
                        L +=[[x,i]]
                    else:
                        if b.data[x][i].color==self.oc:
                            L +=[[x,i]]
                        break

        ppcont = True
        pncont = True
        nncont = True
        npcont = True
        for n in range(1,8):
            if x+n<width and y+n<width and ppcont:
                if b.data[x+n][y+n]==' ':
                    L +=[[x+n,y+n]]
                elif isinstance(b.data[x+n][y+n], Piece):
                    if b.data[x+n][y+n].color==self.oc:
                        L +=[[x+n,y+n]]
                    ppcont = False
                    
            if x+n<width and y-n>=0 and pncont:
                if b.data[x+n][y-n]==' ':
                    L +=[[x+n,y-n]]
                elif isinstance(b.data[x+n][y-n], Piece):
                    if b.data[x+n][y-n].color==self.oc:
                        L +=[[x+n,y-n]]
                    pncont = False
            if x-n>=0 and y-n>=0 and nncont:
                if b.data[x-n][y-n]==' ':
                    L +=[[x-n,y-n]]
                elif isinstance(b.data[x-n][y-n], Piece):
                    if b.data[x-n][y-n].color==self.oc:
                        L +=[[x-n,y-n]]
                    nncont = False
            if x-n>=0 and y+n<width and npcont:
                if b.data[x-n][y+n]==' ':
                    L +=[[x-n,y+n]]
                elif isinstance(b.data[x-n][y+n], Piece):
                    if b.data[x-n][y+n].color==self.oc:
                        L +=[[x-n,y+n]]
                    npcont = False
        return L


