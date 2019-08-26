import numpy as np

import random

class ExperienceBuffer():
	def __init__(self, state_shape, buffer_size = 10000):
		self.buffer = []
		self.buffer_size = buffer_size
		self.state_shape = state_shape

	def add(self, state, action, reward, state_next, done):
		if len(self.buffer) >= self.buffer_size:
			self.buffer.pop(0)

		experience = np.concatenate([
			state.flatten(),
			np.array(action).flatten(),
			np.array(reward).flatten(),
			state_next.flatten(),
			np.array(int(done)).flatten()
		])

		self.buffer.append(experience)

	def get_batch(self, size):
		batch_size = min(len(self.buffer), size)
		state_size = np.prod(self.state_shape)
		
		experiences = np.array(random.sample(self.buffer, batch_size))
		
		batch = {}
		batch['state'] = experiences[:, :state_size].reshape((batch_size, ) + self.state_shape)
		batch['action'] = np.cast['int'](experiences[:, state_size])
		batch['reward'] = experiences[:, state_size + 1]
		batch['state_next'] = experiences[:, state_size + 2:2 * state_size + 2].reshape((batch_size, ) + self.state_shape)
		batch['done'] = experiences[:, 2 * state_size + 2]

		return batch