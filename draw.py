import pygame

# pygame.gfxdraw allows to draw an anti-aliased shapes but is experimental.
try:
	import pygame.gfxdraw
	gfxdraw_available = True
except ImportError:
	gfxdraw_available = False

def background(surface, x, y, size):
	rect = pygame.Rect(x*size, y*size, size, size)
	
	pygame.draw.rect(surface,(127, 183, 190), rect)
	pygame.draw.rect(surface, (161, 202, 207), rect, 1)

def snake_cell(surface, x, y, size):
	if gfxdraw_available:
		pygame.gfxdraw.aacircle(surface, x*size + size/2, y*size + size/2, size/2 -1, (58, 64, 90))
		pygame.gfxdraw.filled_circle(surface, x*size + size/2, y*size + size/2, size/2 -1, (58, 64, 90))
	else:
		pygame.draw.circle(surface, (58, 64, 90), (x*size + size/2, y*size + size/2), size/2 -1)

def prey(surface, x, y, size):
	if gfxdraw_available:
		pygame.gfxdraw.aacircle(surface, x*size + size/2, y*size + size/2, size/2 -1 , (231, 69, 62))
		pygame.gfxdraw.filled_circle(surface, x*size + size/2, y*size + size/2, size/2 -1, (231, 69, 62))
	else:
		pygame.draw.circle(surface, (231, 69, 62), (x*size + size/2, y*size + size/2), size/2 -1)