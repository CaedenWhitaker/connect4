import pygame

class MouseListener:
	listeners = []
	events = []
	mouseEventTypes = [
		pygame.MOUSEBUTTONDOWN,
		pygame.MOUSEBUTTONUP,
		pygame.MOUSEMOTION,
		pygame.MOUSEWHEEL
	]
	def listen(events):
		"""
		This method iterates over the game events, filters out any non-mouse related
		events, and calls on a listeners onClick method
		@param events: the pygame events for the frame
		@returns: None
		@type: None
		"""
		MouseListener.events = tuple(
			event
			for event in events
			if event.type in MouseListener.mouseEventTypes
		)
		if len(MouseListener.events) > 0:
			for listener in MouseListener.listeners:
				listener.onClick()

	def __init__(self) -> None:
		pass

	def register(self):
		"""
		This method adds the caller to the global list of listeners
		@returns: None
		@type: None
		"""
		MouseListener.listeners.append(self)

	def deregister(self):
		"""
		This method removes the caller to the global list of listeners
		@returns: None
		@type: None
		"""
		MouseListener.listeners.remove(self)

	def onClick(self):
		raise NotImplementedError

	def getMousePosition():
		"""
		This method returns the coordinates of the mouse
		@returns: a 2-tuple of the mouse coordinates
		@type: tuple[int, int]
		"""
		return pygame.mouse.get_pos()
