from connect4.Player import Player
from connect4.Board import Board
import random


class AIPlayer(Player):
	def __init__(self):
		super().__init__()
		self.heldPiece = 0.5
		self.direction = 1
	
	def getNextMove(self, state: Board):
		if random.random() <= 0.005:
			return random.choice([
				i
				for i in range(state.cols)
				if not state.colFull(i)
			])
		
	def getHeldPiece(self):
		previousHeldPiece = self.heldPiece
		if random.random() <= 0.01:
			self.direction = -self.direction
		self.heldPiece += -self.direction * 0.005
		self.heldPiece = max(min(self.heldPiece, 1.0), 0.0)
		if self.heldPiece in {0.0, 1.0}:
			self.direction = -self.direction
		return previousHeldPiece
