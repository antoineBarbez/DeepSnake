
import numpy as np

import random

class Environment(object):
	def __init__(self, grid_size):
		self.grid_size = grid_size
		self.reset()

	def get_state(self):
		state = np.zeros((self.grid_size, self.grid_size))

		for point in self.snake_body:
			state[point.x, point.y] = 1

		state[self.snake_head.x, self.snake_head.y] = 2
		state[self.prey.x, self.prey.y] = 3

		return state

	def reset(self):
		self.score = 0

		self.done = False
		
		self.snake_body = []
		self.snake_head = Point(0, 1)
		self.snake_direction = Point(1, 0)
		self.prey = self.__get_new_prey_position()

	def update(self, action):
		# Update snake direction
		if action == Action.TURN_LEFT:
			if self.snake_direction.x == 0:
				self.snake_direction.x = self.snake_direction.y
				self.snake_direction.y = 0
			else:
				self.snake_direction.y = - self.snake_direction.x
				self.snake_direction.x = 0

		if action == Action.TURN_RIGHT:
			if self.snake_direction.x == 0:
				self.snake_direction.x = - self.snake_direction.y
				self.snake_direction.y = 0
			else:
				self.snake_direction.y = self.snake_direction.x
				self.snake_direction.x = 0

		# Update snake position
		self.snake_head.x += self.snake_direction.x
		self.snake_head.y += self.snake_direction.y
		self.snake_body.append(Point(self.snake_head.x - self.snake_direction.x, self.snake_head.y - self.snake_direction.y))

		if (self.snake_head == self.prey):
			self.score += 1
			self.prey = self.__get_new_prey_position()
		else:
			self.snake_body.pop(0)

		self.done = self.__is_done()

	def __get_new_prey_position(self):
		position = Point(random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))

		if (position in self.snake_body) | (position == self.snake_head):
			return self.__get_new_prey_position()
		else:
			return position

	def __is_done(self):
		# The snake touch the environment's boundaries
		if (self.snake_head.x < 0) | (self.snake_head.x >= self.grid_size) | (self.snake_head.y < 0) | (self.snake_head.y >= self.grid_size):
			return True

		# The snake "bite" it's own body
		if self.snake_head in self.snake_body:
			return True

		return False

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, other):
		return (self.x, self.y) == (other.x, other.y)

	def __ne__(self, other):
		return not(self == other)

class Action(object):
	MAINTAIN   = 0
	TURN_LEFT  = 1
	TURN_RIGHT = 2



