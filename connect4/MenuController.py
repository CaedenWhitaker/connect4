import pygame
import pygame_menu
import pygame_menu.locals
import pygame_menu.events


class MenuController:
	
	def __init__(self, scale, size=(700,700)):
		self.scale = scale
		self.size = tuple(scale * element for element in size)
		self.player1 = 0
		self.player2 = 0
		self.loop = False
		#local menu MUST be made before the main menu
		self.make_local_menu()
		self.make_main_menu()
		
	
	def make_main_menu(self):
		self.main_menu = pygame_menu.Menu("Main Menu", *self.size)
		self.main_menu.add.button("Local", action=self.open_local_menu)
		self.main_menu.add.button("Replay", action= lambda: print("NYI"))
		self.main_menu.add.button("Close", action=pygame_menu.events.EXIT)

	def make_local_menu(self):
		self.local_menu = pygame_menu.Menu("Local Play", *self.size)
		self.local_menu.add.selector("Player 1", [("Human",), ("Computer",)], 0, onchange=self.set_player1)
		self.local_menu.add.selector("Player 2", [("Human",), ("Computer",)], 0, onchange=self.set_player2)
		self.local_menu.add.button("Confirm", action=self.close)
		self.local_menu.add.button("Back", action=pygame_menu.events.BACK)
	
	def set_player1(self, value:tuple):
		self.player1 = value[1]

	def set_player2(self, value:tuple):
		self.player2 = value[1]
	
	def open_local_menu(self):
		self.main_menu._open(self.local_menu)
	
	def close(self):
		self.loop = False
	
	def mainloop(self, window:pygame.Surface):
		self.loop = True
		print("loop starting")
		while self.loop:
			if self.main_menu.is_enabled():
				self.main_menu.draw(window)
				self.main_menu.update(pygame.event.get())
				pygame.display.update()
			




