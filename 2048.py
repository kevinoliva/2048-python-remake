'''
Created on Feb 9, 2016

@author: Kevin Oliva
'''
###############################################################################
'''
Recreation of the game 2048
'''
#######################    Classes and Methods    #############################
import random
import string

class gameBoard():
    def __init__(self):
        self.boardList = [None] * 16 #entire board
        self.freeList = [] #list of the indexes of the free spaces on the board
        for i in range(0, 16):
            self.freeList.append(i)
        self.usedList = [] #list of the indexes of used spaces 
        
    def getRow(self, rowNum):
        if rowNum == 1:
            return [self.boardList[0], self.boardList[1], self.boardList[2], self.boardList[3]]
        elif rowNum == 2:
            return [self.boardList[4], self.boardList[5], self.boardList[6], self.boardList[7]]
        elif rowNum == 3:
            return [self.boardList[8], self.boardList[9], self.boardList[10], self.boardList[11]]
        else:
            return [self.boardList[12], self.boardList[13], self.boardList[14], self.boardList[15]]
        
    def setRow(self, rowNum, rowList):
        i = rowNum - 1
        j = 0
        while j < 4:
            if rowList[j] == None and self.boardList[i*4+j] != None: #erase 
                self.freeList.append(i*4+j)
                self.usedList.remove(i*4+j)
            elif self.boardList[i*4+j] == None and rowList[j] != None: #add
                self.usedList.append(i*4+j)
                self.freeList.remove(i*4+j)
            self.boardList[i*4+j] = rowList[j]
            j += 1
    
    def getColumn(self, colNum):
        if colNum == 1:
            return [self.boardList[0], self.boardList[4], self.boardList[8], self.boardList[12]]
        elif colNum == 2:
            return [self.boardList[1], self.boardList[5], self.boardList[9], self.boardList[13]]
        elif colNum == 3:
            return [self.boardList[2], self.boardList[6], self.boardList[10], self.boardList[14]]
        else:
            return [self.boardList[3], self.boardList[7], self.boardList[11], self.boardList[15]]
    
    def setColumn(self, colNum, colList):
        i = colNum - 1
        j = 0
        while j < 4:
            if colList[j] == None and self.boardList[j*4+i] != None: #erase 
                self.freeList.append(j*4+i)
                self.usedList.remove(j*4+i)
            elif self.boardList[j*4+i] == None and colList[j] != None: #add
                self.usedList.append(j*4+i)
                self.freeList.remove(j*4+i)
            self.boardList[j*4+i] = colList[j]
            j += 1
            
    def addRandom(self): #adds a piece randomly to the board
        index = random.randint(0, len(self.freeList)-1) #pick a free space
        piece = int(random.choice("2222222224")) #randomly assigned value
        self.boardList[self.freeList[index]] = piece #add to board
        self.usedList.append(self.freeList[index])
        self.freeList.remove(self.freeList[index])
        
#adds spaces for printing the value on the game board        

def whitespace(count, spaces):
    for i in range(0, count):
        spaces += " "
    return spaces
    
def printBoard(valueList):
    print "---------------------"
    line = "|"
    for i in range(0, 16):
        if len(str(valueList[i])) == 0:
            line = line + str(valueList[i]) + "|"
        elif valueList[i] == None:
            line = line + "    |" 
        else: 
            line = line + whitespace(4-len(str(valueList[i])), "") + str(valueList[i]) + "|"
        if (i+1)%4 == 0:
            print line
            print "---------------------"
            line = "|"

def merge(col):
    #fill in gaps
    for i in range(0, 4):
        if col[i] != None: #find an existing element
            for j in range(0, i): #move it to first available slot
                if col[j] == None:
                    col[j] = col[i]
                    col[i] = None
                    break
    #merge identical values
    for k in range(0, 3):
        if col[k] != None and col[k] == col[k+1]:
            col[k] *= 2
            col[k+1] = None
            for l in range(k+2, 4):
                col[l-1] = col[l]
            col[3] = None
    return col

def swipeUp(gb):
    for i in range(1, 5):
        temp = merge(gb.getColumn(i))
        gb.setColumn(i, temp)
    return gb

def swipeDown(gb):
    for i in range(1, 5):
        #first reverse column you receive
        temp = []
        temp2 = []
        for j in range(0, 4):
            temp.append(gb.getColumn(i)[3-j])
        temp = merge(temp)
        #undo reverse
        for k in range(0, 4):
            temp2.append(temp[3-k])
        gb.setColumn(i, temp2)
    return gb

def swipeLeft(gb):
    for i in range(1, 5):
        temp = merge(gb.getRow(i))
        gb.setRow(i, temp)
    return gb

def swipeRight(gb):
    for i in range(1, 5):
        #first reverse row you receive
        temp = []
        temp2 = []
        for j in range(0, 4):
            temp.append(gb.getRow(i)[3-j])
        temp = merge(temp)
        #undo reverse
        for k in range(0, 4):
            temp2.append(temp[3-k])
        gb.setRow(i, temp2)
    return gb

def canMerge(gb): #helps check for game termination and board updating
    fullCol = [gb.getColumn(1), gb.getColumn(2), gb.getColumn(3), gb.getColumn(4)]
    fullRow = [gb.getRow(1), gb.getRow(2), gb.getRow(3), gb.getRow(4)]
    direction = [0, 0, 0, 0]
    #returns list of directions that can merge
    #check up
    temp = []
    for i in range(1, 5):
        temp.append(merge(gb.getColumn(i)))
    if temp != fullCol: direction[0] = 1
    #check down
    temp = []
    for i in range(1, 5):
        #first reverse column you receive
        temp1 = []
        temp2= []
        for j in range(0, 4):
            temp2.append(gb.getColumn(i)[3-j])
        temp2 = merge(temp2)
        #undo reverse
        for k in range(0, 4):
            temp1.append(temp2[3-k])
        temp.append(temp1)
    if temp != fullCol: direction[1] = 2
    #check left
    temp = []
    for i in range(1, 5):
        temp.append(merge(gb.getRow(i)))
    if temp != fullRow: direction[2] = 3 
    #check right
    temp = []
    for i in range(1, 5):
        #first reverse row you receive
        temp1 = []
        temp2 = []
        for j in range(0, 4):
            temp1.append(gb.getRow(i)[3-j])
        temp1 = merge(temp1)
        #undo reverse
        for k in range(0, 4):
            temp2.append(temp1[3-k])
        temp.append(temp2)
    if temp != fullRow: direction[3] = 4 
    return direction
    
def winCheck(gb):
    for i in range(0, len(gb.boardList)):
        if gb.boardList[i] == 2048:
            printBoard(gb.boardList)
            print "\nYou Win!!!!!!!!"
            return True
    return False #still losing!


#########################    Main Program    ##################################
random.seed()

#initialize game board
board = gameBoard()
board.addRandom()
board.addRandom()


#instructions
print "2048 controls:"
print "\tw: move up\n\ta: move left\n\ts: move down\n\td: move right"
print "\tType \'quit\' to exit the game.\n"

#game loop
while not winCheck(board):
    printBoard(board.boardList)
    if len(board.freeList) == 0 and canMerge(board).count(0) == 4: 
        print "\nGame Over!!"
        break
    print 
    answer = raw_input("Direction: ") 
    while True:
        if string.lower(answer) == 'w':
            if  canMerge(board)[0] == 1:
                board = swipeUp(board)
                if len(board.freeList) != 0:
                    board.addRandom()
                break
            else: 
                print "Move did not affect board"
                answer = raw_input("Direction: ")
        elif string.lower(answer) == 's':
            if  canMerge(board)[1] == 2:
                board = swipeDown(board)
                if len(board.freeList) != 0:
                    board.addRandom()
                break
            else: 
                print "Move did not affect board"
                answer = raw_input("Direction: ")
        elif string.lower(answer) == 'a':
            if  canMerge(board)[2] == 3:
                board = swipeLeft(board) 
                if len(board.freeList) != 0:
                    board.addRandom()
                break
            else: 
                print "Move did not affect board"
                answer = raw_input("Direction: ")
        elif string.lower(answer) == 'd':
            if  canMerge(board)[3] == 4:
                board = swipeRight(board)
                if len(board.freeList) != 0: 
                    board.addRandom()
                break
            else: 
                print "Move did not affect board"
                answer = raw_input("Direction: ")
        elif string.lower(answer) == "quit":
            print "Game Over"
            raise SystemExit
        else: answer = raw_input("Invalid direction. Use 'w' 'a' 's' or 'd': ")
        