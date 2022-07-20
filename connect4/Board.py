class Board:
	rows = 6
	cols = 7
	goal = 4

	def __init__(self) -> None:
		"""Create an empty board object"""
		self.state = [[None]*Board.cols for row in range(Board.rows)]
		"""2D array board state. None for empty, else bool for the player."""
		self.heights = [0 for col in range(Board.cols)]
		self.over = False

	def move(self, col: int, turn: bool) -> bool:
		"""
		Updates board object with given move, if the move is legal.

		Args:
			col: The column the player wants to play a move on.
			turn: The moving player; False for player1 and True for player2.
		
		Returns:
			A bool; hether the move was legal and therefore played.
		"""
		if self.colFull(col):
			return False
		self.state[self.heights[col]][col] = turn
		self.heights[col] += 1
		return True
	
	def checkWin(self, turn: bool) -> bool:
		"""
		Evaluate whether the moving player has won.

		Args:
			turn: The moving player; False for player1 and True for player2.
		
		Returns:
			A bool; whether the moving player has won in the current board state.
		"""
		self.over = self.checkWinAux(turn)
		return self.over

	def checkWinAux(self, turn: bool) -> bool:
		"""
		Auxiliary method to evaluate whether the moving player has won.

		Args:
			turn: The moving player; False for player1 and True for player2.
		
		Returns:
			A bool; whether the moving player has won in the current board state.
		"""
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
			for j in range(Board.cols - Board.goal + 1):
				win = True
				for k in range(Board.goal):
					win = win and self.state[i+k][j+k] == turn
				if win:
					return True
		for i in range(Board.rows - Board.goal + 1):
			for j in range(Board.goal-1, Board.cols):
				win = True
				for k in range(Board.goal):
					win = win and self.state[i+k][j-k] == turn
				if win:
					return True
		return False	

	def colFull(self, col: int) -> bool:
		"""
		Evaluate whether a specific column is full of pieces.

		Args:
			col: The column which is in question.

		Returns:
			A bool; whether the column is already filled with pieces.
		"""
		return Board.rows <= self.heights[col]
	
	def top(self, col: int) -> int:
		"""
		Find the top open slot in a specific column.

		Args:
			col: The column which is in question.

		Returns:
			An integer; the number of pieces already in the column.
		"""
		return self.heights[col]
