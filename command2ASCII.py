#! /usr/bin/env python3
import codecs
import numpy as np

def command2AsciiArray(command_list):
    # Initialize array to 257
    array = np.full(50, 257)
    for index in range(0, len(command_list)-1):
        if command_list[index] == '`esc':
            array[index] = 27
        elif command_list[index] == '`ent':
            array[index] = 13
        elif command_list[index] == '`bac':
            array[index] = 8
        else:
            array[index] = ord(command_list[index])
    return array
#s = codecs.open("test.txt", "r", "utf-8")
#s = s.read()
#print(text2AsciiArray(s,10,10))
