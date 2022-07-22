from connect4.Player import Player
from connect4.Board import Board
import random


class AIPlayer(Player):
	def __init__(self, name):
		"""

		"""
		super().__init__(name)
		self.type = "C"
		self.heldPiece = 0.5
		self.direction = 1
	
	def getNextMove(self, state: Board):
		"""
		This method decides what the next move is for the AI
		@param state: the board for the current game
		@returns: the column index to play on
		@type: int
		"""
		if random.random() <= 0.005:
			return random.choice([
				i
				for i in range(state.cols)
				if not state.colFull(i)
			])
		
	def getHeldPiece(self):
		"""
		This method returns the x-coord of the mouse position for the AI
		@returns: the x-coord of the mouse position
		@type: float
		"""
		previousHeldPiece = self.heldPiece
		if random.random() <= 0.01:
			self.direction = -self.direction
		self.heldPiece += -self.direction * 0.005
		self.heldPiece = max(min(self.heldPiece, 1.0), 0.0)
		if self.heldPiece in {0.0, 1.0}:
			self.direction = -self.direction
		return previousHeldPiece
