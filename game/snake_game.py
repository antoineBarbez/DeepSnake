from pygame.locals import *

import draw
import environment
import os
import pygame
import sys

class SnakeGame(object):
	CELL_SIZE = 30
	
	def __init__(self, grid_size=10):
		self.env = environment.Environment(grid_size)
		self.grid_size = grid_size

	def play(self, agent=None, repeat=True):
		"""
		Watch a pre-trained agent playing the game or simply play 
		yourself with the keyboard if no agent is specified

		args:
			agent (dqn.DQNAgent): A pre-trained agent
			repeat (boolean): If True: starts a new game when the previous game is done
							  If False: simply closes the window at the end of the game
		"""
		self.__display_screen()

		keep_playing = True
		while keep_playing:
			if agent is not None:
				self.__run_episode_agent(agent)
				agent.state_buffer.reset()
			else:
				self.__run_episode_human()

			self.env.reset()
			keep_playing = repeat

		self.__close_screen()

	def __close_screen(self):
		pygame.quit()
		sys.exit()

	def __display_screen(self):
		pygame.init()
		pygame.display.set_caption('Score: 0')
		self.screen = pygame.display.set_mode((self.CELL_SIZE * self.grid_size, self.CELL_SIZE * self.grid_size))
		self.__update_screen()

	def __run_episode_agent(self, agent):
		"""
		Runs a single episode of the game with the specified agent playing

		args:
			agent (dqn.DQNAgent): A pre-trained agent
		"""
		time_previous_update = pygame.time.get_ticks()
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

	def __run_episode_human(self):
		"""
		Runs a single episode of the game with the user playing with the keyboard
		"""
		action = environment.Action.MAINTAIN
		time_previous_update = pygame.time.get_ticks()
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

