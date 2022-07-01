import pygame

class VisualElement:
	def __init__(self, canvasWidth=700, canvasHeight=700, scale=1.0, refreshRate=60) -> None:
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
		raise NotImplementedError

	def rescale(vector, scale, rounding=False):
		vector = (scale * element for element in vector)
		if rounding:
			vector = map(round, vector)
		return tuple(vector)
