import pygame
import pygame_menu
import pygame_menu.locals
import pygame_menu.events


class MenuController:
	
	def __init__(self, size=(400,400)):
		self.size = size
		self.player1 = 0
		self.player2 = 0
		self.p1_name_widget = None
		self.p2_name_widget = None
		self.player1_name = "AAA"
		self.player2_name = "AAA"
		self.loop = False
		#local menu MUST be made before the main menu
		self._make_replay_menu()
		self._make_local_menu()
		self._make_main_menu()

		self.info_surf = pygame.Surface((400, 700))

		
	
	def _make_main_menu(self):
		self.main_menu = pygame_menu.Menu("Main Menu", *self.size)
		self.main_menu.add.button("Local", action=self.open_local_menu)
		self.main_menu.add.button("Replay", action=self.open_replay_menu)
		self.main_menu.add.button("Exit", action=pygame_menu.events.EXIT)

	def _make_local_menu(self):
		self.local_menu = pygame_menu.Menu("Local Play", *self.size, columns=2, rows=3)
		self.local_menu.add.selector("Player 1", [("Human",), ("Computer",)], 0, onchange=self.set_player1)
		self.local_menu.add.selector("Player 2", [("Human",), ("Computer",)], 0, onchange=self.set_player2)
		self.local_menu.add.button("Back", action=pygame_menu.events.BACK)
		self.p1_name_widget = self.local_menu.add.text_input("Id:", "AAA", onchange=self.p1_change_name)
		self.p2_name_widget = self.local_menu.add.text_input("Id:", "AAA", onchange=self.p2_change_name)
		self.local_menu.add.button("Confirm", action=self.close)
		for widget in self.local_menu.get_widgets():
			widget.set_onselect(self.update_names)
			widget.set_onmouseover(self.update_names)
			widget.set_onmouseleave(self.update_names)

	def load_database(self, db):
		#do stuff
		pass
	
	def _make_replay_menu(self):

		self.replay_menu = pygame_menu.Menu("Select a game to replay", *self.size, center_content=False)
		self.replay_menu.add.dropselect("Game:", [("Item" + str(x),) for x in range(10)], 0, onchange=lambda x: print(x))


	def update_names(self):
		if self.player1 == 0:
			self.p1_name_widget.set_value(self.player1_name)
		else:
			self.p1_name_widget.set_value("CP1")
		if self.player2 == 0:
			self.p2_name_widget.set_value(self.player2_name)
		else:
			self.p2_name_widget.set_value("CP2")
	
	def set_player1(self, value:tuple):
		self.player1 = value[1]
		if self.player1 == 1:
			self.p1_name_widget.set_value("CP1")
		if self.player1 == 0:
			self.p1_name_widget.set_value(self.player1_name)
	
	def p1_change_name(self, value:str):
		if self.player1 == 1:
			return
		if len(value) < 3:
			value = value + "_"*(3 - len(value))
		value = value[:3]
		self.player1_name = value.upper()

	def set_player2(self, value:tuple):
		self.player2 = value[1]
		if self.player2 == 1:
			self.p2_name_widget.set_value("CP2")
		if self.player2 == 0:
			self.p2_name_widget.set_value(self.player2_name)
	
	def p2_change_name(self, value:str):
		if self.player2 == 1:
			return
		if len(value) < 3:
			value = value + "_"*(3 - len(value))
		value = value[:3]
		self.player2_name = value.upper()
	
	def open_local_menu(self):
		self.main_menu._open(self.local_menu)

	def open_replay_menu(self):
		self.main_menu._open(self.replay_menu)
	
	def update_info(self, info:dict):
		kPlayer1Type = "p1_type"
		kPlayer2Type = "p2_type"
		kPlayer1Name = "p1_name"
		kPlayer2Name = "p2_name"
		kGameDateStamp = "datestamp"
		kNumberOfMoves = "num_moves"

		



	def close(self):
		self.loop = False
	
	def mainloop(self, window:pygame.Surface):
		self.loop = True
		while self.loop:
			if self.main_menu.is_enabled():
				self.main_menu.draw(window)
				self.main_menu.update(pygame.event.get())
				if self.main_menu._current is self.replay_menu:
					pass
				pygame.display.update()
			




