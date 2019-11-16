def state2array(cursor_pos, mode_list):
    a = []
    x = cursor_pos[0]
    a.append(x)
    y = cursor_pos[1]
    a.append(y)
    z = mode_list[-1]
    a.append(z)
    #with open(modeFile) as f1:
#        x = cursor_pos[0].zfill(nPos)
#        y = cursor_pos[1].zfill(nPos)
#        z = mode_list[-1]
        #m = f2.readline().strip()
        #a.append(x+y+m)

    print(a)
    return a


#test
#state2array('posout.txt', 'modeout.txt', 3);
            
