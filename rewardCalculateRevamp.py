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

def diff(fp1, fp2, max_keystrokes, num_keystrokes):
    reward = 0
#    extra_line_count = 0
#    missing_line_count = 0
    exact_matching = 0
    partial_matching = 0
    max_line_count = 0
    min_line_count = 0
    with open(fp1) as f1, open(fp2) as f2:
        for line1, line2 in zip_longest(f1, f2):
            max_line_count += 1
            if line1 is not None and line2 is not None:
                min_line_count += 1
                # Find exact matching characters
                line1 = t2a(line1)
                line2 = t2a(line2)
                chars = zip_longest(line1, line2)
                for c,d in chars:
                    if c == None:
                        c = 0
                    if d == None:
                        d = 0
                    if c == d:
                        exact_matching += 1
                    else:
                        if chr(c) in alphas and chr(d) in alphas:
                            # Baseline
                            #correct += 2
                            partial_matching += 1

                            # Test distance from each other in alphabet.
    #                        indexa = alphas.index(chr(c))
    #                        indexb = alphas.index(chr(d))
    #                        ind_diff = abs(indexa - indexb)
    #                        ind_diff = 27 - ind_diff
    #                        partial_matching += (ind_diff / 26)
                        elif chr(c) in numbers and chr(d) in numbers:
                            partial_matching += 1
                        elif chr(c) in space and chr(d) in space:
                            partial_matching += 1
                        elif chr(c) in symbols and chr(d) in symbols:
                            partial_matching += 1

                # Penalize extra characters either way (Too long/Too short)
                extra_characters = abs(len(line2) - len(line1))
    
    # Calc reward
    reward += exact_matching * 20 
    reward += partial_matching * 2
    reward += 50 / (extra_characters + 1)
    reward += 30 / (abs(max_line_count - min_line_count) + 1)
#    if reward - (num_keystrokes) > 1:
#        reward -= num_keystrokes 
#    else:
#        reward = 1
    reward *= ((max_keystrokes - num_keystrokes) / max_keystrokes)
    #reward *= 0.1
    return reward

def calReward(f1, f2, max_keystrokes, keystrokes):
    diff_sim = diff(f1, f2, max_keystrokes, keystrokes)
    return diff_sim

#s = calReward("vimgolf_challenges/Blank/start.txt", "vimgolf_challenges/Blank/end.txt", 0)
#s = calReward("start.txt", "end.txt", 10, 3)
#print(s)
