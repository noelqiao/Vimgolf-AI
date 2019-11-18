#!/usr/bin/python3

# Tensorforce needs integer representation of our states
# These are our number representations of the vim modes
# normal mode = 0
# insert mode = 1
# visual mode = 2
# command mode = 3

def fun(keystrokes): 
    # There are very likely to be more potential situations.
    c2n = ['`ent', '`esc']
    i2n = ['`esc']
    n2c = [':']
    n2i = ['a', 'A', 'i', 'I', 'o', 'O', 'r', 'R', 's', 'S']
    n2v = ['v', 'V']
    v2n = ['`ent', '`esc']
    idx = 0
    currentMode = 0
    modeList = []
    cCount = 0
    while keystrokes[idx:]:
        if currentMode == 0:
            if keystrokes[idx] in n2i:
                currentMode = 1
            elif keystrokes[idx] in n2c:
                currentMode = 3
            elif keystrokes[idx] in n2v:
                currentMode = 2
        elif currentMode == 1:
            if keystrokes[idx] in i2n:
                currentMode = 0
        elif currentMode == 2:
            if keystrokes[idx] in v2n:
                currentMode = 0
        else:
            if keystrokes[idx] in c2n:
                currentMode = 0
        if currentMode == 3:
            if keystrokes[idx] == '`bac':
                cCount = cCount - 1
            else:
                cCount = cCount + 1
            if cCount == -1: # c2n when current column is empty
                currentMode = 0
        modeList.append(currentMode)
        idx = idx + 1;
    return modeList


            
        
