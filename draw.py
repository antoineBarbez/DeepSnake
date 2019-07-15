import pygame


def background(surface, x, y, size):
	rect = pygame.Rect(x*size, y*size, size, size)
	
	pygame.draw.rect(surface,(127, 183, 190), rect)
	pygame.draw.rect(surface, (161, 202, 207), rect, 1)

def snake_cell(surface, x, y, size):
	rect = pygame.Rect(x*size, y*size, size, size)

	pygame.draw.ellipse(surface, (58, 64, 90), rect)

def prey(surface, x, y, size):
	rect = pygame.Rect(x*size, y*size, size, size)

	pygame.draw.ellipse(surface, (231, 69, 62), rect)