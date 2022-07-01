from connect4.MouseListener import MouseListener
from connect4.AIPlayer import AIPlayer
from connect4.HumanPlayer import HumanPlayer
from connect4.Match import Match
from connect4.Board import Board
import pygame
import ctypes
import sys
import tkinter
import tkinter.ttk


def main():
	if hasattr(ctypes, "windll"):
		ctypes.windll.user32.SetProcessDPIAware()
		currMaxY = ctypes.windll.user32.GetSystemMetrics(1)
		scale = 0.8 * currMaxY / 700
	else:
		scale = 1.0

	pygame.init()

	global mode
	global popup
	popup = tkinter.Tk()
	mode = None

	def p1vp2():
		global mode
		global popup
		mode = 1
		popup.destroy()

	def p1vc1():
		global mode
		global popup
		mode = 2
		popup.destroy()

	def c1vc2():
		global mode
		global popup
		mode = 3
		popup.destroy()

	popup.wm_title("Connect 4")
	label = tkinter.ttk.Label(popup, text="Welcome to the Connect 4 Simulator!", font=("Verdana", 10))
	label.pack(side="top", fill="x", padx=15, pady=15)
	B1 = tkinter.ttk.Button(popup, text="Player 1 v. Player 1", command=p1vp2)
	B1.pack()
	B2 = tkinter.ttk.Button(popup, text="Player 1 v. Computer 1", command=p1vc1)
	B2.pack()
	B3 = tkinter.ttk.Button(popup, text="Computer 1 v. Computer 2", command=c1vc2)
	B3.pack()
	popup.mainloop()

	player1 = AIPlayer() if mode == 3 else HumanPlayer()
	player2 = HumanPlayer() if mode == 1 else AIPlayer()

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
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()