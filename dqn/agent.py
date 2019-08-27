import tensorflow as tf 
import numpy as np

import experience_replay
import model
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

import game.environment
 
class StateBuffer(object):
	def __init__(self, grid_size, buffer_size):
		"""
		Class used to store a given number of consecutive states
		Used to construct the input of the DQN
		
		args:
			grid_size (int):
				Size of the environment's grid
			buffer_size (int):
				Number of states to be stored in the buffer
		"""
		self.grid_size = grid_size
		self.buffer_size = buffer_size
		self.reset()

	def reset(self):
		"""
		Resets the buffer with "zero states"
		"""
		self.states = np.zeros((self.grid_size, self.grid_size, self.buffer_size))

	def add(self, state):
		"""
		Add a new state on top of the stack and remove the bottom state
		"""
		state_expanded = np.expand_dims(state, axis=-1)
		self.states = np.concatenate((state_expanded, self.states), axis=-1)
		self.states = np.delete(self.states, -1, -1)

class DQNAgent(object):
	def __init__(self, grid_size, num_states=2):
		"""
		args:
			grid_size (int):
				Size of the environment's grid
			num_states (int):
				Number of input states to be fed through the model, i.e., the "memory size" of the agent.
				Thus, the input of the model is a (grid_size x grid_size x num_states) tensor containing 
				the "num_states" previous states of the environment
		"""
		tf.reset_default_graph()
		
		self.grid_size = grid_size
		self.num_states = num_states

		self.model = model.SnakeDQN(grid_size, num_states)
		self.saver = tf.train.Saver()
		self.session = tf.Session()
		self.state_buffer = StateBuffer(grid_size, num_states)

	def get_action(self, state):
		self.state_buffer.add(state)
		s = self.state_buffer.states
		return self.session.run(
			self.model.predict_action,
			feed_dict={self.model.input:np.expand_dims(s, axis=0)})[0]

	def load_model(self, model_name):
		save_path = os.path.join(ROOT_DIR, 'dqn', 'trained_models', model_name)
		self.saver.restore(self.session, save_path)

	def __save_model(self, model_name):
		save_path = os.path.join(ROOT_DIR, 'dqn', 'trained_models', model_name)
		self.saver.save(self.session, save_path)

	def train(self, num_steps=25000, batch_size=100, learning_rate=0.001, y=0.9,
		start_e=1.0, end_e=0.05, exploration_steps=20000, save_name="dqn-10x10x2"):
		"""
		Train the agent and save the trained model

		args:
			num_steps (int): 
				Number of training steps
			batch_size (int): 
				Size of the training batch used to update the model with experience replay
			learning_rate (float): 
				Learning rate
			y (float): 
				Discount factor of the target Q-values
			start_e (float): 
				Initial value of the exploration rate
			end_e (float): 
				Final value of the exploration rate
			exploration_steps (int): 
				Number of exploration steps during which the exploration
			 	rate decreases linearly from start_e to end_e
			save_name (string): 
				Name of the trained model to be saved 
		"""

		env = game.environment.Environment(self.grid_size)
		experience_buffer = experience_replay.ExperienceBuffer(state_shape=(self.grid_size, self.grid_size, self.num_states))

		self.session.run(tf.global_variables_initializer())

		e = start_e
		max_step = 200
		for i in range(num_steps):
			if i <= exploration_steps:
				e -= (start_e - end_e)/(exploration_steps)
			
			env.reset()
			self.state_buffer.reset()
			self.state_buffer.add(env.get_state())
			s = self.state_buffer.states
			step = 0
			while not (env.done or step > max_step):
				step += 1

				# Choose an action (random with a probability e)
				if np.random.rand(1) < e:
					a = np.random.randint(0,3)
				else:
					a = self.session.run(
						self.model.predict_action, 
						feed_dict={self.model.input:np.expand_dims(s, axis=0)})[0]
					
				score = env.score
				env.update(a)
				
				if env.done:
					self.state_buffer.add(np.zeros((self.grid_size, self.grid_size)))
					r = -1.
				else:
					self.state_buffer.add(env.get_state())
					r = env.score - score

				s1 = self.state_buffer.states
				experience_buffer.add(s, a, r, s1, env.done)
				s = s1

			if len(experience_buffer.buffer) >= batch_size:
				batch = experience_buffer.get_batch(batch_size)

				next_Q = self.session.run(self.model.output_Q, feed_dict={self.model.input:batch['state_next']}) 
				target_Q = self.session.run(self.model.output_Q, feed_dict={self.model.input:batch['state']})
				target_Q[range(batch_size), batch['action']] = batch['reward'] + y*(1 - batch['done'])*np.max(next_Q, axis=1)
				
				# Update model
				self.session.run(
					self.model.update_model, 
					feed_dict={
						self.model.input: batch['state'],
						self.model.target_Q: target_Q,
						self.model.learning_rate: learning_rate})

			if i%100 == 0:
				test_score = self.__test_agent()
				print("Episode: {0}, Score: {1}".format(i, test_score))

		if save_name != None:
			self.__save_model(save_name)


	def __test_agent(self, num_test_episodes = 20):
		"""
		Returns the mean score achieved by the agent on a given number of test episodes.

		args:
			num_test_episodes: the number of test game episodes

		Returns: 
			the mean score achieved by the agent on the test episodes 
		"""

		env = game.environment.Environment(self.grid_size)
		max_step = 200
		
		scores = []
		for i in range(num_test_episodes):
			env.reset()
			self.state_buffer.reset()
			
			step = 0
			while step < max_step:
				step +=1
				a = self.get_action(env.get_state())
				env.update(a)

				if env.done:
					scores.append(env.score)
					break

				if step == max_step:
					scores.append(env.score)
				
		return np.mean(np.array(scores))




