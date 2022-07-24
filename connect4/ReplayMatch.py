import pygame
from connect4.Board import Board
from connect4.GameMenuController import GameMenuController
from connect4.Match import Match
from connect4.MouseListener import MouseListener
from connect4.Player import Player


class ReplayMatch(Match):

	def __init__(self, board: Board, game_info:dict, canvasWidth=700, canvasHeight=700, scale=1):
		super().__init__(Player("###"), Player("###"), board, canvasWidth, canvasHeight, scale)
		self.game_menu = GameMenuController(self.scale, can_save_game=False)
		self.moves = game_info["moves"]
		self.winner = game_info["winner"]
		self.index = -1
		self.heldPiece = self.slotToPos(Board.rows, self.moves[0])[0] - self.slotRadius
		self.potentialMove = self.moves[0]

	def advanceTurn(self):
		if self.index == len(self.moves) - 1:
			return
		self.index += 1
		self.board.move(self.moves[self.index], self.turn)
		self.turn = not self.turn
		self.board.over = self.index == len(self.moves) - 1
			
	

	def onClick(self):
		for event in MouseListener.events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.pos[0] <= 27 and event.pos[1] <= 27:
					self.open_game_menu = True
					continue
				self.advanceTurn()

	def undo(self):
		undone = self.board.undo()
		if not undone:#if no pieces are on the board, do nothing
			return
		self.turn = not self.turn
		self.board.over = False
		self.index -= 1

	
	def doTurn(self):
		pass#gnerf this method
	def updateHeldPiece(self):
		if self.index >= len(self.moves) - 1:
			self.heldPiece = -300
			self.updatePotentialMove()
			return
		self.heldPiece = self.slotToPos(Board.rows, self.moves[self.index + 1])[0] - self.slotRadius
		self.updatePotentialMove()
	

	def updatePotentialMove(self):
		if self.index >= len(self.moves) - 1:
			self.potentialMove = -2
			return
		self.potentialMove = self.moves[self.index + 1]
				







