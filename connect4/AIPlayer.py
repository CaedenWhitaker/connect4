from scipy import rand
from connect4.Player import Player
from connect4.Board import Board
from connect4.PolicyNode import PolicyNode
from connect4.PolicyState import PolicyState
import random
import time


class AIPlayer(Player):
	def __init__(self, name):
		super().__init__(name)
		self.type = "C"
		self.heldPiece = 0.5
		self.direction = 1
		self.nodes = []
		self.deadline = None
		self.running = False
		self.counter = 30
	
	def getNextMove(self, board: Board):
		"""
		This method decides what the next move is for the AI
		@param state: the board for the current game
		@returns: the column index to play on
		@type: int
		"""
		if self.counter > 0:
			self.counter -= 1
			return None
		else:
			if len(self.nodes) == 0 or PolicyState.fromMoves(board.moves[:-1]).boards != self.nodes[-1].state.boards:
				self.nodes = [PolicyNode(PolicyState.fromMoves(board.moves[:-1]))]
			if len(board.moves) > 0:
				move = board.moves[-1]
				parent = self.nodes[-1]
				child = [child for child in parent.children if child.move == move]
				if len(child) > 0:
					child = child[0]
				else:
					state = parent.state.copy()
					state.move(move)
					child = parent.expand(move, state)
				self.nodes.append(child)
			self.counter = 30
			return self.policyTreeSearch()
			
		
	def getHeldPiece(self):
		"""
		This method returns the x-coord of the mouse position for the AI
		@returns: the x-coord of the mouse position
		@type: float
		"""
		previousHeldPiece = self.heldPiece
		self.heldPiece += self.direction * 0.005
		self.heldPiece = max(min(self.heldPiece, 1.0), 0.0)
		if self.heldPiece in {0.0, 1.0}:
			self.direction = -self.direction
		return previousHeldPiece


	def policyTreeSearch(self, iterationsMax=10000):
		"""
			Monte Carlo Tree Search for Connect Four
			Implementation referenced from https://replit.com/talk/share/Connect-4-AI-using-Monte-Carlo-Tree-Search/10640
			Thanks to Christopher Yong (see also PolicyNode and PolicyState)
		"""
		root = self.nodes[-1]

		for _ in range(iterationsMax):
			node = root
			state = root.state.copy()
			
			while len(node.branches) == 0 and len(node.children) > 0:
				node = node.select()
				state.move(node.move)
			
			while len(state.getMoves()) > 0:
				state.move(random.choice(state.getMoves()))
			
			while node is not None:
				node.update(state.result(node.parity))
				node = node.parent
			
			if self.deadline is not None and time.perf_counter() < self.deadline or len(root.branches) > 0:
				break

		for child in root.children:
			for _ in range(iterationsMax // len(root.children)):
				node = child
				state = child.state.copy()

				while len(node.branches) == 0 and len(node.children) > 0:
					node = node.select()
					state.move(node.move)
				
				if len(node.branches) > 0:
					move = random.choice(node.branches)
					state.move(move)
					node = node.expand(move, state)
				
				while len(state.getMoves()) > 0:
					state.move(random.choice(state.getMoves()))
				
				while node is not None:
					node.update(state.result(node.parity))
					node = node.parent
				
				if self.deadline is not None and time.perf_counter() < self.deadline:
					break
		
		for _ in range(iterationsMax):
				node = root
				state = root.state.copy()

				while len(node.branches) == 0 and len(node.children) > 0:
					node = node.select()
					state.move(node.move)
				
				if len(node.branches) > 0:
					move = random.choice(node.branches)
					state.move(move)
					node = node.expand(move, state)
				
				while len(state.getMoves()) > 0:
					state.move(random.choice(state.getMoves()))
				
				while node is not None:
					node.update(state.result(node.parity))
					node = node.parent
				
				if self.deadline is not None and time.perf_counter() < self.deadline:
					break

		node = max(((node.performance(), node) for node in root.children), key=lambda x: x[0])[1]
		self.nodes.append(node)
		return node.move
