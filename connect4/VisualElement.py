import pygame

class VisualElement:
	def __init__(self, canvasWidth=700, canvasHeight=700, scale=1.0, refreshRate=60) -> None:
		"constructor"
		self.canvasWidth = canvasWidth
		self.canvasHeight = canvasHeight
		self.scale = scale
		self.refreshRate = refreshRate
		self.clock = pygame.time.Clock()
		self.size = (self.scale * self.canvasWidth, self.scale * self.canvasHeight)
		self.surface: pygame.Surface = pygame.display.set_mode(
			self.size
		)

	def render(self) -> None:
		"""
		This method draws the game to the screen
		This method should be over-ridden by subclasses
		@raises: NotImplementedError
		"""
		raise NotImplementedError

	def rescale(vector, scale, rounding=False):
		"""
		This method calculates the scale to resize the drawn objects in the window
		@param vector:
		@param scale:
		@param rounding:
		@returns:
		@type: tuple[int, int]
		"""
		vector = (scale * element for element in vector)
		if rounding:
			vector = map(round, vector)
		return tuple(vector)
