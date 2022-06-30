from connect4.Board import Board

class Player:

	def __init__(self):
		self.turn = None
		self.order = None
		self.potentialMove = None

	def setTurn(self, turn):
		self.turn = turn

	def setOrder(self, order):
		self.order = order

	def setPotentialMove(self, potentialMove):
		self.potentialMove = potentialMove

	def getNextMove(self, state: Board):
		raise NotImplementedError
	
	def getHeldPiece(self):
		raise NotImplementedError
