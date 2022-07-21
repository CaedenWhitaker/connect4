from connect4.AIPlayer import AIPlayer
from connect4.HumanPlayer import HumanPlayer
from connect4.Match import Match
from connect4.Board import Board
import pygame
import ctypes
import sys
from connect4.MainMenuController import MainMenuController


def main():
	if hasattr(ctypes, "windll"):
		ctypes.windll.user32.SetProcessDPIAware()
		currMaxY = ctypes.windll.user32.GetSystemMetrics(1)
		scale = 0.8 * currMaxY / 700
	else:
		scale = 1.0

	pygame.init()
	temp_window = pygame.display.set_mode((700*scale,700*scale))
	running = True
	while running:
		mc = MainMenuController(scale)
		mc.mainloop(temp_window)#reset the menu only after the first game
		print(mc.player1, mc.player2)

		player1 = HumanPlayer() if mc.player1 == 0 else AIPlayer()
		player2 = HumanPlayer() if mc.player2 == 0 else AIPlayer()

		match = Match(player1, player2, Board(), scale=scale)
		running = match.mainloop()
				
			
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()