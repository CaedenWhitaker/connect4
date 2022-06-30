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
		MouseListener.events = [
			event
			for event in events
			if event.type in MouseListener.mouseEventTypes
		]
		for listener in MouseListener.listeners:
			listener.onClick()

	def __init__(self) -> None:
		pass

	def register(self):
		MouseListener.listeners.append(self)

	def deregister(self):
		MouseListener.listeners.remove(self)

	def onClick(self):
		raise NotImplementedError

	def getMousePosition():
		return pygame.mouse.get_pos()
