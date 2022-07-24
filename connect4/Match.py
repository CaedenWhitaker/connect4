from connect4.Constants import Constants
from connect4.GameDatabase import GameDatabase
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
		
		self.moves = []
		self.heldPiece = 0
		self.potentialMove = 0
		self.slotRadius = self.canvasWidth / (2 * self.board.cols)
		self.pieceRadius = 0.8 * self.slotRadius

		self.font = pygame.font.SysFont(None, 175)
		self.p1win = self.font.render("Player 1 Wins!", True, (255,0,0))
		self.p2win = self.font.render("Player 2 Wins!", True, (0,0,255))
		self.tieWin = self.font.render("Tie!", True, (255,255,255))

		self.font_small = pygame.font.SysFont(None, int(30 * self.scale))
		self.move_is_invalid = False
		self.invalid_prompt = self.font_small.render("Invalid", True, (255,255,255))

		img = pygame.image.load(Constants.GEAR_ICON_PATH)
		self.gear_icon = pygame.transform.scale(img, (25*self.scale, 25*self.scale))
		self.game_menu = GameMenuController(self.scale)
		self.open_game_menu = False
		self.quit = False
		print(self.player1.type, self.player2.type)

	def undo_humans(self):
		undone = self.board.undo()
		if not undone:#if no pieces are on the board, do nothing
			return
		if not self.board.over:
			self.turn = not self.turn
		if self.board.over:
			self.board.over = False
			if self.winner != 3:
				self.turn = self.winner == 2
			else:
				self.turn = True
		self.player1.setTurn(self.turn)
		self.player2.setTurn(self.turn)

	def undo_one_com(self):
		self.undo_humans()
		self.undo_humans()

	def undo_two_comp(self):
		self.undo_one_com()

	def undo(self):
		if self.player1.type == "H" and self.player2.type == "H":
			self.undo_humans()
			return
		
		if self.player1.type == "C" and self.player2.type == "C":
			print("Undo is unsupported when 2 AI are playing")
			return
		
		if self.player1.type == "C" or self.player2.type == "C":
			self.undo_one_com()
			return

	def doTurn(self):
		"""
		
		"""
		if self.turn:
			col = self.player2.getNextMove(self.board)
		else:
			col = self.player1.getNextMove(self.board)
		
		if col is not None:
			self.board.move(col, self.turn)
			self.moves.append(col)
			win = self.board.checkWin(self.turn)
			self.turn = not self.turn
			if win != 0:
				if self.turn is not None:
					self.winner = win
					self.end = datetime.datetime.now()
				self.turn = None
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
			font = pygame.font.SysFont(None, 175)
			if self.winner == 1:
				text_obj = font.render("Player 1 Wins!", True, (255,0,0))
				self.surface.blit(text_obj, (10,0))
			if self.winner == 2:
				text_obj = font.render("Player 2 Wins!", True, (0,0,255))
				self.surface.blit(text_obj, (10,0))
			if self.winner == 3:
				self.surface.blit(self.tieWin, (10,0))
		
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
				GameDatabase().save(self)
				self.quit = True
		
		pygame.display.update()
		self.clock.tick(Match.framerate)
	
	def renderMenuButton(self):
		self.surface.blit(self.gear_icon, (0,0))
	
	def renderInvalidPrompt(self):
		x = MouseListener.getMousePosition()[0] / self.scale
		col = (x-1) // (2 * self.slotRadius)
		center = self.slotToPos(Board.rows, col)
		top_corner = (center[0] - self.slotRadius, center[1] - self.slotRadius)#translate center to top corner
		#top_corner = (top_corner[0] + 2, top_corner[1] - 3*self.slotRadius)
		
		
		padding_x = (self.slotRadius - self.pieceRadius)
		padding_y = self.slotRadius - (self.slotRadius//4) - 2
		top_corner_scaled = VisualElement.rescale(top_corner, self.scale)
		pygame.draw.rect(self.surface, (50,50,50), (top_corner_scaled[0] + padding_x,
													top_corner_scaled[1] + padding_y,
													self.slotRadius*2,
													self.slotRadius), 0, 12)
		pygame.draw.rect(self.surface, self.colorMap[self.turn], (top_corner_scaled[0] + padding_x,
																	top_corner_scaled[1] + padding_y,
																	self.slotRadius*2,
																	self.slotRadius), 5, 12)
		
		size = self.font_small.size("Invalid")
		text_pad_x = ((self.slotRadius*2) - size[0]) / 2
		text_pad_y = (self.slotRadius - size[1]) / 2
		self.surface.blit(self.invalid_prompt, (top_corner_scaled[0] + padding_x + text_pad_x, 
												top_corner_scaled[1] + padding_y + text_pad_y))
	
		

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
		if col is not None:
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
			self.heldPiece = x * (self.canvasWidth - 2 * self.slotRadius)
		else:
			self.heldPiece = self.canvasWidth / 2
		self.heldPiece -= self.slotRadius
		self.heldPiece = max(min(self.heldPiece, self.canvasWidth - 2 * self.slotRadius), 0)
		self.updatePotentialMove()

	def updatePotentialMove(self):
		self.potentialMove = self.xToCol(self.heldPiece)
		self.move_is_invalid = self.board.colFull(self.potentialMove)
		if self.board.colFull(self.potentialMove):
			self.potentialMove = None
		if self.turn:
			self.player2.setPotentialMove(self.potentialMove)
		else:
			self.player1.setPotentialMove(self.potentialMove)
	
	def xToCol(self, x: int):
		return math.floor(self.board.cols * (x + self.slotRadius) / (self.canvasWidth))
	
	def onClick(self):
		for event in MouseListener.events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.pos[0] <= 27 and event.pos[1] <= 27:
					self.open_game_menu = True
					continue
			#if the menu button was clicked, the code will not get this far
			#if self.board.over and event.type == pygame.MOUSEBUTTONDOWN:
				#self.running = False
	def deregister_listeners(self):
		if hasattr(self.player1, "deregister"):
			self.player1.deregister()
		if hasattr(self.player2, "deregister"):
			self.player2.deregister()
		self.deregister()
	
	def mainloop(self):
		self.running = True
		while self.running and not self.quit:
			if pygame.event.peek(eventtype=pygame.QUIT):
				self.running = False
				self.deregister_listeners()
				return False
			else:
				events = pygame.event.get()
				MouseListener.listen(events)
				if not self.board.over:
					self.doTurn()
				self.render()
		self.deregister_listeners()
		return True
