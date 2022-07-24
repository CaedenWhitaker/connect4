from connect4.Constants import Constants
from connect4.MouseListener import MouseListener
from connect4.VisualElement import VisualElement
from connect4.Player import Player
from connect4.Board import Board
from connect4.GameMenuController import GameMenuController
import math
import pygame
import datetime


class Match(VisualElement, MouseListener):
	player1Color = (255, 0, 0)
	player2Color = (0, 0, 255)
	boardColor = (255, 255, 0)
	backgroundColor = (0, 0, 0)
	colorMap = {
		None: backgroundColor,
		False: player1Color,
		True: player2Color
	}
	framerate = 60

	def __init__(self, player1: Player, player2: Player, board: Board, canvasWidth=700, canvasHeight=700, scale=1.0):
		"""
		Match Constructor
		The Match object is in charge of the graphics logic. It recieves info from the Board object.

		@param player1:      the Player object representing player 1
		@param player2:      the Player object representing player 2
		@param board:        the Board object in charge of the game logic
		@param canvasWidth:  the width of the screen for the game
		@param canvasHeight: the height of the screen for the game
		@returns: None
		"""
		super().__init__(canvasWidth=canvasWidth, canvasHeight=canvasHeight, scale=scale)
		self.turn = False
		self.player1 = player1
		self.player1.setOrder(False)
		self.player1.setTurn(self.turn)
		self.player2 = player2
		self.player2.setOrder(True)
		self.player2.setTurn(self.turn)
		self.board = board
		self.winner = 0
		self.start = datetime.datetime.now()
		self.end = datetime.datetime.min
		self.running = False

		self.register()
		
		self.heldPiece = 0
		self.potentialMove = 0
		self.slotRadius = self.canvasWidth / (2 * self.board.cols)
		self.pieceRadius = 0.8 * self.slotRadius

		self.font = pygame.font.SysFont(None, math.floor(2 * self.pieceRadius * self.scale))
		self.p1Win = self.font.render(f"Player 1, {self.player1.name}, Wins!", True, Match.player1Color)
		self.p2Win = self.font.render(f"Player 2, {self.player2.name}, Wins!", True, Match.player2Color)
		self.tieWin = self.font.render("Tie!", True, (255,255,255))

		self.font_small = pygame.font.SysFont(None, math.floor(40 * self.scale))
		self.move_is_invalid = False
		self.invalid_prompt = self.font_small.render("Invalid", True, (255,255,255))

		img = pygame.image.load(Constants.GEAR_ICON_PATH)
		self.gear_icon = pygame.transform.scale(img, (20*self.scale, 20*self.scale))
		self.gearSize = VisualElement.rescale((25,25),self.scale,rounding=True)
		self.game_menu = GameMenuController(self.scale)
		self.open_game_menu = False
		self.quit = False

	

	def undo(self):
		undone = self.board.undo()
		if not undone:#if no pieces are on the board, do nothing
			return
		if not self.board.over:
			self.turn = not self.turn
		if self.board.over:
			self.board.over = False
			if self.winner is not None:
				self.turn = self.winner
			else:
				self.turn = True
		self.player1.setTurn(self.turn)
		self.player2.setTurn(self.turn)

	def doTurn(self):
		"""
		
		"""
		if self.turn:
			col = self.player2.getNextMove(self.board)
		else:
			col = self.player1.getNextMove(self.board)
		
		if col is not None:
			self.board.move(col, self.turn)
			win = self.board.checkWin(self.turn)
			self.turn = not self.turn
			if win != 0:
				if self.turn is not None:
					self.winner = win
					self.end = datetime.datetime.now()
				self.turn = None
				MouseListener.clear()
			self.player1.setTurn(self.turn)
			self.player2.setTurn(self.turn)

	def render(self):
		self.renderBackground()
		self.renderBoard()
		self.renderHeldPiece()
		self.renderPotentialMove()
		if self.move_is_invalid and not self.board.over:
			self.renderInvalidPrompt()
		
		if self.board.over:
			if self.winner == 1:
				size = self.p1Win.get_size()
				pos = ((self.scale*self.canvasWidth - size[0])/2, (2*self.scale*self.slotRadius - size[1])/2)
				self.surface.blit(self.p1Win, pos)
			if self.winner == 2:
				size = self.p2Win.get_size()
				pos = ((self.scale*self.canvasWidth - size[0])/2, (2*self.scale*self.slotRadius - size[1])/2)
				self.surface.blit(self.p2Win, pos)
			if self.winner == 3:
				size = self.tieWin.get_size()
				pos = ((self.scale*self.canvasWidth - size[0])/2, (2*self.scale*self.slotRadius - size[1])/2)
				self.surface.blit(self.tieWin, pos)
		
		self.renderMenuButton()
		if self.open_game_menu:
			self.open_game_menu = False
			ret_val = self.game_menu.mainloop(self.surface)
			if ret_val == "noop":
				pass
			if ret_val == "quit":
				self.quit = True
				#if self.board.over: #save game still if leaving when finished
			if ret_val == "undo":
				self.undo()
			if ret_val == "save":
				#save and quit
				#TODO save
				self.quit = True
		
		pygame.display.update()
		self.clock.tick(Match.framerate)
	
	def renderMenuButton(self):
		self.surface.blit(self.gear_icon, VisualElement.rescale((2.5,2.5), self.scale, True))
	
	def renderInvalidPrompt(self):
		pos = self.slotToPos(Board.rows, self.potentialMove)
		pos = (pos[0] - self.slotRadius, pos[1] - self.slotRadius / 2)
		pos = (pos[0], pos[1], 2*self.slotRadius, self.slotRadius)
		pos = VisualElement.rescale(pos, self.scale)
		pygame.draw.rect(self.surface, self.colorMap[self.turn], pos, 0, round(self.scale*12))
		pygame.draw.rect(self.surface, (50,50,50), pos, round(self.scale*5), round(self.scale*12))
		
		size = self.invalid_prompt.get_size()
		size = VisualElement.rescale(size, 1/self.scale)
		pos = VisualElement.rescale(pos, 1/self.scale)
		textPad = [(2*self.slotRadius - size[0]) / 2, (self.slotRadius - size[1]) / 2]
		pos = (pos[0] + textPad[0], pos[1] + textPad[1], 2*self.slotRadius, self.slotRadius)
		pos = VisualElement.rescale(pos, self.scale)
		self.surface.blit(self.invalid_prompt, pos)
	
		

	def renderBackground(self):
		self.surface.fill(Match.backgroundColor)

	def renderBoard(self):
		pygame.draw.rect(
			self.surface,
			Match.boardColor,
			VisualElement.rescale((0, 100, 700, 600), self.scale)
		)
		for row in range(self.board.rows):
			for col in range(self.board.cols):
				x, y = self.slotToPos(row, col)
				self.renderPiece(x, y, self.board.state[row][col])

	def slotToPos(self, row, col):
		x = (2 * self.slotRadius * col) + self.slotRadius
		y = (2 * self.slotRadius * (self.board.rows-1-row)) + 3 * self.slotRadius
		return (x, y)

	def renderPiece(self, x, y, turn, alpha=1.0):
		x, y = VisualElement.rescale((x, y), self.scale)
		color = self.colorMap[turn]
		if alpha:
			color = VisualElement.rescale(color, alpha, rounding=True)
		pygame.draw.circle(self.surface, color, (x, y), self.scale * self.pieceRadius)

	def renderHeldPiece(self):
		self.updateHeldPiece()
		x = self.heldPiece + self.slotRadius
		y = self.slotRadius
		self.renderPiece(x, y, self.turn)

	def renderPotentialMove(self):
		col = self.potentialMove
		if not self.board.colFull(self.potentialMove):
			x, y = self.slotToPos(self.board.top(col), col)
			self.renderPiece(x, y, self.turn, 0.35)

	def updateHeldPiece(self):
		if self.turn:
			x = self.player2.getHeldPiece()
		else:
			x = self.player1.getHeldPiece()
		if isinstance(x, int):
			self.heldPiece = x / self.scale
		elif isinstance(x, float):
			self.heldPiece = x * (self.canvasWidth - 2 * self.slotRadius) + self.slotRadius
		else:
			self.heldPiece = self.canvasWidth / 2
		self.heldPiece -= self.slotRadius
		self.heldPiece = max(min(self.heldPiece, self.canvasWidth - 2 * self.slotRadius), 0)
		self.updatePotentialMove()

	def updatePotentialMove(self):
		self.potentialMove = self.xToCol(self.heldPiece)
		self.move_is_invalid = self.board.colFull(self.potentialMove)
		if self.turn:
			self.player2.setPotentialMove(self.potentialMove)
		else:
			self.player1.setPotentialMove(self.potentialMove)
	
	def xToCol(self, x: int):
		return math.floor(self.board.cols * (x + self.slotRadius) / (self.canvasWidth))
	
	def onClick(self):
		for event in MouseListener.events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.pos[0] <= self.gearSize[0] and event.pos[1] <= self.gearSize[1]:
					self.open_game_menu = True
					continue
			#if the menu button was clicked, the code will not get this far
			#if self.board.over and event.type == pygame.MOUSEBUTTONDOWN:
				#self.running = False
	
	def mainloop(self):
		self.running = True
		while self.running and not self.quit:
			if pygame.event.peek(eventtype=pygame.QUIT):
				self.running = False
				return False
			else:
				events = pygame.event.get()
				MouseListener.listen(events)
				if not self.board.over:
					self.doTurn()
				self.render()
				#winning banner
		return True
