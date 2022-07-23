import math

from connect4.Constants import Constants

class PolicyNode:
	def __init__(self, state, move=None, parent=None) -> None:
		self.state = state.copy()
		self.parent = parent
		self.move = move
		self.branches = state.getMoves()
		self.children = []
		self.score = 0
		self.reached = 0
		self.parity = state.parity
	
	def policy(self):
		if self.reached > 0:
			return self.score / self.reached + math.sqrt(3 * math.log(self.parent.reached) / (self.reached))
		else:
			return -Constants.INF

	def performance(self):
		if self.reached > 0:
			return self.score / self.reached
		else:
			return -Constants.INF

	def select(self):
		return max(((node.policy(), node) for node in self.children), key=lambda x: x[0])[1]

	def expand(self, move, state):
		child = PolicyNode(state, move=move, parent=self)
		self.branches.remove(move)
		self.children.append(child)
		return child
	
	def update(self, delta):
		self.score += delta
		self.reached += 1

