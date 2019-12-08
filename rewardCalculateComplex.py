import numpy as np
import codecs
from difflib import SequenceMatcher
from itertools import zip_longest

alphas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
space = [' ']
symbols = ['$', '^', '%', ',', '.', '@']

def t2a(string):
    arr = []
    for i in range(0,len(string)):
        arr.append(ord(string[i]))
    return arr

def diff(fp1, fp2):
    reward = 0
    extra_line_count = 0
    with open(fp1) as f1, open(fp2) as f2:
        for line1, line2 in zip_longest(f1, f2):
            #print(line1, line2)
            if line1 == None:
                line1 = ""
                extra_line_count += 1
            if line2 == None:
                line2 = ""

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
            #shortest_length = min
            chars = zip_longest(line1, line2)
            for c,d in chars:
                #print(c, d)
                if c == None:
                    c = 0
                if d == None:
                    d = 0
                if c == d:
                    correct += 5
                else:
                    if chr(c) in alphas and chr(d) in alphas:
                        # Baseline
                        correct += 2

                        # Test distance from each other in alphabet.
                        # Range [1, 3]
#                        indexa = alphas.index(chr(c))
#                        indexb = alphas.index(chr(d))
#                        ind_diff = abs(indexa - indexb)
#                        ind_diff = 27 - ind_diff
#                        correct += (((2 * ind_diff) / 26) + 1)
                    elif chr(c) in numbers and chr(d) in numbers:
                        correct += 2
                    elif chr(c) in space and chr(d) in space:
                        correct += 2
                    elif chr(c) in symbols and chr(d) in symbols:
                        correct += 2
            #print(correct)
            reward += correct * 0.1

            # Penalize extra characters
            penalty = abs(len(line2) - len(line1)) * 0.20
            if reward - penalty > 0.1:
                reward -= penalty
            else:
                reward = 0.1
        # Penalize extra lines
        penalty = extra_line_count * 0.35
        if reward - penalty > 0.1:
            reward -= penalty
        else:
            reward = 0.1
    return reward

def calReward(f1, f2, keystrokes):
    diff_sim = diff(f1, f2)
    return float(diff_sim) + 0.1

#s = calReward("vimgolf_challenges/Blank/start.txt", "vimgolf_challenges/Blank/end.txt", 0)
#s = calReward("start.txt", "end.txt", 0)
#print(s)
