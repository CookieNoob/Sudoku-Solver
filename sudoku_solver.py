# this program is supposed to solve a sudoku puzzle via backtracking

import numpy as np



class field:
    def __init__(self, playingfield=[]):
        self.field = playingfield
        self.dimension = len(playingfield)
        
        offsetlist = []
        for i in range(int(np.sqrt(self.dimension))):
            for j in range(int(np.sqrt(self.dimension))):
                offsetlist.append([i,j])
        self.offsets = tuple(offsetlist)

        
    def valid_move(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                for k in range(self.dimension):
                    if self.field[i][j] == self.field[i][k] and k != j and self.field[i][k] != 0:
                        return False
        
        for i in range(self.dimension):
            for j in range(self.dimension):
                for k in range(self.dimension):
                    if self.field[j][i] == self.field[k][i] and k != j and self.field[k][i] != 0:
                        return False
        
        blocksize = int(np.sqrt(self.dimension))
        blockcount = blocksize
        for blockX in range(blockcount):
            for blockY in range(blockcount):
                for offsetC in self.offsets:
                    for offset in self.offsets:
                        if self.field[blocksize*blockX+offset[0]][blocksize*blockY+offset[1]] \
                            == self.field[blocksize*blockX+offsetC[0]][blocksize*blockY+offsetC[1]] and \
                            offsetC != offset and self.field[blocksize*blockX+offsetC[0]][blocksize*blockY+offsetC[1]] != 0:
                            return False
                            
        return True
        

        
        







sudokufield = [[0,0,0,3],[3,4,2,1],[0,1,3,4],[4,3,1,2]]

testsudoku = field(sudokufield)

testsudoku.solve_grid()

