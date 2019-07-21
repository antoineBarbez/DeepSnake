
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

import environment
import model
import random

class StateBuffer(object):
	def __init__(self, grid_size, buffer_size):
		self.states = np.zeros((grid_size, grid_size, buffer_size))

	def add(self, state):
		state_expanded = np.expand_dims(state, axis=-1)
		self.states = np.concatenate((state_expanded, self.states), axis=-1)
		self.states = np.delete(self.states, -1, -1)

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

# Returns the mean score achieved on a number of test episodes.
def test_model(session, env, model, num_test_episodes = 20):
	scores = []
	max_step = 100 
	for i in range(num_test_episodes):
		env.reset()

		state_buffer = StateBuffer(grid_size, nb_states)
		state_buffer.add(env.get_state())
		s = state_buffer.states
		step=0
		while step<max_step:
			step +=1
			a = session.run(model.predict_action, feed_dict={model.input:np.expand_dims(s, axis=0)})[0]
			env.update(a)

			if env.done:
				scores.append(env.score)
				break
			else:
				state_buffer.add(env.get_state())
				s = state_buffer.states

			if step == max_step:
				scores.append(env.score)
			
	return np.mean(np.array(scores))

if __name__ == "__main__":
	tf.reset_default_graph()

	grid_size = 10
	nb_states = 2

	num_episodes = 10000
	start_e = 1.0
	lr = 0.001
	y = 0.9
	batch_size = 50

	env = environment.Environment(grid_size)
	dqn = model.SnakeDQN(grid_size, nb_states)

	experience_buffer = ExperienceBuffer(state_shape=(grid_size, grid_size, nb_states))

	losses = []
	with tf.Session() as session:
		session.run(tf.global_variables_initializer())

		e = start_e
		for i in range(num_episodes):
			env.reset()

			e = start_e - start_e*i/num_episodes

			state_buffer = StateBuffer(grid_size, nb_states)
			state_buffer.add(env.get_state())
			s = state_buffer.states
			while not env.done:
				# Choose an action (random with a chance e)
				if np.random.rand(1) < e:
					a = np.random.randint(0,3)
				else:
					a = session.run(dqn.predict_action, feed_dict={dqn.input:np.expand_dims(s, axis=0)})[0]
					
				score = env.score
				env.update(a)
				if env.done:
					state_buffer.add(np.zeros((grid_size, grid_size)))
					r = -1.
				else:
					state_buffer.add(env.get_state())
					r = env.score - score

				s1 = state_buffer.states
				experience_buffer.add(s, a, r, s1, env.done)
				s = s1

			if len(experience_buffer.buffer) >= batch_size:
				batch = experience_buffer.get_batch(batch_size)

				next_Q = session.run(dqn.output_Q, feed_dict={dqn.input:batch['state_next']}) 
				target_Q = session.run(dqn.output_Q, feed_dict={dqn.input:batch['state']})
				target_Q[range(batch_size), batch['action']] = batch['reward'] + y*(1 - batch['done'])*np.max(next_Q, axis=1)
				
				# Update model
				session.run(
					dqn.update_model, 
					feed_dict={
						dqn.input: batch['state'],
						dqn.target_Q: target_Q,
						dqn.learning_rate: lr})

				loss = session.run(dqn.loss, feed_dict={dqn.input: batch['state'], dqn.target_Q: target_Q})
				losses.append(loss)

			if i%100 == 0:
				print("Episode: " + str(i) + ", Score: " + str(test_model(session, env, dqn)))

	plt.figure()
	plt.plot(range(len(losses)), losses)
	plt.show()





