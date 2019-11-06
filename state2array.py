
def state2array(cursorFile, modeFile, nPos):
    a = []
    with open(cursorFile) as f1, open(modeFile) as f2:
        for line in f1:
            pos = line.split()
            x = pos[0].zfill(nPos)
            y = pos[1].zfill(nPos)
            m = f2.readline().strip()
            a.append(x+y+m)
    print(a)
    return a


#test
#state2array('posout.txt', 'modeout.txt', 3);
            