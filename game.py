from pygame.locals import *

import environment as env

import pygame
import sys
import time

class SnakeGame(object):
	CELL_SIZE = 30
	
	def __init__(self, grid_size=10):
		pygame.init()
		pygame.display.set_caption('Score: 0')
		self.screen = pygame.display.set_mode((self.CELL_SIZE * grid_size, self.CELL_SIZE * grid_size))
		self.screen.fill((200, 200, 200))

		self.env = env.Environment(grid_size)

	def play(self):
		time_previous_update = pygame.time.get_ticks()
		action = env.Action.MAINTAIN
		while not self.env.done:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						action = env.Action.TURN_LEFT

					if event.key == pygame.K_RIGHT:
						action = env.Action.TURN_RIGHT

				if event.type==pygame.locals.QUIT:
					pygame.quit()
					sys.exit()

			current_time = pygame.time.get_ticks()
			if (current_time - time_previous_update) > 300:
				time_previous_update = current_time
				self.env.update(action)
				action = env.Action.MAINTAIN

			self.update_screen()

	def update_screen(self):
		state = self.env.get_state()
		for x in range(self.env.grid_size):
			for y in range(self.env.grid_size):
				coordinates = pygame.Rect(x*self.CELL_SIZE, y*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
				
				if state[x, y] == 0.: 
					pygame.draw.rect(self.screen, (200, 200, 200), coordinates)
				elif (state[x, y] == 1.) | (state[x, y] == 2.):
					pygame.draw.rect(self.screen, (255, 0, 0), coordinates)
				else:
					pygame.draw.rect(self.screen, (0, 0, 255), coordinates)
		
		pygame.display.set_caption('Score: ' + str(self.env.score))

		pygame.display.update()


if __name__ == "__main__":
	game = SnakeGame(10)
	game.play()

