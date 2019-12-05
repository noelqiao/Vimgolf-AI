#! /usr/bin/env python3
import tempfile, subprocess
import sys, os
import time
import filecmp
import random
import codecs
import numpy as np
#from multiprocessing import Process

# Our modules
import testWriteSpecChar as tWSC
import modetrack
from rewardCalculate import calReward
from state2array import state2array
from text2ASCII import text2AsciiArray
from command2ASCII import command2AsciiArray

EDITOR = os.environ.get('EDITOR', 'vim')

class VimGolfer():

    def __init__(self, challenge, visible=False):
        self.start_file, self.end_file = self.getChallenge(challenge)
#        self.commands = [' ', '!', '"', '#', '$', '%', '&', "'", '(',
#                     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', 
#                     '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
#                     #'[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e','f',
#                     '[', '\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e','f',
#                     'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
#                     's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 
#                     'A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K', 'L',
#                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
#                     'Y', 'Z',
#                     '`bac', '`ent', '`esc', 'dw', 'dd', 'db', 'de', 'yy'
#                     ]
#        self.commands = [' ', '!', '"', '#', '$', '%', '&', "'", '(',
#                     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', 
#                     '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@',
#                     '[', '\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e','f',
#                     'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
#                     's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 
#                     'A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K', 'L',
#                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
#                     'Y', 'Z',
#                     '`bac', '`ent', '`esc'
#                     ]
        self.commands = [' ', '$', '%',
                     ',', '.', '0', '1', '2', '3', '4', 
                     '5', '6', '7', '8', '9', '@',
                     '^', 'a', 'b', 'c', 'd', 'e','f',
                     'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                     's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                     'A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K', 'L',
                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                     'Y', 'Z',
                     '`bac', '`ent', '`esc'
                     ]
        self.actions_num = len(self.commands)
        self.modelist = [0]
        self.reward = 0
        a = 1

        self.fileshape_col = 80
        self.fileshape_row = 3

#        self.states = {'dictCurrFile' : dict(type='int', shape=(80*80), num_values=259), 'dictEndFile' : dict(type='int', shape=(80*80),\
#        num_values=259), 'dictState' : dict(type='int', shape=3, num_values=81)}
#        self.states = {'dictCurrFile' : dict(type='int', shape=(self.fileshape_col*self.fileshape_row), num_values=259), 'dictEndFile' : dict(type='int', shape=(self.fileshape_col*self.fileshape_row),\
#        num_values=259), 'dictState' : dict(type='int', shape=3, num_values=81)}
        self.states = {'dictCurrFile' : dict(type='int', shape=(self.fileshape_col*self.fileshape_row), num_values=259), 'dictEndFile' : dict(type='int', shape=(self.fileshape_col*self.fileshape_row),\
                num_values=259), 'dictState' : dict(type='int', shape=3, num_values=81), 'dictHistory' : dict(type='int', shape=50, num_values=258), 'dictModetrack' : dict(type='int', shape=50, num_values=5)}
        
        text_list = []
        with open(self.start_file, 'r') as file:
            for line in file:
                text_list.append(line)
        self.text_list = text_list
        self.state = self.reset()

    def getChallenge(self, challenge):
        if challenge == 'OneNumberPerLine':
            return os.path.normpath('vimgolf_challenges/{}/start.txt'.format(challenge)), os.path.normpath('vimgolf_challenges/{}/end.txt'.format(challenge))
        if challenge == 'ViceVersa':
            return os.path.normpath('vimgolf_challenges/{}/start.txt'.format(challenge)), os.path.normpath('vimgolf_challenges/{}/end.txt'.format(challenge))
        else:
            raise ChallengeError('Not a valid challenge')

    # Reset the environment
    def reset(self):
        self.command_list = []
        vim_array = state2array([1, 1], self.modelist)
        history_array = command2AsciiArray([])
#        start_file_array = text2AsciiArray(codecs.open(self.start_file, 'r', 'utf-8').read(), 80, 80)
#        end_file_array = text2AsciiArray(codecs.open(self.end_file, 'r', 'utf-8').read(), 80, 80)
        start_file_array = text2AsciiArray(codecs.open(self.start_file, 'r', 'utf-8').read(), self.fileshape_row, self.fileshape_col)
        end_file_array = text2AsciiArray(codecs.open(self.end_file, 'r', 'utf-8').read(), self.fileshape_row, self.fileshape_col)

        
        state = np.concatenate((vim_array, start_file_array.flatten()), axis=None)
        #state = {'dictCurrFile' : start_file_array.flatten(), 'dictEndFile' : end_file_array.flatten(), 'dictMode' : np.array(vim_array[2],), 'dictCursor' : [0,0]}
        #state = {'dictCurrFile' : start_file_array.flatten(), 'dictEndFile' : end_file_array.flatten(), 'dictState' : vim_array}
        state = {'dictCurrFile' : start_file_array.flatten(), 'dictEndFile' : end_file_array.flatten(), 'dictState' : vim_array, 'dictHistory' : history_array, 'dictModetrack' : np.full(50, 4).tolist()}
        self.state = state
        return state

    def getState(self):
        coords = []
        with open('posout.txt', 'r') as posfile:
            for line in posfile:
                line = line.strip()
                if line:
                    coords.append(int(line))
        vim_array = state2array(coords, self.modelist)
        history_array = command2AsciiArray(self.command_list)
        modetrack_array = self.modelist +  [4] * (50 - len(self.modelist))
#        temp_file_array = text2AsciiArray(codecs.open(self.tempfile.name, 'r', 'utf-8').read(), 80, 80)
#        end_file_array = text2AsciiArray(codecs.open(self.end_file, 'r', 'utf-8').read(), 80, 80)
        temp_file_array = text2AsciiArray(codecs.open(self.tempfile.name, 'r', 'utf-8').read(), self.fileshape_row, self.fileshape_col)
        end_file_array = text2AsciiArray(codecs.open(self.end_file, 'r', 'utf-8').read(), self.fileshape_row, self.fileshape_col)
        state = np.concatenate((vim_array, temp_file_array.flatten()), axis=None)
        #state = {'dictCurrFile' : temp_file_array.flatten(), 'dictEndFile' : end_file_array.flatten(), 'dictMode' : vim_array[2], 'dictCursor' : coords} 
        #state = {'dictCurrFile' : temp_file_array.flatten(), 'dictEndFile' : end_file_array.flatten(), 'dictState' : vim_array}
        state = {'dictCurrFile' : temp_file_array.flatten(), 'dictEndFile' : end_file_array.flatten(), 'dictState' : vim_array, 'dictHistory' : history_array, 'dictModetrack' : modetrack_array}
        self.state = state
        return state

    def setup(self):
        with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
            for line in self.text_list:
                tmp.write(str.encode(line))
            tmp.flush()
        self.tempfile = tmp
        return tmp

    def runVim(self):
        # Setup the tempfile
        tempfile = self.setup()

        # For reference/testing
        #master_command_list = ['i', '`esc', 'd', 'd', 'y', 'y', 'p', 'f', '-', 'i', '`bac', '`bac', '`bac', '`esc', ':', 'q', '!', '`ent', 'DONE']
        master_command_list = ['d', 'j', 'q', 'q', 'f', ',', 'r', '`ent', 'q', '2', '@', 'q', 'l', 'x', 'j', '3', '@', 'q', 'd', 'd', '3', '@', 'q', 'd', 'd']

        # Create the script in here
        command_string = ''.join(self.command_list)
        scriptin = 'scriptin'
        tWSC.writeChars(scriptin, command_string)
        self.modelist = modetrack.fun(self.command_list)
#        print(self.command_list)
#        print(self.modelist)

# Legacy code for multiprocess. 
#                vimgolf = Process(target = lambda: subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout]))
#                vimgolf.start()

        # Run through the commands
        # Don't really need scriptout, but we will leave this incase
        #subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout])
        subprocess.call([EDITOR, tempfile.name, '-s', scriptin])

#        print('=================Start of File=================')
#        os.system('more {}'.format(tempfile.name))
#        print('==================End of File==================')

        coords = []
        if self.command_list:
            with open('posout.txt', 'r') as posfile:
                for line in posfile:
                    line = line.strip()
                    if line:
                        coords.append(line)
        else:
            coords.append(1)
            coords.append(1)
        #print('Ending coords: {}\n\n'.format(coords))

        # For reference (Things that we must do at the end of executing vim commands, this code is founded)
        #    press('Esc')
        #    typewrite(':w | :set cmdheight=2 | redir! > posout | echo line(".") | echo col(".") | redir END')
        #    press('enter')

    # Return a reward for an action given a state
    def getReward(self):
        self.reward, diffstack = calReward(self.tempfile.name, self.end_file, len(self.command_list))
        return self.reward, diffstack

#    # Return an action for a given state
#    def getAction(self, state, reward):
#        mode = state[2]
#        # Random percent chance of choosing an action for exploration
#        if random.random() <= 0.50:
##            if mode == 2:
##                action = self.visual_mode[random.randint(0, len(self.visual_mode))]
##            if mode == 0:
##                action = self.normal_mode[random.randint(0, len(self.normal_mode))]
##            if mode == 1:
##                action = self.insertion_mode[random.randint(0, len(self.insertion_mode))]
##            if mode == 3:
##                action = self.command_mode[random.randint(0, len(self.command_mode))]
#            action = random.randint(0, len(self.commands)-1)
#        # Else, use a method based around cost/etc
#        else:
#            return 47
#        return action

    def fileCompare(self):
        # Check if files are the same
        if filecmp.cmp(self.tempfile.name, self.end_file):
            return True
        else:
            return False

    def cleanUp(self):
        self.tempfile.close()
        os.remove(self.tempfile.name)
        #print('Closed and removed the temp file')
        return

    def isLegal(self, actions):
        # Always use i_illegal since most keys should be valid in insertion.
        mode = self.modelist[-1]
        action = self.commands[actions]
        i_illegal = ['`']

        # Edit-Distance Modified
        # Delete character, insertion mode
        n_legal = ['x', 'i', 'd', 'y', 'w', 'h', 'j', 'k', 'l', '`esc', '`ent']
        v_legal = ['`esc']
        c_legal = ['`esc']

        if mode == 0:
            if action in n_legal:
                return True
        elif mode == 1:
            if action in i_illegal:
                return False
            else:
                return True
        elif mode == 2:
            if action in v_legal:
                return True
        elif mode == 3:
            if action in c_legal:
                return True
        return False

    # Return the old state if a move is considered illegal
    def oldState(self):
        state = self.state
        reward = self.reward
        terminal = False
        return state, reward, terminal

    # Return a tuple (state, reward, terminal)
    def act(self, action):
        self.command_list.append(self.commands[action])
        self.runVim()
        # Temp value for state
        state = self.getState()
        # Get a reward
        reward, diffstack = self.getReward()
        #print('Reward: {}'.format(reward))
        terminal = self.fileCompare()
        if terminal:
            print('FOUND SOLUTION: {}'.format(command_list))
        self.cleanUp()
        return state, reward, terminal
