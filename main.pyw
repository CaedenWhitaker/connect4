from connect4.MouseListener import MouseListener
from connect4.AIPlayer import AIPlayer
from connect4.HumanPlayer import HumanPlayer
from connect4.Match import Match
from connect4.Board import Board
import pygame
import ctypes
import sys
from connect4.MenuController import MenuController


def main():
	if hasattr(ctypes, "windll"):
		ctypes.windll.user32.SetProcessDPIAware()
		currMaxY = ctypes.windll.user32.GetSystemMetrics(1)
		scale = 0.8 * currMaxY / 700
	else:
		scale = 1.0

	pygame.init()
	temp_window = pygame.display.set_mode((400,400))


	mc = MenuController()
	mc.mainloop(temp_window)


	player1 = HumanPlayer() if mc.player1 == 0 else AIPlayer()
	player2 = HumanPlayer() if mc.player2 == 0 else AIPlayer()

	match = Match(player1, player2, Board(), scale=scale)

	running = True
	while running:
		if pygame.event.peek(eventtype=pygame.QUIT):
			running = False
		else:
			events = pygame.event.get()
			MouseListener.listen(events)
			if not match.board.over:
				match.doTurn()
			match.render()
			#winning banner
			
				
			
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()