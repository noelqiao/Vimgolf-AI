# -*- coding: utf-8 -*-
from difflib import *
from pprint import pprint
import numpy as np

def fdiff(fp1, fp2):
    with open(fp1) as f1, open(fp2) as f2:
        t1 = f1.readlines()
        t2 = f2.readlines()
        #print(t1)
        #print(t2)
        d = Differ()
        nd =list(d.compare(t1,t2))
        #pprint(nd)
        diff = len1 = len2 = dtmp = dplus = 0
        d1 = []
        d2 = []
        flag1 = False
        flag2 = False
        for lines in nd:
            if lines[0] == '-':
                if flag1 == True:
                    diff = diff + len1
                len1 = len(lines)
                flag1 = True
                flag2 = False
            if lines[0] == '+':
                if flag2 == True:
                    diff = diff + len2
                len2 = len(lines)
                flag2 = True 
                flag1 = False
            if lines[0] == '?':
                i = 1
                while i < len(lines):
                    if lines[i] == '^':
                        dtmp = 0
                        while lines[i] == '^':
                            dtmp = dtmp + 1
                            i = i + 1
                        if flag1 == True:
                            d1.append(dtmp)
                        if flag2 == True:
                            d2.append(dtmp)
                    while lines[i] == '+':
                        dplus = dplus + 1
                        i = i + 1
                    i = i + 1
                #print(d1,d2)
                if flag2 == True and flag1 == False:
                    while len(d1) < len(d2):
                        d1.append(0)
                    while len(d2) < len(d1):
                        d2.append(0)
                    #print(d1,d2)
                    diff = diff + dplus + int(np.sum(np.maximum(d1,d2)))
                    dplus = 0
                    d1 = []
                    d2 = []
                    flag2 = False
                #print(diff)
        if flag1 == True:
            diff = diff + len1
        if flag2 == True:
            diff = diff + len2
    return diff

def calReward(f1, f2, diffstack, keystrokes):
    diff1 = diffstack[len(diffstack)-1]
    diff2 = fdiff(f1,f2)
    diffstack.append(diff2)
    return diff1-diff2-keystrokes,diffstack
   
#s = []   
#s.append(fdiff(startfile,endfile))
#r, s= calReward(tmpfile,endfile,s,1)
