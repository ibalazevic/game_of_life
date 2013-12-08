# authors: Ivana Balazevic, Franziska Horn
import sys, copy
import numpy as np
import matplotlib.pyplot as plt
import time

class GOLerror(Exception): pass
class InvalidStateError(GOLerror): pass
class InvalidCoordError(GOLerror): pass

class Board(object):
    def __init__(self, size=[0,0],units=0):
        # size: size of the board
        # units: probability of cells being switched on
        self._board = np.array((np.random.rand(size[0], size[1])<=units),dtype=int)
        self._size = size


    def setGameRegion(self, state, x=0, y=0):
        # test that state matrix is a np.array of 0 and 1
        if (not isinstance(state, np.ndarray)) or (not state.dtype == int) or np.any(state < 0) or np.any(state > 1):
            raise InvalidStateError
        # test that given coordinates are ints smaller than the size of the board
        if (not isinstance(x, int)) or (not isinstance(y, int)) or x < 0 or y < 0 or x >= self._size[0] or y >= self._size[1]:
            raise InvalidCoordError
        xend, yend = np.shape(state)
        # test that state matrix is smaller than the board
        # and that with the given coordinates it still does not excide the board
        if x+xend-1 >= self._size[0] or y+yend-1 >= self._size[1]:
            raise InvalidStateError
        # set the board accordingly
        self._board[x:x+xend,y:y+yend] = state
        return self._board


    def getGameRegion(self, x=0, y=0, xend=10, yend=10):
        #test if xend and yend are smaller than x and y and are they ints greater than 0
        if (not isinstance(x, int)) or (not isinstance(y, int)) or (not isinstance(xend, int)) or (not isinstance(yend, int)) \
        or x < 0 or y < 0 or xend < 0 or yend < 0 or x > xend or y > yend:
            raise InvalidCoordError
        if xend > self._size[0]:
            xend = self._size[0]
        if yend > self._size[1]:
            yend = self._size[1]
        return self._board[x:xend,y:yend]


    def iterate(self):
        #extend the board with border rows (wrap around...)
        extendedBoard = np.insert(self._board, 0, self._board[-1,:], axis=0)
        extendedBoard = np.insert(extendedBoard, self._size[0]+1, self._board[0,:], axis=0)
        newcol = np.concatenate((np.array([self._board[-1,-1]]),self._board[:,-1],np.array([self._board[0,-1]])))
        extendedBoard = np.insert(extendedBoard, 0, newcol, axis=1)
        newcol = np.concatenate((np.array([self._board[-1,0]]),self._board[:,0],np.array([self._board[0,0]])))
        extendedBoard = np.insert(extendedBoard, self._size[1]+1, newcol, axis=1)
        #iterate through the extended board
        for i in range(self._size[0]):
            for j in range(self._size[1]):
                self._board[i,j] = self.applyRules(extendedBoard[i:i+3, j:j+3])                
                   
    
    def applyRules(self, currentGrid):
        #count the number of live neighbors and apply the rules accordingly
        numLiveCells = sum(sum(currentGrid==1))
        if currentGrid[1,1] == 1:
            numLiveCells -= 1
            if numLiveCells < 2 or numLiveCells > 3:
                return 0
            else:
                return 1
        else:
            if numLiveCells == 3:
                return 1
            else:
                return 0
            
            
                
def GOL(size=[10,10], units=0.5, special=None):
    myBoard = Board(size, units)
    saveState1 = copy.deepcopy(myBoard._board)
    saveState2 = copy.deepcopy(myBoard._board)
    plt.ion()   
    while True:
        myBoard.iterate()
        GOLDisplay(myBoard)
        # check if board is the same as in 1 or 2 iterations back
        if np.array_equal(saveState1, myBoard._board) or np.array_equal(saveState2, myBoard._board):
            break
        saveState2 = copy.deepcopy(saveState1)
        saveState1 = copy.deepcopy(myBoard._board)
                


def GOLDisplay(board):
    # display the board - by pygame, ASCII...
    plt.clf()
    plt.imshow(board.getGameRegion(),interpolation='nearest',cmap='Greys')
    frame1 = plt.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)
    plt.draw()
    time.sleep(0.01)
      

if __name__ == "__main__":
    GOL()


