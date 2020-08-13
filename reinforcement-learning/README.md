## Reinforcement Learning

![alt text](../images/state.jpg?raw=true)

Deep Q learning algorithm is used to train the RL agent. The state at each time step is the price movement prediction by the LSTM model and price difference and number of days holding the stock. This state will then be passed on to the agent model which outputs the action values for that particular state. The agent follows an epsilon greedy policy in choosing actions. 