#
# Chess endgame simulator

class Board:
    """ a datatype representing a chess board """

    def __init__(self):
        """ the constructor for objects of type Board
        """
        self.width = 8
        self.height = 8
        self.data = [ [' ']*self.width for row in range(self.height) ]
        self.dataMem = [ [' ']*self.width for row in range(self.height) ]
        self.pieceList = []

    def __repr__(self):
        """ returns a string representation of type Board
            later will return a graphical 2D representation
        """
        H = self.height+1
        W = self.width
        s = ''
        for row in range(H ):
            if row>0:
                s += '|'
            for col in range( self.width ):
                x = self.data[col][row-1]
                if row>0 and x==' ':
                    s += '__|'
                elif row==0:
                    s+= ' __'
                elif isinstance(x, Queen) and x.color=='white':
                    s+= '_Q|'
                elif isinstance(x, Queen):
                    s+= '_q|'
                elif isinstance(x, King) and x.color=='white':
                    s+= '_K|'
                elif isinstance(x, King):
                    s+= '_k|'
                elif isinstance(x, Pawn) and x.color=='white':
                    s+= '_P|'
                elif isinstance(x, Pawn):
                    s+= '_p|'
                elif x=='A':
                    s+= '_A|'
                    
            s += '\n'

        
        s += '\n'
        return s

    def addPiece(self, p):
        """ adds a piece to the board """
        self.data[p.x][p.y] = p
        self.pieceList+=[p]

    def delPiece(self, p):
        """ deletes a piece from the board """
        self.data[p.x][p.y] = " "
        for i in self.pieceList:
            if i==p:
                i = ''

    def movePiece(self, p, x, y):
        """ moves a piece's position """
        for i in self.pieceList:
            if i!='':
                if i.color==p.oc:
                    i.isAttacking(self)
        L = p.getLegalMoves(self)
        if [x, y] in L:
            self.delPiece(p)
            for i in self.pieceList:
                if i!='' and i.x==x and i.y==y:
                    self.delPiece(i)
            p.x = x
            p.y = y
            self.addPiece(p)
            self.dataMem = [ [' ']*self.width for row in range(self.height) ]
            return True
        else:
            print "That is not a valid move."
            return False

    def playQueenGame(self):
        """ plays a queen + king game """

    def playPawnGame(self):
        """ plays a pawn + king game """

class Player:
    """ a datatype representing a chess player """

    def __init__(self, playerType):
        self.type = playerType

    def getMoves(self, width , height, x, y, piece, data):
        L = []
        

class Piece:

    def __init__(self, color, x, y):
        """ the contstructor """
        self.color = color
        self.x = x
        self.y = y
        if self.color=='white':
            self.oc = 'black'
        else:
            self.oc = 'white'
            
    def getLegalMoves(self, b):
        L = [[self.x, self.y]]
        return self.getSurroundingSpaces(b, L)

    def isAttacking(self, b):
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
        attackCheck = True
        if L != []:
            attackCheck = False
        x = self.x
        y = self.y
        width = 8
        height = 8
        for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    if i>=0 and i<width and j>=0 and j<height and not (i==x and j==y):
                        if (b.data[i][j]==' ' and b.dataMem[i][j] == ' ') or (attackCheck==True and b.dataMem[i][j] == 'A') or (isinstance(b.data[i][j], Piece) and b.data[i][j].color==self.oc):
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

class Pawn(Piece):
    """ a datatype representing a King """

    def __repr__(self):
        """ returns a P if white and p if black """
        # same as queen
        if self.color=='white':
            return 'P'
        else:
            return 'p'
