#! /usr/bin/python3
import tempfile, subprocess
import sys, os
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
        self.text_list =  text_list

    def createStartFile(self):
        with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
            for line in self.text_list:
                tmp.write(str.encode(line))
            tmp.flush()
        return tmp

def main(start_file, end_file, scriptout):
    # Create environment with the contents of the start file
    env = environment(start_file)
    tempfile = env.createStartFile()
    
    master_command_list = ['i', '`esc', 'd', 'd', 'y', 'y', 'p', 'f', '-', 'i', '`bac', '`bac', '`bac', '`esc', ':', 'q', '!', '`ent']
    print('Number of commands (cost):  {}'.format(len(master_command_list)))
    # Create the script in here
    master_command_string = ''.join(master_command_list)
    scriptin = 'scriptin.test'
    tWSC.writeChars(scriptin, master_command_string)
    modelist = modetrack.fun(master_command_list)
    print(modelist)

    coords = []
    with open('posout', 'r') as posfile:
        for line in posfile:
            line = line.strip()
            if line:
                coords.append(line)
    print(coords)

    vimgolf = Process(target = lambda: subprocess.call([EDITOR, tempfile.name, '-s', scriptin, '-W', scriptout]))
    vimgolf.start()

    # For reference
#    press('Esc')
#    typewrite(':w | :set cmdheight=2 | redir! > posout | echo line(".") | echo col(".") | redir END')
#    press('enter')

    tempfile.close()

    # Try and run vim with subprocesses
#    with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
#        with open(start_file, 'r') as start:
#            line = str.encode(start.readline())
#            tmp.write(line)
#        tmp.flush()
#        subprocess.call([EDITOR, tmp.name])
    print('Are we here')
    print('more {}'.format(tempfile.name))
      

if __name__ == '__main__':
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    main(sys.argv[1], sys.argv[2], sys.argv[3])
