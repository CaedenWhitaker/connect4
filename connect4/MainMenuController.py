import pygame
import pygame_menu
import pygame_menu.locals
import pygame_menu.events
from connect4.Constants import Constants
import string

from connect4.GameDatabase import GameDatabase


class MainMenuController:
	
	def __init__(self, scale:float, size=(700,700)):
		self.size = size[0] * scale, size[1] * scale
		self.scale = scale
		self.player1 = 0
		self.player2 = 0
		self.player1_name = "HP1"
		self.player2_name = "HP2"
		self.cp1_diff = 1
		self.cp2_diff = 1
		self.replay_info = None
		self.replay_game = False
		self.loop = False
		self.x1 = 100 * self.scale
		self.x2 = 400 * self.scale
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont(None, int(45 * self.scale))
		theme = pygame_menu.Theme(**self.scale_theme(Constants.get_main_theme()))
		#local menu MUST be made before the main menu
		self.games = list()
		self.process_db_info()
		self._make_replay_menu()
		self._make_local_menu(None)
		self._make_main_menu(theme)

		self.info_surf = pygame.Surface((700 * self.scale, 600 * self.scale))
		self._draw_info_layout()

	def scale_theme(self, theme:dict):
		if "title_font" in theme:
			theme["title_font"] = pygame.font.SysFont(None, int(145 * self.scale))
		if "title_font_size" in theme:
			theme["title_font_size"] = int(theme["title_font_size"] * self.scale)
		if "border_width" in theme:
			theme["border_width"] = int(theme["border_width"] * self.scale)
		return theme
		
	
	def _make_main_menu(self, theme):
		self.main_menu = pygame_menu.Menu("Connect4", *self.size, theme=theme)
		self.main_menu.add.button("Local", action=self.open_local_menu)
		
		if len(self.games) > 0:
			self.main_menu.add.button("Replay", action=self.open_replay_menu)
		self.main_menu.add.button("Exit", action=pygame_menu.events.EXIT)

	def _make_local_menu(self, theme):
		valid_chars = list(string.ascii_letters + string.digits)
		min_col_width = int(300*self.scale)
		self.local_menu = pygame_menu.Menu("Local Play", *self.size, columns=2, rows=5,
											column_min_width=(min_col_width,min_col_width))

		self.local_menu.add.selector("Player 1", [("Human",), ("Computer",)], 0, onchange=self.set_player1)
		self.local_menu.add.vertical_margin(65, margin_id="vm1")
		self.local_menu.get_widget("vm1").hide()
		self.local_menu.add.none_widget("none1vm")
		self.local_menu.add.selector("Player 2", [("Human",), ("Computer",)], 0, onchange=self.set_player2)
		self.local_menu.add.vertical_margin(65, margin_id="vm2")
		self.local_menu.get_widget("vm2").hide()
		self.local_menu.add.none_widget("none2vm")
		self.local_menu.add.button("Back", action=pygame_menu.events.BACK)
		self.local_menu.add.text_input("Id:", "HP1", onchange=self.p1_change_name,
										maxchar=3, valid_chars=valid_chars, textinput_id="p1name")
		
		self.local_menu.add.range_slider("Difficulty:", 1, [x+1 for x in range(9)], 1,
											onchange=self.cp1_change_diff, rangeslider_id="cp1r")
		self.local_menu.get_widget("cp1r").hide()
		self.local_menu.add.none_widget("none1r")

		self.local_menu.add.text_input("Id:", "HP2", onchange=self.p2_change_name,
										maxchar=3, valid_chars=valid_chars, textinput_id="p2name")
		self.local_menu.add.range_slider("Difficulty:", 1, [x+1 for x in range(9)], 1,
											onchange=self.cp2_change_diff, rangeslider_id="cp2r")
		self.local_menu.get_widget("cp2r").hide()
		self.local_menu.add.none_widget("none2r")

		self.local_menu.add.button("Confirm", action=self.close)

		for widget in self.local_menu.get_widgets():
			widget.set_onselect(self.update_names)
			widget.set_onmouseover(self.update_names)
			widget.set_onmouseleave(self.update_names)
		
	def process_db_info(self):
		for game in GameDatabase().getMatches():
			self.games.append((game["start"], game))

	
	def _make_replay_menu(self):

		self.replay_menu = pygame_menu.Menu("Select a game to replay", *self.size, center_content=False, columns=2, rows=1)
		if len(self.games) > 0:
			self.replay_menu.add.dropselect("Game:", self.games[::-1], (len(self.games)-1), onchange=self.update_info)
		self.replay_menu.add.button("Confirm", action=self.close)


	def update_names(self):
		if self.player1 == 0:
			self.local_menu.get_widget("p1name").set_value(self.player1_name)
		else:
			self.local_menu.get_widget("p1name").set_value("CP1")
		if self.player2 == 0:
			self.local_menu.get_widget("p2name").set_value(self.player2_name)
		else:
			self.local_menu.get_widget("p2name").set_value("CP2")
	
	def set_player1(self, value:tuple):
		self.player1 = value[1]
		if self.player1 == 1:
			self.local_menu.get_widget("p1name").set_value("CP1")
			self.local_menu.get_widget("none1vm").hide()
			self.local_menu.get_widget("none1r").hide()
			self.local_menu.get_widget("vm1").show()
			self.local_menu.get_widget("cp1r").show()
			
		if self.player1 == 0:
			self.local_menu.get_widget("p1name").set_value(self.player1_name)
			self.local_menu.get_widget("vm1").hide()
			self.local_menu.get_widget("cp1r").hide()
			self.local_menu.get_widget("none1vm").show()
			self.local_menu.get_widget("none1r").show()
			
	
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
			self.local_menu.get_widget("p2name").set_value("CP2")
			self.local_menu.get_widget("none2vm").hide()
			self.local_menu.get_widget("none2r").hide()
			self.local_menu.get_widget("cp2r").show()
			self.local_menu.get_widget("vm2").show()
			
		if self.player2 == 0:
			self.local_menu.get_widget("p2name").set_value(self.player2_name)
			self.local_menu.get_widget("cp2r").hide()
			self.local_menu.get_widget("vm2").hide()
			self.local_menu.get_widget("none2vm").show()
			self.local_menu.get_widget("none2r").show()
	
	def p2_change_name(self, value:str):
		if self.player2 == 1:
			return
		if len(value) < 3:
			value = value + "A"*(3 - len(value))
		value = value[:3]
		self.player2_name = value.upper()
	
	def cp1_change_diff(self, diff_lvl):
		self.cp1_diff = diff_lvl
	
	def cp2_change_diff(self, diff_lvl):
		self.cp2_diff = diff_lvl
	
	def open_local_menu(self):
		self.replay_game = False
		self.main_menu._open(self.local_menu)

	def open_replay_menu(self):
		self.replay_game = True
		self.main_menu._open(self.replay_menu)
		self.update_info(0, self.games[-1][1])
	
	def _draw_info_layout(self):
		p1_label_text = "Player 1:"
		p2_label_text = "Player 2:"
		moves_label_text = "Moves:"
		win_type_text = "Winner:"
		
		p1_label = self.font.render(p1_label_text, True, (255,0,0))
		p2_label = self.font.render(p2_label_text, True, (0,0,255))
		moves_label = self.font.render(moves_label_text, True, (255,255,255))
		win_type_label = self.font.render(win_type_text, True, (255,255,255))
		self.info_surf.blit(p1_label, (self.x1,50 * self.scale))
		self.info_surf.blit(p2_label, (self.x2, 50 * self.scale))
		self.info_surf.blit(moves_label, (self.x1, 250 * self.scale))
		self.info_surf.blit(win_type_label, (self.x1, (250 + 50) * self.scale))
		
	
	def update_info(self, something, info:dict):
		self.info_surf.fill((0,0,0))
		self._draw_info_layout()
		self.replay_info = info
		kPlayer1Type = "p1type"
		kPlayer2Type = "p2type"
		kPlayer1Name = "p1name"
		kPlayer2Name = "p2name"
		kNumberOfMoves = "moves"
		kWinType = "winner"
		winner_label_size = self.font.size("Winner: ")
		

		if info[kPlayer1Type] == "H":
			p1_name_label = self.font.render(info[kPlayer1Name], True, (255,0,0))
			p1_type_label = self.font.render("Human", True, (255,0,0))
		if info[kPlayer1Type] == "C":
			diff = info[kPlayer1Name][-1]
			p1_name_label = self.font.render(info[kPlayer1Name][:-1] + "1", True, (255,0,0))
			p1_type_label = self.font.render("Computer: " + diff, True, (255,0,0))
		
		
		if info[kPlayer2Type] == "H":
			p2_name_label = self.font.render(info[kPlayer2Name], True, (0,0,255))
			p2_type_label = self.font.render("Human", True, (0,0,255))
		if info[kPlayer2Type] == "C":
			diff = info[kPlayer2Name][-1]
			p2_name_label = self.font.render(info[kPlayer2Name][:-1] + "2", True, (0,0,255))
			p2_type_label = self.font.render("Computer: " + diff, True, (0,0,255))
		
		moves_label = self.font.render(str(len(info[kNumberOfMoves])), True, (255,255,255))
		if info[kWinType] == 0:
			winner_label = self.font.render("Unfinished", True, (255,255,255))
		if info[kWinType] == 1:
			winner_label = p1_name_label
		if info[kWinType] == 2:
			winner_label = p2_name_label
		if info[kWinType] == 3:
			winner_label = self.font.render("Tie", True, (255,255,255))
		
		start_y = 100 
		self.info_surf.blit(p1_name_label, (self.x1, start_y * self.scale))
		self.info_surf.blit(p1_type_label, (self.x1, (start_y + 50) * self.scale))

		self.info_surf.blit(p2_name_label, (self.x2, start_y * self.scale))
		self.info_surf.blit(p2_type_label, (self.x2, (start_y + 50) * self.scale))

		self.info_surf.blit(moves_label, (self.x1 + winner_label_size[0], 250 * self.scale))
		self.info_surf.blit(winner_label, (self.x1 + winner_label_size[0], (250 + 50) * self.scale))

	def close(self):
		self.loop = False
	
	
	def mainloop(self, window:pygame.Surface):
		self.loop = True
		while self.loop:
			self.clock.tick(30)
			if self.main_menu.is_enabled():
				self.main_menu.draw(window)
				self.main_menu.update(pygame.event.get())
				if self.main_menu._current is self.replay_menu:
					window.blit(self.info_surf, (0 * self.scale, 250 * self.scale))
				pygame.display.update()
		self.games = None
		if self.player1 == 1:
			self.player1_name = "CP" + str(self.cp1_diff)
		if self.player2 == 1:
			self.player2_name = "CP" + str(self.cp2_diff)
			




