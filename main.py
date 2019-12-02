#! /usr/bin/env python3.6
import tempfile, subprocess
import sys, os
import queue
import numpy as np
import time
import filecmp
import random
from multiprocessing import Process

# Our modules
import testWriteSpecChar as tWSC
import modetrack
from vim_environ import VimEnviron

# tensorforce modules
from tensorforce.environments import Environment
from tensorforce.environments import MazeExplorer
from tensorforce.execution import Runner
from tensorforce.agents import Agent
from tensorforce.agents import DeepQNetwork

def main(repeat, max_episode_timesteps):
    #v = VimEnviron('OneNumberPerLine')
    v = VimEnviron('ViceVersa')
    environment = Environment.create(environment=v)
    for _ in range(repeat, max_episode_timesteps):
        agent_kwargs = dict()
        if max_episode_timesteps is not None:
            assert environment.max_episode_timesteps() is None or \
                environment.max_episode_timesteps() == max_episode_timesteps
            agent_kwargs['max_episode_timesteps'] = max_episode_timesteps
#DeepQNetwork
        agent = Agent.create(agent='ppo1.json', environment=environment, **agent_kwargs)
#        print(agent)
#        agent.initialize()
#        agent.reset()
#        actions = agent.act(environment.reset())
#        print(actions)
#        states, terminal, reward = environment.execute(actions=actions)
#        print(states, terminal, reward)
#        agent.observe(terminal=terminal, reward=reward)
#        actions = agent.act(states)
#        print(actions)
#        states, terminal, reward = environment.execute(actions=actions)
#        print(states, terminal, reward)
#        agent.observe(terminal=terminal, reward=reward)
#        actions = agent.act(states)
#        print(actions)
#        states, terminal, reward = environment.execute(actions=actions)
#        print(states, terminal, reward)
#        agent.observe(terminal=terminal, reward=reward)
#        return

        runner = Runner(agent=agent, environment=environment)
        runner.run(
            num_timesteps=100, num_episodes=100,
            max_episode_timesteps=100#, callback=callback,
            #mean_horizon=args.mean_horizon, evaluation=args.evaluation
            # save_best_model=args.save_best_model
            #Changed to 100 and 1
        )
        runner.close()

if __name__ == '__main__':
#    print(sys.argv[1])
#    print(sys.argv[2])
#    print(sys.argv[3])
    #main(sys.argv[1], sys.argv[2], sys.argv[3])
    #main(1, 'start.txt', 'end.txt', 'scriptout')
    main(repeat=300, max_episode_timesteps=500)
