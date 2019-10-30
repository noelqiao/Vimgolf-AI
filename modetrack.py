#!/usr/bin/python3

def fun(keystrokes): 
    # requires input to be in the form of a list like ['i', ':', '<Esc>']
    v2i = ['a', 'A', 'i', 'I', 'o', 'O', 's', 'S']
    v2c = [':']
    i2v = ['<Esc>']
    c2v = ['<Enter>', '<Esc>']
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
            if keystrokes[idx] == '<BS>':
                cCount = cCount - 1
            else:
                cCount = cCount + 1
            if cCount == 0: # C2V when current column is empty
                currentMode = 'v'
        modeList.append(currentMode)
        idx = idx + 1;
    return modeList


            
        
