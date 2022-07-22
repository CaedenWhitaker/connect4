from connect4.Board import Board

class Player:

	def __init__(self, name):
		self.name = name
		self.turn = None
		self.order = None
		self.type = ""
		self.potentialMove = None

	def setTurn(self, turn):
		"""
		This method sets whether it is this players turn
		@param turn: the turn of the game
		@returns: None
		@type: None
		"""
		self.turn = turn

	def setOrder(self, order):
		"""
		This method sets the play order of the player
		@returns: None
		@type: None
		"""
		self.order = order

	def setPotentialMove(self, potentialMove):
		"""
		This method sets the players potential move
		@param potentialMove: the potentialMove
		@returns: None
		@type: None
		"""
		self.potentialMove = potentialMove

	def getNextMove(self, state: Board):
		"""
		This method gets the next of the player
		This method should be over-ridden by subclasses
		@raises: NotImplementedError
		"""
		raise NotImplementedError
	
	def getHeldPiece(self):
		"""
		This method sets the position of the the hovering game
		token above the board
		This method should be over-ridden by subclasses
		@raises: NotImplementedError
		"""
		raise NotImplementedError
