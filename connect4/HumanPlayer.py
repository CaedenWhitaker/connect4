from connect4.Player import Player
from connect4.MouseListener import MouseListener
from connect4.Board import Board
import pygame

class HumanPlayer(Player, MouseListener):

	def __init__(self) -> None:
		self.heldPiece = 0
		self.selected = False
		self.register()
		super().__init__()

	def onClick(self):
		if self.turn == self.order:
			for event in MouseListener.events:
				if not self.selected and event.type == pygame.MOUSEBUTTONUP:
					self.heldPiece = event.pos[0]
					self.selected = True
		else:
			self.selected = False
	
	def getNextMove(self, state: Board):
		if self.selected:
			self.selected = False
			return self.potentialMove

	def getHeldPiece(self):
		if not self.selected:
			self.heldPiece = MouseListener.getMousePosition()[0]
		return self.heldPiece
	