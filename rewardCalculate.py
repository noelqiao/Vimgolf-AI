# -*- coding: utf-8 -*-
from difflib import *

def fdiff(fp1, fp2):
    with open(fp1) as f1, open(fp2) as f2:
        t1 = f1.readlines()
        t2 = f2.readlines()
        #print(t1)
        #print(t2)
        nd =list(ndiff(t1,t2))
        diff = 0
        for lines in nd:
            if (lines[0]=='?'):
                for i in lines:
                    if (line[i]=='+' | lines[i]=='^'):
                        diff = diff + 1           
    return diff

def calReward(f1, f2, diffstack, keystrokes):
    diff1 = diffstack.pop()
    diff2 = fdiff(f1,f2)
    diffstack.append(diff2)
    return diff1-diff2-keystrokes,diffstack
   
#s = []
#s[0] = fdiff(f1,f2)
    
f1 = ''
f2 = ''
r, s= calReward(f1,f2,s,1)