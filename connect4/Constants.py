import pygame
import pygame_menu

class Constants:
	DATABASE_PATH = r"connect4.db"
	def get_main_theme():
		return {
	        "background_color": pygame_menu.BaseImage(r"connect4\resources\c4_bg_pic.png"),
	        "border_color": (128, 128, 128),
	        "border_width": 5,
	        "selection_color": (173,0,0),
	        #"cursor_color": (int(), int(), int()),
	        "fps": 60,
	        "title": True,
	        "title_background_color": (255,255,0),
	        "title_close_button": True,
	        #"title_fixed": True,
	        "title_floating": True,
	        #"title_font": pygame.font.SysFont(None, 145),
	        "title_font_antialias": True,
	        "title_font_color": (int(), int(), int()),
	        "title_font_size": 50,
	        "widget_font_size": 40,
	        "widget_font_color": (0,173,0),
	        "widget_background_color": (100,100,100)
            }