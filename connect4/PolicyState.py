class PolicyStateConstants:
	def __init__(self) -> None:
		"constructor"
		self.rows = 6
		self.cols = 7
		self.goal = 4
		self.directions = [1, self.rows+1, self.rows, self.rows+2]
		self.full = sum(((1 << self.rows)-1) << (i*(self.rows+1)) for i in range(self.cols))

class PolicyState:
	constants = PolicyStateConstants()
	def __init__(self):
		"constructor"
		self.boards = [0, 0]
		self.heights = [0] * PolicyState.constants.cols
		self.parity = 0
        
	def copy(self):
		"copy the data of this object to prevent monadic effects"
		state = PolicyState()
		state.boards = list(self.boards)
		state.heights = list(self.heights)
		state.parity = self.parity
		return state

	def fromMoves(moves):
		"create a state from a moves list in the Board style"
		state = PolicyState()
		for move in moves:
			state.move(move)
		return state
        
	def move(self, col):
		"use bit operations to add a move to the player board"
		self.boards[self.parity] ^= 1 << ((PolicyState.constants.rows + 1) * col + self.heights[col])
		self.heights[col] += 1
		self.parity ^= 1
    
	def scoreState(self):
		"score the game if final state"
		if self.winner(0):
			self.score = -1
		elif self.winner(1):
			self.score = 1
		elif self.draw():
			self.score = 0
	
	def result(self, player):
		"don't recore"
		if not hasattr(self, "score"):
			self.scoreState()
		if self.score is not None:
			return ((1-2*player) * self.score + 1) / 2

	def valid(self, col):
		"ensure column isn't already full"
		return self.heights[col] < PolicyState.constants.rows
    
	def winner(self, player):
		"check in each direction, use the '0' bit as a seperate and & operation to assert 4 of the same, for each direction"
		for direction in PolicyState.constants.directions:
			bitboard = self.boards[player]
			for i in range(1, PolicyState.constants.goal): 
				bitboard &= self.boards[player] >> (i * direction)
			if bitboard > 0:
				return True
		return False
    
	def draw(self):
		"check if the game is a tie"
		return self.complete() and not self.winner(0) and not self.winner(1)

	def complete(self):
		"see if both boards together are full"
		return (self.boards[0] ^ self.boards[1]) == PolicyState.constants.full
    
	def getMoves(self):
		"find each column that isn't full"
		return [col for col in range(PolicyState.constants.cols) if self.valid(col)]
