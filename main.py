#! /usr/bin/python3
import tempfile, subprocess
import sys, os
import queue
import numpy as np
import time
import filecmp
import random
from multiprocessing import Process
from pyautogui import press, typewrite

# Our modules
import testWriteSpecChar as tWSC
import modetrack
from vim_environ import VimEnviron

# tensorforce modules
from tensorforce.environments import Environment
from tensorforce.execution import Runner
from tensorforce.agents import DeepQNetwork

vim_commands_list = ['h', 'j', 'k', 'l', 'i', 'I', 'a', 'A', 'o', 'O', 's', 'S',
                     '.', 'b', 'db', 'w', 'dw', 'e', 'de', 'yy', 'p', 'x',
                     ':']
keyboard_commands = ['\t', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
                     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                     '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                     'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 
                     'backspace', 'capslock', 'ctrl', 'ctrlleft', 'ctrlright', 'del', 'delete',
                     'down', 'enter', 'esc', 'escape', 'help', 'home', 'insert', 'left', 'return',
                     'right', 'shift', 'shiftleft', 'shiftright', 'space', 'tab', 'up', 'command',
                     'option', 'optionleft', 'optionright']

EDITOR = os.environ.get('EDITOR', 'vim')

class environment:
    def __init__(self, start_file, end_file):
        text_list = []
        self.start_file = start_file
        self.end_file = end_file
        with open(start_file, 'r') as file:
            for line in file:
                text_list.append(line)
        self.text_list = text_list
        self.normal_mode = [[' '], ['!'], ['"'], ['#'], ['$'], ['%'], ['&'], ["'"], ['('],
                     [')'], ['*'], ['+'], [','], ['-'], ['.'], ['/'], ['0'], ['1'], ['2'], ['3'], ['4'], 
                     ['5'], ['6'], ['7'], ['8'], ['9'], [':'], [';'], ['<'], ['='], ['>'], ['?'], ['@'],
                     ['['], ['\\'], [']'], ['^'], ['_'], ['`'], ['a'], ['b'], ['c'], ['d'], ['e'],['f'],
                     ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'],
                     ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['{'], ['|'], ['}'], ['~'], 
                     ['A'], ['B'], ['C'], ['D'], ['E'],['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'],
                     ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'],
                     ['Y'], ['Z'],
                     ['`bac'], ['`ent'], ['`esc'], ['d', 'w'], ['d', 'd'], ['d', 'b'], ['d', 'e'], ['y', 'y']
                     ]
        self.visual_mode = [[' '], ['!'], ['"'], ['#'], ['$'], ['%'], ['&'], ["'"], ['('],
                     [')'], ['*'], ['+'], [','], ['-'], ['.'], ['/'], ['0'], ['1'], ['2'], ['3'], ['4'], 
                     ['5'], ['6'], ['7'], ['8'], ['9'], [':'], [';'], ['<'], ['='], ['>'], ['?'], ['@'],
                     ['['], ['\\'], [']'], ['^'], ['_'], ['`'], ['a'], ['b'], ['c'], ['d'], ['e'],['f'],
                     ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'],
                     ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['{'], ['|'], ['}'], ['~'], 
                     ['A'], ['B'], ['C'], ['D'], ['E'],['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'],
                     ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'],
                     ['Y'], ['Z'],
                     ['`bac'], ['`ent'], ['`esc']
                     ]
        self.insertion_mode = [[' '], ['!'], ['"'], ['#'], ['$'], ['%'], ['&'], ["'"], ['('],
                     [')'], ['*'], ['+'], [','], ['-'], ['.'], ['/'], ['0'], ['1'], ['2'], ['3'], ['4'], 
                     ['5'], ['6'], ['7'], ['8'], ['9'], [':'], [';'], ['<'], ['='], ['>'], ['?'], ['@'],
                     ['['], ['\\'], [']'], ['^'], ['_'], ['`'], ['a'], ['b'], ['c'], ['d'], ['e'],['f'],
                     ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'],
                     ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['{'], ['|'], ['}'], ['~'], 
                     ['A'], ['B'], ['C'], ['D'], ['E'],['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'],
                     ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'],
                     ['Y'], ['Z'],
                     ['`bac'], ['`ent'], ['`esc']
                     ]
        self.command_mode = [[' '], ['!'], ['"'], ['#'], ['$'], ['%'], ['&'], ["'"], ['('],
                     [')'], ['*'], ['+'], [','], ['-'], ['.'], ['/'], ['0'], ['1'], ['2'], ['3'], ['4'], 
                     ['5'], ['6'], ['7'], ['8'], ['9'], [':'], [';'], ['<'], ['='], ['>'], ['?'], ['@'],
                     ['['], ['\\'], [']'], ['^'], ['_'], ['`'], ['a'], ['b'], ['c'], ['d'], ['e'],['f'],
                     ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'],
                     ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['{'], ['|'], ['}'], ['~'], 
                     ['A'], ['B'], ['C'], ['D'], ['E'],['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'],
                     ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'],
                     ['Y'], ['Z'],
                     ['`bac'], ['`ent'], ['`esc']
                     ]

    def setup(self):
        with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
            for line in self.text_list:
                tmp.write(str.encode(line))
            tmp.flush()
        self.tempfile = tmp
        return tmp

    # Return a reward for an action given a state
    def getReward(self):
        pass

    # Return an action for a given state
    def getAction(self, mode):
        # Random percent chance of choosing an action for exploration
        if random.random() <= 0.10:
            rand_index = random.randint(0, len(mode))
            if mode == 'v':
                action = self.visual_mode[rand_index]
            if mode == 'n':
                action = self.normal_mode[rand_index]
            if mode == 'i':
                action = self.insertion_mode[rand_index]
            if mode == 'c':
                action = self.command_mode[rand_index]
        # Else, use a method based around cost/etc
        else:
            pass
        print(rand_index)
        print(action)
        return action

    def fileCompare(self):
        # Check if files are the same
        if filecmp.cmp(self.tempfile.name, self.end_file):
            return True
        else:
            return False

    def cleanUp(self):
        self.tempfile.close()
        os.remove(self.tempfile.name)
        print('Closed and removed the temp file')
        return


def main(repeat, max_episode_timesteps):
    environment = Environment.create(environment=VimEnviron)
    for _ in range(repeat, max_episode_timesteps):
        agent_kwargs = dict()
        if max_episode_timesteps is not None:
            assert environment.max_episode_timesteps() is None or \
                environment.max_episode_timesteps() == max_episode_timesteps
            agent_kwargs['max_episode_timesteps'] = max_episode_timesteps
        agent = Agent.create(agent=DeepQNetwork, environment=environment, **agent_kwargs)
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
            num_timesteps=args.timesteps, num_episodes=args.episodes,
            max_episode_timesteps=args.max_episode_timesteps, callback=callback,
            mean_horizon=args.mean_horizon, evaluation=args.evaluation
            # save_best_model=args.save_best_model
        )
        runner.close()
    
#
#    # Iterate over the number of attempts
#    for i in range(0, attempts):
#        # Create environment with the contents of the start file
#        env = environment(start_file, end_file)
#        q = queue.Queue()
#        golfing = True
#
#        # For reference/testing
#        #master_command_list = ['i', '`esc', 'd', 'd', 'y', 'y', 'p', 'f', '-', 'i', '`bac', '`bac', '`bac', '`esc', ':', 'q', '!', '`ent', 'DONE']
#        master_command_list = ['d', 'j', 'q', 'q', 'f', ',', 'r', '`ent', 'q', '2', '@', 'q', 'l', 'x', 'j', '3', '@', 'q', 'd', 'd', '3', '@', 'q', 'd', 'd']
#        for command in master_command_list:
#            q.put(command)
#
#        command_list = [] 
#        same_files = False
#        while golfing:
#            if command_list:
#                tempfile = env.setup()
#                #time.sleep(1)
#                print('Number of commands (cost):  {}'.format(len(command_list)))
#
#                # Create the script in here
#                command_string = ''.join(command_list)
#                scriptin = 'scriptin'
#                tWSC.writeChars(scriptin, command_string)
##                with(open('scriptin', 'r')) as f:
##                    for line in f:
##                        print(line)
#                modelist = modetrack.fun(command_list)
#                print(command_list)
#                print(modelist)
#
#                # Run through the commands
##                vimgolf = Process(target = lambda: subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout]))
##                vimgolf.start()
#                subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout])
#
#                # Check if files are the same
#                same_files = env.fileCompare()
#
#                print('=================Start of File=================')
#                os.system('more {}'.format(tempfile.name))
#                print('==================End of File==================')
#                env.cleanUp()
#
#
#            coords = []
#            if command_list:
#                with open('posout', 'r') as posfile:
#                    for line in posfile:
#                        line = line.strip()
#                        if line:
#                            coords.append(line)
#            else:
#                coords.append(1)
#                coords.append(1)
#            print('Ending coords: {}\n\n'.format(coords))
#
#            # Get a new command if queue is empty
#            if q.empty():
#                if same_files:
#                    next_command = 'DONE'
#                else:
#                    next_command = env.getAction()
#            # Fetch one from the queue
#            else:
#                next_command = q.get()
#            command_list.append(next_command)
#            
#            if next_command == 'DONE':
#                golfing = False
#
#        # Final Output
#        print('\nFinal Output for iteration {}'.format(i))
#        print('Number of commands (cost):  {}'.format(len(command_list) + 1))
#        print('AI\'s commands:')
#        print(command_list)
#
#            # For reference
#        #    press('Esc')
#        #    typewrite(':w | :set cmdheight=2 | redir! > posout | echo line(".") | echo col(".") | redir END')
#        #    press('enter')

      

if __name__ == '__main__':
#    print(sys.argv[1])
#    print(sys.argv[2])
#    print(sys.argv[3])
    #main(sys.argv[1], sys.argv[2], sys.argv[3])
    #main(1, 'start.txt', 'end.txt', 'scriptout')
    main(repeat=300, max_episode_timesteps=500)
