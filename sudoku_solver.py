# this program is supposed to solve a sudoku puzzle via backtracking

import numpy as np
import copy



class field:
    def __init__(self, playingfield=[]):
        self.field = copy.deepcopy(playingfield)
        self.dimension = len(playingfield)
        self.solutions = []
        
        # list of positions of the upper left corner of the blocks - required for the validity check
        offsetlist = []
        for i in range(int(np.sqrt(self.dimension))):
            for j in range(int(np.sqrt(self.dimension))):
                offsetlist.append([i,j])
        self.offsets = tuple(offsetlist)

        
    def valid_move(self, field):
        # ckecks if the current configuration is valid
        
        #rows and collums
        for i in range(self.dimension):
            for j in range(self.dimension):
                for k in range(self.dimension):
                    if field[i][j] == field[i][k] and k != j and field[i][k] != 0:
                        return False
        
        for i in range(self.dimension):
            for j in range(self.dimension):
                for k in range(self.dimension):
                    if field[j][i] == field[k][i] and k != j and field[k][i] != 0:
                        return False
        
        # blocks
        blocksize = int(np.sqrt(self.dimension))
        blockcount = blocksize
        for blockX in range(blockcount):
            for blockY in range(blockcount):
                for offsetC in self.offsets:
                    for offset in self.offsets:
                        if field[blocksize*blockX+offset[0]][blocksize*blockY+offset[1]] \
                            == field[blocksize*blockX+offsetC[0]][blocksize*blockY+offsetC[1]] and \
                            offsetC != offset and field[blocksize*blockX+offsetC[0]][blocksize*blockY+offsetC[1]] != 0:
                            return False
                            
        return True
        
    def check_solved(self):
        # checks if the current configuration is valid and solved
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.field[i][j] == 0:
                    return False
        return self.valid_move()
        
    def solve_grid(self):
        # automatically solves the sudoku
        
        def find_unsolved(self):
            # returns a list of empty spots on the grid
            unsolved = []
            for i in range(self.dimension):
                for j in range(self.dimension):
                    if self.field[i][j] == 0:
                        unsolved.append([i,j])
            return unsolved
        
        def solve_step(self, unsolved, grid):
            # loops over the empty spots and tries to find a valid solution there
            x,y = unsolved.pop()
            laststep = len(unsolved) == 0
            for i in range(self.dimension):
                grid[x][y] = i+1
                
                if self.valid_move(grid):
                    if laststep:
                        self.solutions.append(copy.deepcopy(grid))
                    else:
                        solve_step(self, unsolved[:], copy.deepcopy(grid))
                        solve_step(self, unsolved[:], grid)
            grid[x][y] = 0
                    
        unsolvedlist = find_unsolved(self)
        solve_step(self, unsolvedlist, self.field)




def main():
    sudokufield = [[0,0,0,3],[3,4,2,1],[0,1,3,4],[4,3,1,2]]
    testsudoku = field(sudokufield)
    testsudoku.solve_grid()
    print("saved solutions", testsudoku.solutions)
    
    sudokufield2 = [[0,1,0,0],[0,0,0,0],[0,0,0,0],[1,2,3,4]]
    testsudoku2 = field(sudokufield2)
    testsudoku2.solve_grid()
    print("gefundene Lösungen: ", len(testsudoku2.solutions))
    print("saved solutions")
    for solution in testsudoku2.solutions:
        print(solution)


    sudokufield3 = [[1,2,3,4,5,6,7,8,9], \
                    [4,5,6,0,0,0,0,0,0], \
                    [7,8,9,0,0,0,5,0,0], \
                    [0,0,0,1,2,3,0,0,0], \
                    [0,0,0,0,0,0,3,1,2], \
                    [2,0,0,7,8,9,0,0,0], \
                    [5,0,0,0,0,0,1,2,3], \
                    [8,9,7,0,0,0,4,5,6], \
                    [3,1,2,0,0,0,8,9,7] ]
    testsudoku3 = field(sudokufield3)
    testsudoku3.solve_grid()
    print("gefundene Lösungen: ", len(testsudoku3.solutions))
    print("saved solutions")
    for solution in testsudoku3.solutions:
        for reihe in solution:
            print(reihe)
        print()






if __name__ == "__main__":
    main()