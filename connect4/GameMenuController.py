from faulthandler import is_enabled
import pygame
import pygame_menu
import pygame_menu.locals
import pygame_menu.events
from connect4.Constants import Constants


class GameMenuController:

	def __init__(self, scale):
		self.scale = scale
		self.size = (400, 600)
		self.looping = False
		self._make_save_menu()
		self._make_game_menu()
		self.close_with = "noop"

	def _make_game_menu(self):
		self.game_menu = pygame_menu.Menu("Game Menu", *self.size)
		self.game_menu.add.button("Undo", action=self.undo_move)
		self.game_menu.add.button("Quit", action=self.save_menu)
		self.game_menu.add.button("Back", action=self.close_menu)
	
	def _make_save_menu(self):
		self.save_menu = pygame_menu.Menu("Save", *self.size)
		self.save_menu.add.label("Would you like to save?")
		self.save_menu.add.button("Yes", action=self.save_game)
		self.save_menu.add.button("No", action=self.quit_game)
	
	def save_game(self):
		self.close_with = "save"
		self.close_menu()
	
	def undo_move(self):
		self.close_with = "undo"
		self.close_menu()
	
	def quit_game(self):
		self.close_with = "quit"
		self.close_menu()

	def close_menu(self):
		self.looping = False

	def mainloop(self, window:pygame.Surface):
		self.looping = True
		self.close_with = "noop"
		while self.looping:
			if pygame.event.peek(pygame.QUIT):
				break
			if self.game_menu.is_enabled():
				self.game_menu.draw(window)
				self.game_menu.update(pygame.event.get())
				pygame.display.update()
		return self.close_with

