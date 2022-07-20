import pygame
import pygame_menu
import pygame_menu.locals
import pygame_menu.events
import string


class MainMenuController:
	
	def __init__(self, size=(400,400)):
		self.size = size
		self.player1 = 0
		self.player2 = 0
		self.p1_name_widget = None
		self.p2_name_widget = None
		self.player1_name = "AAA"
		self.player2_name = "AAA"
		self.loop = False
		self.x1 = 100
		self.x2 = 400
		self.font = pygame.font.SysFont(None, 45)
		#local menu MUST be made before the main menu
		self._make_replay_menu()
		self._make_local_menu()
		self._make_main_menu()

		self.info_surf = pygame.Surface((700,600))
		self._make_info_layout()

		
	
	def _make_main_menu(self):
		self.main_menu = pygame_menu.Menu("Main Menu", *self.size)
		self.main_menu.add.button("Local", action=self.open_local_menu)
		#if there are games
		self.main_menu.add.button("Replay", action=self.open_replay_menu)
		self.main_menu.add.button("Exit", action=pygame_menu.events.EXIT)

	def _make_local_menu(self):
		valid_chars = list(string.ascii_letters + string.digits)
		self.local_menu = pygame_menu.Menu("Local Play", *self.size, columns=4, rows=3)
		#self.local_menu.add.horizontal_margin(300)
		#self.local_menu.add.horizontal_margin(300)
		#self.local_menu.add.horizontal_margin(300)
		self.local_menu.add.selector("Player 1", [(" Human ",), ("Computer",)], 0, onchange=self.set_player1)
		self.local_menu.add.selector("Player 2", [(" Human ",), ("Computer",)], 0, onchange=self.set_player2)
		self.local_menu.add.button("Back", action=pygame_menu.events.BACK)
		self.p1_name_widget = self.local_menu.add.text_input("Id:", "AAA", onchange=self.p1_change_name,
																maxchar=3, valid_chars=valid_chars)
		self.p2_name_widget = self.local_menu.add.text_input("Id:", "AAA", onchange=self.p2_change_name,
																maxchar=3, valid_chars=valid_chars)
		self.local_menu.add.button("Confirm", action=self.close)
		self.local_menu.add.horizontal_margin(50)
		self.local_menu.add.horizontal_margin(50)
		self.local_menu.add.horizontal_margin(50)
		for widget in self.local_menu.get_widgets():
			widget.set_onselect(self.update_names)
			widget.set_onmouseover(self.update_names)
			widget.set_onmouseleave(self.update_names)

	def load_database(self, db):
		#do stuff
		pass
	
	def _make_replay_menu(self):

		self.replay_menu = pygame_menu.Menu("Select a game to replay", *self.size, center_content=False)
		self.replay_menu.add.dropselect("Game:", [("Item" + str(x), {}) for x in range(10)], 0, onchange=self.update_info)


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
			value = value + "A"*(3 - len(value))
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
		self.update_info(0, {})
	
	def _make_info_layout(self):
		p1_label_text = "Player 1:"
		p2_label_text = "Player 2:"
		moves_label_text = "Moves:"
		win_type_text = "Winner:"
		
		p1_label = self.font.render(p1_label_text, True, (255,255,255))
		p2_label = self.font.render(p2_label_text, True, (255,255,255))
		moves_label = self.font.render(moves_label_text, True, (255,255,255))
		win_type_label = self.font.render(win_type_text, True, (255,255,255))
		self.info_surf.blit(p1_label, (self.x1,50))
		self.info_surf.blit(p2_label, (self.x2, 50))
		self.info_surf.blit(moves_label, (self.x1, 250))
		self.info_surf.blit(win_type_label, (self.x1, 250 + 50))
		
	
	def update_info(self, something, info:dict):
		self.info_surf.fill((0,0,0))
		self._make_info_layout()
		kPlayer1Type = "p1_type"
		kPlayer2Type = "p2_type"
		kPlayer1Name = "p1_name"
		kPlayer2Name = "p2_name"
		kGameDateStamp = "datestamp"
		kNumberOfMoves = "num_moves"
		kWinType = "win_type"
		winner_label_size = self.font.size("Winner: ")
		print(something)
		print(info)
		
		p1_name_label = self.font.render("AJR", True, (255,255,255))
		p1_type_label = self.font.render("Computer", True, (255,255,255))
		p2_name_label = self.font.render("C_W", True, (255,255,255))
		p2_type_label = self.font.render("Human", True, (255,255,255))
		moves_label = self.font.render("42", True, (255,255,255))
		winner_label = self.font.render("Tie", True, (255,255,255))

		start_y = 100
		self.info_surf.blit(p1_name_label, (self.x1, start_y))
		self.info_surf.blit(p1_type_label, (self.x1, start_y + 50))

		self.info_surf.blit(p2_name_label, (self.x2, start_y))
		self.info_surf.blit(p2_type_label, (self.x2, start_y + 50))

		self.info_surf.blit(moves_label, (self.x1 + winner_label_size[0], 250))
		self.info_surf.blit(winner_label, (self.x1 + winner_label_size[0], 250 + 50))



		





		



	def close(self):
		self.loop = False
	
	def mainloop(self, window:pygame.Surface):
		self.loop = True
		while self.loop:
			if self.main_menu.is_enabled():
				self.main_menu.draw(window)
				self.main_menu.update(pygame.event.get())
				if self.main_menu._current is self.replay_menu:
					window.blit(self.info_surf, (0,250))
				pygame.display.update()
			




