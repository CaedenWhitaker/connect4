from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
from connect4.MouseListener import MouseListener
from connect4.AIPlayer import AIPlayer
from connect4.HumanPlayer import HumanPlayer
from connect4.Match import Match
from connect4.Board import Board
import pygame
import ctypes
import sys

from connect4.MouseListener import MouseListener


def main():
	if hasattr(ctypes, "windll"):
		prevMaxY = ctypes.windll.user32.GetSystemMetrics(1)
		ctypes.windll.user32.SetProcessDPIAware()
		currMaxY = ctypes.windll.user32.GetSystemMetrics(1)
		scale = 0.8 * currMaxY / prevMaxY
	else:
		scale = 1.0

	pygame.init()

	match = Match(AIPlayer(), AIPlayer(), Board(), scale=scale)
	
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
	pygame.quit()
	sys.exit()
		

if __name__ == "__main__":
	main()