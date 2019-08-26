from pygame.locals import *

import draw
import environment
import os
import pygame
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

import dqn.agent

class SnakeGame(object):
	CELL_SIZE = 30
	
	def __init__(self, grid_size=10):
		self.env = environment.Environment(grid_size)
		self.grid_size = grid_size

	def __display_screen(self):
		pygame.init()
		pygame.display.set_caption('Score: 0')
		self.screen = pygame.display.set_mode((self.CELL_SIZE * self.grid_size, self.CELL_SIZE * self.grid_size))
		self.__update_screen()

	def __update_screen(self):
		state = self.env.get_state()
		for x in range(self.env.grid_size):
			for y in range(self.env.grid_size):
				draw.background(self.screen, x, y, self.CELL_SIZE)
				
				if (state[x, y] == 1) | (state[x, y] == 2):
					draw.snake_cell(self.screen, x, y, self.CELL_SIZE)
				elif state[x, y] == 3:
					draw.prey(self.screen, x, y, self.CELL_SIZE)
		
		pygame.display.set_caption('Score: ' + str(self.env.score))
		pygame.display.update()

	def __close_screen(self):
		pygame.quit()
		sys.exit()

	def play(self):
		self.__display_screen()

		time_previous_update = pygame.time.get_ticks()
		action = environment.Action.MAINTAIN
		
		while not self.env.done:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						action = environment.Action.TURN_LEFT

					if event.key == pygame.K_RIGHT:
						action = environment.Action.TURN_RIGHT

					if event.key == pygame.K_ESCAPE:
						self.__close_screen() 

				if event.type == pygame.locals.QUIT:
					self.__close_screen()

			current_time = pygame.time.get_ticks()
			if (current_time - time_previous_update) > 300:
				self.env.update(action)
				action = environment.Action.MAINTAIN
				time_previous_update = current_time

				if not self.env.done:
					self.__update_screen()

		self.__close_screen()

	def play_agent(self, model_name):
		self.__display_screen()

		time_previous_update = pygame.time.get_ticks()
		agent = dqn.agent.DQNAgent(self.grid_size, 2)
		agent.load_model(model_name)		
		while not self.env.done:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.__close_screen()

				if event.type==pygame.locals.QUIT:
					self.__close_screen()

			current_time = pygame.time.get_ticks()
			if (current_time - time_previous_update) > 200:
				action = agent.get_action(self.env.get_state())
				self.env.update(action)
				time_previous_update = current_time

				if not self.env.done:
					self.__update_screen()

		self.__close_screen()

