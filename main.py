#
# Chess endgame simulator 

class Board:
	""" a datatype representing a chess board """

	def __init__(self):
		""" the constructor for objects of type Board
		"""
		self.width = 8
		self.height = 8
		self.data = [["" for x in range(width)] for y in range(height)]
		#self.moveAllowed = [["" for x in range(width)] for y in range(height)]

	def __repr__(self):
		""" returns a string representation of type Board
		later will return a graphical 2D representation
		"""
	    H = self.height
	    W = self.width
	    s = ''
	    for x in range(0,H):
			for col in range(O,W):
				s = 1

	def playQueenGame(self):
	    """ plays a queen + king game """

	def playPawnGame(self):
	    """ plays a pawn + king game """


class Player:
	""" a datatype representing a chess player """

	def __init__(self, type):
		self.type = type

	def getMoves(self, width, height):
		L = [[0 for i in range(width)] for j in range(height)]
		print L[3][4]
			

	def bestMoveKing(self):
		""" returns the best possible spot that a player with only a
			king can move to
		"""

	def bestMoveQueen(self):
		""" returns the best possible piece and spot that a player 
			with a king and queen can move to.
		"""

	def bestMovePawn(self):
		""" returns the best possible piece and spot that a player
			with a pawn and king can move to.
		"""
