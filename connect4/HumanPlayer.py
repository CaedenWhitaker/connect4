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
		"""
		This method sets the selected column, or if selected, finalizes the choice of a column
		@returns: None
		@type: None
		"""
		if self.turn == self.order:
			for event in MouseListener.events:
				if not self.selected and event.type == pygame.MOUSEBUTTONUP:
					if event.pos[0] <= 27 and event.pos[1] <= 27:#do not drop piece if clicking on the menu button
						return
					self.heldPiece = event.pos[0]
					self.selected = True
		else:
			self.selected = False
	
	def getNextMove(self, state: Board):
		"""
		This method returns the column index to play if the player has already selected one
		@param state: the board for the current game
		@returns: the column to play or NOne
		@type: int|None
		"""
		if self.selected:
			self.selected = False
			return self.potentialMove

	def getHeldPiece(self):
		"""
		This method sets the position of the the hovering game
		token above the board
		@returns: the x-coord of the mouse position
		@type: int
		"""
		if not self.selected:
			self.heldPiece = MouseListener.getMousePosition()[0]
		return self.heldPiece
	