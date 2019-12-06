import numpy as np
import codecs
from difflib import SequenceMatcher
#from itertools import zip_longest

def t2a(string):
    arr = []
    for i in range(0,len(string)):
        arr.append(ord(string[i]))
    return arr

def diff(fp1, fp2):
    reward = 0
    with open(fp1) as f1, open(fp2) as f2:
        for line1, line2 in zip(f1, f2):
            # Example scoring
            #line1 = 'ABC'
            #line2 = '1ABC' # score 
            #line2 = 'A12' # score 

            # Find longest matching block
            s = SequenceMatcher(None, line1.rstrip(), line2.rstrip())
            longest_matching_block = s.find_longest_match(0, len(line1.rstrip()), 0, len(line2.rstrip()))
#            print(longest_matching_block)
#            print(longest_matching_block.size)
            reward += longest_matching_block.size * 0.1

            # Find exact matching characters
            correct = 0
            line1 = t2a(line1)
            line2 = t2a(line2)
            shortest_length = min
            chars = zip(line1, line2)
            for c,d in chars:
                #print(c, d)
                if c == d:
                    correct += 5
            #print(correct)
            reward += correct * 0.1
    return reward

def calReward(f1, f2, keystrokes):
    diff_sim = diff(f1, f2)
    #return diff_sim-keystrokes
    #return diff_sim+1
    return float(diff_sim) + 0.1

#s = calReward("vimgolf_challenges/ViceVersa/start.txt", "vimgolf_challenges/ViceVersa/end.txt", 0)
#print(s)
