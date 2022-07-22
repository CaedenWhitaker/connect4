

class Board:
	rows = 6
	cols = 7
	goal = 4

	def __init__(self) -> None:
		"""
		Board constructor
		"""
		self.state = [[None]*Board.cols for row in range(Board.rows)]
		self.heights = [0 for _ in range(Board.cols)]
		self.over = False
		self.moves:list[int] = list()
	
	def undo(self):
		if len(self.moves) == 0:#if no pieces are on the board, do nothing
			return False
		col = self.moves.pop()
		self.heights[col] -= 1
		self.state[self.heights[col]][col] = None
		return True


	def move(self, col: int, turn: bool) -> bool:
		"""
		Validates a move, then, if the move is valid, simulates the move being taken
		It also updates the `heights` property to reflect the new height of the column played on
		@param col: the column the player wishes to try to play on
		@param turn: the current player
		@returns: True if the move was valid, False otherwise
		@type: bool
		"""
		if self.colFull(col):
			return False
		self.state[self.heights[col]][col] = turn
		self.heights[col] += 1
		self.moves.append(col)
		return True
	
	def checkWin(self, turn: bool) -> bool:
		"""
		This method checks for a win and sets the `over` property to True if a win was detected.
		@param turn: the current player
		@returns: True is a win condition has been met, False otherwise
		"""
		if self.checkFull():
			self.over = True
			return (self.over, None)
		self.over = self.checkWinAux(turn)
		return (self.over, turn)
	
	def checkFull(self):
		for col in self.heights:
			if col < Board.rows:
				return False
		return True

	def checkWinAux(self, turn: bool) -> bool:
		"""
		This method checks win conditions for vertical, horizontal, and both diagonals.
		@param turn: the current player
		@returns: True if any win condition is met, False otherwise
		@type: bool
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
		"""
		This method checks to see if a given column is already full.
		@param col: the column to check
		@returns: True if the column is full, False if it is not.
		@type: bool
		"""
		return Board.rows <= self.heights[col]
	
	def top(self, col: int) -> int:
		"""
		This method gets the top slot of a column
		@param col: the column index
		@returns: the height of the specified column
		@type: int
		"""
		return self.heights[col]
