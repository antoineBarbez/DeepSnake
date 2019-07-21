
import tensorflow as tf

class SnakeDQN(object):
	def __init__(self, grid_size, num_states):
		"""
		args:
			grid_size: size of the environment's grid
			num_states: number of last states the agent considers as input
		"""

		self.input = tf.placeholder(tf.float32, [None, grid_size, grid_size, num_states], name="input")

		conv_1 = tf.layers.conv2d(
			inputs=self.input,
			filters=16,
			kernel_size=(2, 2),
			strides=(1, 1),
			padding="valid",
			activation=tf.nn.relu,
			kernel_initializer=tf.contrib.layers.xavier_initializer())

		conv_2 = tf.layers.conv2d(
			inputs=conv_1,
			filters=32,
			kernel_size=(2, 2),
			strides=(1, 1),
			padding="valid",
			activation=tf.nn.relu,
			kernel_initializer=tf.contrib.layers.xavier_initializer())

		conv_2_flat = tf.layers.flatten(conv_2)

		hidden = tf.layers.dense(
			inputs=conv_2_flat,
			units=128,
			activation=tf.nn.relu,
			kernel_initializer=tf.contrib.layers.xavier_initializer())

		self.output_Q = tf.layers.dense(
			inputs=hidden,
			units=3)

		# Prediction
		self.predict_action = tf.argmax(self.output_Q, 1)

		# Training
		self.target_Q = tf.placeholder(tf.float32, [None, 3])
		self.learning_rate = tf.placeholder(tf.float32, name="learning_rate")
		self.loss = tf.losses.mean_squared_error(self.target_Q, self.output_Q)
		self.update_model = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)




