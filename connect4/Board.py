class Board:
	rows = 6
	cols = 7
	goal = 4

	def __init__(self) -> None:
		self.state = [[None]*Board.cols for row in range(Board.rows)]
		self.heights = [0 for col in range(Board.cols)]
		self.over = False

	def move(self, col: int, turn: bool) -> bool:
		if self.colFull(col):
			return False
		self.state[self.heights[col]][col] = turn
		self.heights[col] += 1
		return True
	
	def checkWin(self, turn: bool) -> bool:
		self.over = self.checkWinAux(turn)
		return self.over

	def checkWinAux(self, turn: bool) -> bool:
		for i in range(Board.rows):
			for j in range(Board.cols - Board.goal + 1):
				win = True
				for k in range(Board.goal):
					win = win and self.state[i][j+k] == turn
				if win:
					return True
		for i in range(Board.rows - Board.goal + 1):
			for j in range(Board.cols):
				win = True
				for k in range(Board.goal):
					win = win and self.state[i+k][j] == turn
				if win:
					return True
		for i in range(Board.rows - Board.goal + 1):
			for j in range(Board.rows - Board.goal + 1):
				win = True
				for k in range(Board.goal):
					win = win and self.state[i+k][j+k] == turn
				if win:
					return True
		for i in range(Board.rows - Board.goal + 1):
			for j in range(Board.goal, Board.rows):
				win = True
				for k in range(Board.goal):
					win = win and self.state[i+k][j-k] == turn
				if win:
					return True
		return False	

	def colFull(self, col: int) -> bool:
		return Board.rows <= self.heights[col]
	
	def top(self, col: int) -> int:
		return self.heights[col]
