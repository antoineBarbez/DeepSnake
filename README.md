# DeepSnake
A simple implementation of Deep Q-learning for playing the famous Snake game.

<p align="center">
  <img src="https://user-images.githubusercontent.com/32719533/63809535-8f190a80-c8f0-11e9-8a01-01a490fb4b99.gif" width="250px">
</p>

## Training
To train your own agent to play on a 10x10 grid:

```python
import dqn.agent as agent

dqn_agent = agent.DQNAgent(grid_size=10, num_states=2)
dqn_agent.train(save_name="my_model")
```
At the end of the training, the model will be saved in *./dqn/trained_models/*.

Note that this code uses the default configuration but you can modify any of the learning 
parameters of the *train()* function, e.g., *num_steps*, *batch_size*, *learning_rate* etc...

## Playing
To watch a pre-trained agent playing the game:

```python
import dqn.agent as agent
import game.snake_game as game 

dqn_agent = agent.DQNAgent(grid_size=10)
dqn_agent.load_model("dqn-10x10x2")

snake_game = game.SnakeGame(grid_size=10)
snake_game.play(dqn_agent)
```

You can also play the game on your own using the keyboard arrows:

```python
import game.snake_game as game

snake_game = game.SnakeGame(grid_size=10)
snake_game.play()
```