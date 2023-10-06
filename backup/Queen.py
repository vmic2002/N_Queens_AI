import random
from enum import Enum
class Queen:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "("+str(self.row)+", "+str(self.col)+")"

class QueenError(Enum):
    SAME_ROW = 1
    SAME_COL = 2
    SAME_DIAGONAL = 3


#def get4Queens():# for testing
#    return [Queen(1,1), Queen(2,2), Queen(0,3), Queen(1,0)]


def getFirstListOfQueens(N):
    #returns list of N queens with a certain initial position
    #no two queens are in the same row or col!
    #important that no queens start at the same position (same row and same col)
    result = []
    rows = [r for r in range(N)]
    cols = [c for c in range(N)]
    for _ in range(N):
        row = rows.pop(random.randrange(len(rows)))
        col = cols.pop(random.randrange(len(cols)))
        result.append(Queen(row,col))
    return result
