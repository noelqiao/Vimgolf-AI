#! /usr/bin/python3
import tempfile, subprocess
import sys, os
from multiprocessing import Process
from pyautogui import press, typewrite

print('Hello, World!')

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
        return tmp.name

def main(start_file, end_file, scriptout):
    # Create environment with the contents of the start file
    env = environment(start_file)
    tempfile = env.createStartFile()

    subprocess.call([EDITOR, tempfile, '-W', scriptout], stdin=)
    press('d')
    press('d')
    press(':')
    press('q')
    press('!')
    print('Are we here')
    # Try and run vim with subprocesses
#    with tempfile.NamedTemporaryFile(suffix='tmp', delete=False) as tmp:
#        with open(start_file, 'r') as start:
#            line = str.encode(start.readline())
#            tmp.write(line)
#        tmp.flush()
#        subprocess.call([EDITOR, tmp.name])
      

if __name__ == '__main__':
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    main(sys.argv[1], sys.argv[2], sys.argv[3])
