#! /usr/bin/env python3
import tempfile, subprocess
import sys, os
import time
import filecmp
import random
#from multiprocessing import Process

# Our modules
import testWriteSpecChar as tWSC
import modetrack

EDITOR = os.environ.get('EDITOR', 'vim')

class VimGolfer():

    def __init__(self, challenge, visible=False):
        self.start_file, self.end_file = self.getChallenge(challenge)
#        self.commands = [[' '], ['!'], ['"'], ['#'], ['$'], ['%'], ['&'], ["'"], ['('],
#                     [')'], ['*'], ['+'], [','], ['-'], ['.'], ['/'], ['0'], ['1'], ['2'], ['3'], ['4'], 
#                     ['5'], ['6'], ['7'], ['8'], ['9'], [':'], [';'], ['<'], ['='], ['>'], ['?'], ['@'],
#                     ['['], ['\\'], [']'], ['^'], ['_'], ['`'], ['a'], ['b'], ['c'], ['d'], ['e'],['f'],
#                     ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'],
#                     ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'], ['{'], ['|'], ['}'], ['~'], 
#                     ['A'], ['B'], ['C'], ['D'], ['E'],['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'],
#                     ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'],
#                     ['Y'], ['Z'],
#                     ['`bac'], ['`ent'], ['`esc'], ['d', 'w'], ['d', 'd'], ['d', 'b'], ['d', 'e'], ['y', 'y']
#                     ]
        self.commands = [' ', '!', '"', '#', '$', '%', '&', "'", '(',
                     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', 
                     '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
                     '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e','f',
                     'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                     's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 
                     'A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K', 'L',
                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                     'Y', 'Z',
                     '`bac', '`ent', '`esc', 'dw', 'dd', 'db', 'de', 'yy'
                     ]
        self.actions_num = len(self.commands)
        a = 1

        self.states = {'dictCurrFile' : dict(type='int', shape=(80*80), num_states=256), 'dictEndFile' : dict(type='int', shape=(80*80),\
        num_states=256), 'dictMode' : dict(type='int', shape=1, num_states=4), 'dictCursor' : dict(type='int', shape=2, num_states=80),\
        'dictPrevActions' : dict(type='int', shape=100, num_states=len(self.commands))}
        self.command_list = []
        self.reset()

    def getChallenge(self, challenge):
        if challenge == 'OneNumberPerLine':
            return os.path.normpath('vimgolf_challenges/{}/start.txt'.format(challenge)), os.path.normpath('vimgolf_challenges/{}/end.txt'.format(challenge))
        else:
            raise ChallengeError('Not a valid challenge')

    # Reset the environment
    def reset(self):
        text_list = []
        with open(self.start_file, 'r') as file:
            for line in file:
                text_list.append(line)
        self.text_list = text_list
        self.command_list = []

    def setup(self):
        with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
            for line in self.text_list:
                tmp.write(str.encode(line))
            tmp.flush()
        self.tempfile = tmp
        return tmp

    def runVim(self):
        # Create temporary file with the contents of the start file
        tempfile = self.setup()

        # For reference/testing
        #master_command_list = ['i', '`esc', 'd', 'd', 'y', 'y', 'p', 'f', '-', 'i', '`bac', '`bac', '`bac', '`esc', ':', 'q', '!', '`ent', 'DONE']
        master_command_list = ['d', 'j', 'q', 'q', 'f', ',', 'r', '`ent', 'q', '2', '@', 'q', 'l', 'x', 'j', '3', '@', 'q', 'd', 'd', '3', '@', 'q', 'd', 'd']

        # Create the script in here
        command_string = ''.join(self.command_list)
        scriptin = 'scriptin'
        tWSC.writeChars(scriptin, command_string)
        modelist = modetrack.fun(self.command_list)
        print(self.command_list)
        print(modelist)

# Legacy code for multiprocess. 
#                vimgolf = Process(target = lambda: subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout]))
#                vimgolf.start()

        # Run through the commands
        # Don't really need scriptout, but we will leave this incase
        #subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout])
        subprocess.call([EDITOR, tempfile.name, '-s', scriptin])

        print('=================Start of File=================')
        os.system('more {}'.format(tempfile.name))
        print('==================End of File==================')

        coords = []
        if self.command_list:
            with open('posout', 'r') as posfile:
                for line in posfile:
                    line = line.strip()
                    if line:
                        coords.append(line)
        else:
            coords.append(1)
            coords.append(1)
        print('Ending coords: {}\n\n'.format(coords))

        # For reference (Things that we must do at the end of executing vim commands, this code is founded)
        #    press('Esc')
        #    typewrite(':w | :set cmdheight=2 | redir! > posout | echo line(".") | echo col(".") | redir END')
        #    press('enter')

    # Return a reward for an action given a state
    def getReward(self, state):
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

    # Return a tuple (state, reward, terminal)
    def act(self, action):
        self.command_list.append(action)
        self.runVim()
        # Temp value for state
        state = 0
        # Get a reward
        reward = self.getReward(state)
        terminal = self.fileCompare()
        self.cleanUp()
        return state, reward, terminal


if __name__ == '__main__':
    vim_inst = VimGolfer('OneNumberPerLine')
    print(vim_inst.start_file)
    print(vim_inst.end_file)
    vim_inst.act('i')