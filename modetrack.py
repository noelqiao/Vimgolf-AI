#!/usr/bin/python3

# Tensorforce needs integer representation of our states
# These are our number representations of the vim modes
# normal mode = 0
# insert mode = 1
# visual mode = 2
# command mode = 3
def fun(keystrokes): 
    # requires input to be in the form of a list like ['i', ':', '<Esc>']
    v2i = ['a', 'A', 'i', 'I', 'o', 'O', 's', 'S']
    v2c = [':']
    i2v = ['`esc']
    c2v = ['`ent', '`esc']
    idx = 0
    currentMode = 'v'
    modeList = []
    cCount = 0
    while keystrokes[idx:]:
        if currentMode == 'v':
            if keystrokes[idx] in v2i:
                currentMode = 'i'
            elif keystrokes[idx] in v2c:
                currentMode = 'c'
        elif currentMode == 'i':
            if keystrokes[idx] in i2v:
                currentMode = 'v'
        else:
            if keystrokes[idx] in c2v:
                currentMode = 'v';
        if currentMode == 'c':
            if keystrokes[idx] == '`bac':
                cCount = cCount - 1
            else:
                cCount = cCount + 1
            if cCount == 0: # C2V when current column is empty
                currentMode = 'v'
        modeList.append(currentMode)
        idx = idx + 1;
    return modeList


            
        
