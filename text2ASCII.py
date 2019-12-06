import codecs
import numpy as np
def t2a(string):
    arr = []
    for i in range(0,len(string)):
        arr.append(ord(string[i]))
    return arr

def ascii2AsciiArray(arr,rows,cols):
    # Initialize as 257
    newArr = np.full((rows,cols), 257)
    currRow = 0
    currCol = 0
    skipping = False
    for i in range(0,len(arr)):
        if not skipping:
            val = arr[i]
            newArr[currRow,currCol] = val 
            currCol += 1
            if val == 10:
                currRow += 1
                if currRow >= rows:
                    break;
                currCol = 0
            elif currCol == cols - 1:
                # If over the size of the array, assign 258 as the last index of that row
                newArr[currRow,currCol] = 258
                currRow += 1
                currCol = 0
                skipping = True
                if currRow >= rows:
                    break;
        else:
            if arr[i] == 10:
                skipping = False
    return newArr    
def text2AsciiArray(string,rows,cols):
    arr = t2a(string)
    finArr = ascii2AsciiArray(arr,rows,cols)
    return finArr
#s = codecs.open("vimgolf_challenges/ViceVersa/start.txt", "r", "utf-8")
#s = s.read()
#print(text2AsciiArray(s, 3, 80))
