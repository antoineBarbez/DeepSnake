
import numpy as np

import random

class Environment(object):
	def __init__(self, grid_size=10):
		self.grid_size = grid_size
		self.reset()

	def get_state(self):
		state = numpy.zeros((self.grid_size, self.grid_size))

		# Body of the snake
		state[self.snake_position_x[:-1], self.snake_position_y[:-1]] = 1
		
		# Head of the snake
		state[self.snake_position_x[-1], self.snake_position_y[-1]] = 2
		
		# Prey
		state[self.prey_position_x, self.prey_position_y] = 3

		return state

	def reset(self):
		self.done = False

		self.score = 0
		
		self.snake_position_x = [0]
		self.snake_position_y = [0]
		self.snake_direction_x = 0
		self.snake_direction_y = 0

		self.prey_position_x, self.prey_position_y = self.__get_new_prey_position()

	def update(self, action):
		# Update snake direction
		snake_direction_x = self.snake_direction_x
		if action == action.LEFT:
			self.snake_direction_x = - self.snake_direction_y
			self.snake_direction_y = - snake_direction_x

		if action == action.RIGHT:
			self.snake_direction_x = self.snake_direction_y
			self.snake_direction_y = snake_direction_x

		# Update snake position
		self.snake_position_x.append(self.snake_position_x[-1] + self.snake_direction_x)
		self.snake_position_y.append(self.snake_position_y[-1] + self.snake_direction_y)

		if (self.snake_position_x[-1] == self.prey_position_x) & (self.snake_position_y[-1] == self.prey_position_y):
			self.score += 1
			self.prey_position_x, self.prey_position_y = self.__get_new_prey_position()
		else:
			self.snake_position_x.pop(0)
			self.snake_position_y.pop(0)

		self.done = self.__is_done()

	def __get_new_prey_position(self):
		x = random.randint(0, 9)
		y = random.randint(0, 9)

		if (x in self.snake_position_x) & (y in self.snake_position_y):
			return self.__get_new_mouse_position()
		else:
			return x, y

	def __is_done(self):
		snake_head_x = self.snake_position_x[-1]
		snake_head_y = self.snake_position_y[-1]

		# The snake touch the environment's boundaries
		if (snake_head_x < 0) | (snake_head_x >= self.grid_size) | (snake_head_y < 0) | (snake_head_y >= grid_size):
			return True

		# The snake "bite" it's own body
		for i in np.where(self.snake_position_x[:-1] == snake_head_x, self.snake_position_x[:-1]):
			if self.snake_position_y[i] == snake_head_y:
				return True

		return False



