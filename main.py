#! /usr/bin/python3
import tempfile, subprocess
import sys, os
import queue
import numpy as np
import time
import filecmp
from multiprocessing import Process
from pyautogui import press, typewrite

# Our modules
import testWriteSpecChar as tWSC
import modetrack

print('Hello, World!')
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
    def __init__(self, start_file):
        text_list = []
        with open(start_file, 'r') as file:
            for line in file:
                text_list.append(line)
        self.text_list = text_list

    def setup(self):
        with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
            for line in self.text_list:
                tmp.write(str.encode(line))
            tmp.flush()
        return tmp

def main(attempts, start_file, end_file, scriptout):
    # Iterate over the number of attempts
    for i in range(0, attempts):
        # Create environment with the contents of the start file
        env = environment(start_file)
        q = queue.Queue()
        golfing = True

        # For reference/testing
        #master_command_list = ['i', '`esc', 'd', 'd', 'y', 'y', 'p', 'f', '-', 'i', '`bac', '`bac', '`bac', '`esc', ':', 'q', '!', '`ent', 'DONE']
        master_command_list = ['d', 'j', 'q', 'q', 'f', ',', 'r', '`ent', 'q', '2', '@', 'q', 'l', 'x', 'j', '3', '@', 'q', 'd', 'd', '3', '@', 'q', 'd', 'd']
        for command in master_command_list:
            q.put(command)

        command_list = [] 
        same_files = False
        while golfing:
            if command_list:
                tempfile = env.setup()
                #time.sleep(1)
                print('Number of commands (cost):  {}'.format(len(command_list)))

                # Create the script in here
                command_string = ''.join(command_list)
                scriptin = 'scriptin'
                tWSC.writeChars(scriptin, command_string)
#                with(open('scriptin', 'r')) as f:
#                    for line in f:
#                        print(line)
                modelist = modetrack.fun(command_list)
                print(command_list)
                print(modelist)

                # Run through the commands
#                vimgolf = Process(target = lambda: subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout]))
#                vimgolf.start()
                subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout])

                #time.sleep(0.1)

                tempfile.close()
                if filecmp.cmp(tempfile.name, end_file):
                    same_files = True

                # Check if files are the same

            #    print('more {}'.format(tempfile.name))
                print('')
                os.system('more {}'.format(tempfile.name))

                os.remove(tempfile.name)
                #print('\nTemp file removed')
                # Get a new command if queue is empty

            coords = []
            if command_list:
                with open('posout', 'r') as posfile:
                    for line in posfile:
                        line = line.strip()
                        if line:
                            coords.append(line)
            else:
                coords.append(1)
                coords.append(1)
            print('\n',coords, '\n')
            print('=======================================')

            if q.empty():
                if same_files:
                    next_command = 'DONE'
                else:
                    next_command = 'y'
            # Fetch one from the queue
            else:
                next_command = q.get()
            command_list.append(next_command)
            
            if next_command == 'DONE':
                golfing = False

        # Final Output
        print('\n\nFinal Output for iteration {}'.format(i))
        print('Number of commands (cost):  {}'.format(len(command_list) + 2))
        print('AI\'s commands:')
        print(command_list)

            # For reference
        #    press('Esc')
        #    typewrite(':w | :set cmdheight=2 | redir! > posout | echo line(".") | echo col(".") | redir END')
        #    press('enter')

      

if __name__ == '__main__':
#    print(sys.argv[1])
#    print(sys.argv[2])
#    print(sys.argv[3])
    #main(sys.argv[1], sys.argv[2], sys.argv[3])
    main(1, 'start.txt', 'end.txt', 'scriptout')
