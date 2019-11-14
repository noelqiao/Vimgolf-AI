import codecs
import numpy as np
def t2a(string):
    arr = []
    for i in range(0,len(string)):
        arr.append(ord(string[i]))
    return arr
def ascii2AsciiArray(arr,rows,cols):
    newArr = np.full((rows,cols), -1)
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
                currCol = 0
            elif currCol == cols - 1:
                newArr[currRow,currCol] = -2
                currRow += 1
                currCol = 0
                skipping = True
        else:
            if arr[i] == 10:
                skipping = False
    return newArr    
def text2AsciiArray(string,rows,cols):
    arr = t2a(string)
    finArr = ascii2AsciiArray(arr,rows,cols)
    return finArr
#s = codecs.open("test.txt", "r", "utf-8")
#s = s.read()
#print(text2AsciiArray(s,10,10))
