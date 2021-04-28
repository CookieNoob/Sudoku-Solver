import numpy as np
import copy
import pygame
pygame.font.init()



class sudoku:
    def __init__(self, sizeX, sizeY, numberspace, field):
        self.sizeX = sizeX
        self.sizeY = sizeY
        
        self.selected = None
        
        self.gridcolor = (100,100,100)
        
        self.window = pygame.display.set_mode( (sizeX,sizeY) )
        pygame.display.set_caption("Sudoku-Solver")
        
        self.field = copy.deepcopy(field)
        self.initialfield = copy.deepcopy(field)
        
        self.numberspace = numberspace
        self.draw()
        
        self.solutions = []
        
        offsetlist = []
        for i in range(int(np.sqrt(self.numberspace))):
            for j in range(int(np.sqrt(self.numberspace))):
                offsetlist.append([i,j])
        self.offsets = tuple(offsetlist)
        
    

    def select(self, position):
        if self.sizeX < position[0] or self.sizeY < position[1]:
            self.selected = None
        else:
            pos = (int(position[0]/self.sizeX * self.numberspace), \
                   int(position[1]/self.sizeY * self.numberspace)  )
            if self.initialfield[pos[0]][pos[1]] == 0:
                self.selected = pos
        return None

    def draw(self):
        self.window.fill( (255,255,255) )
        for i in range(self.numberspace+1):
            if i % np.sqrt(self.numberspace) == 0:
                linewidth = 5
            else:
                linewidth = 1
            pygame.draw.line( self.window, self.gridcolor,                       
                             (0         , i*(self.sizeY - 4)/self.numberspace + 2),    # startpoint
                             (self.sizeX, i*(self.sizeY - 4)/self.numberspace + 2),    # endpoint
                             linewidth)
            pygame.draw.line( self.window, self.gridcolor,                       
                             (i*(self.sizeX - 4)/self.numberspace + 2, 0),             # startpoint
                             (i*(self.sizeX - 4)/self.numberspace + 2, self.sizeY),    # endpoint
                             linewidth)
        
        
        for i in range(self.numberspace):
            for j in range(self.numberspace):
                if self.initialfield[i][j] != 0:
                    self.drawNumber(i,j,self.initialfield[i][j],(0,0,0))
                    continue
                if self.field[i][j] != 0:
                    self.drawNumber(i,j,self.field[i][j],(128,128,128))
                    
        pygame.display.update()

    def drawNumber(self, positionX, positionY, number, color):
        arialFont = pygame.font.SysFont("Arial", 35)
        self.window.blit(arialFont.render(str(number), 1, color),\
                         (positionX*(self.sizeX - 4)/self.numberspace + int((self.sizeX - 4)/self.numberspace/2)-8 *9/self.numberspace,\
                          positionY*(self.sizeY - 4)/self.numberspace + int((self.sizeY - 4)/self.numberspace/2)-16*9/self.numberspace) )
        self.redrawRect((positionX, positionY))
        
        
        
    def highlightSquare(self):
        if self.selected == None:
            return None
        position = self.selected
        pygame.draw.rect(self.window, (255,50,50),
                              (position[0]*(self.sizeX - 4)/self.numberspace + 3,  
                               position[1]*(self.sizeY - 4)/self.numberspace + 3, 
                               (self.sizeX-8)/self.numberspace, 
                               (self.sizeY-8)/self.numberspace ),
                              3                                                     # linewidth
                             )
        self.redrawRect(position)
                                

    def unhighlightSquare(self):
        if self.selected == None:
            return None
        position = self.selected
        
        pygame.draw.rect(self.window, (255,255,255),
                              (position[0]*(self.sizeX - 4)/self.numberspace + 3,  
                               position[1]*(self.sizeY - 4)/self.numberspace + 3, 
                               (self.sizeX-8)/self.numberspace+1, 
                               (self.sizeY-8)/self.numberspace+1 ),
                              0                                                     # linewidth
                             )
        

                             
        for i in range(position[0],position[0]+2):
            if i % np.sqrt(self.numberspace) == 0:
                linewidth = 5
            else:
                linewidth = 1
            pygame.draw.line( self.window, self.gridcolor,                       
                             (i*(self.sizeX - 4)/self.numberspace + 2, 0),             # startpoint
                             (i*(self.sizeX - 4)/self.numberspace + 2, self.sizeY),    # endpoint
                             linewidth)
                             
        for i in range(position[1],position[1]+2):
            if i % np.sqrt(self.numberspace) == 0:
                linewidth = 5
            else:
                linewidth = 1
            pygame.draw.line( self.window, self.gridcolor,                       
                             (0         , i*(self.sizeY - 4)/self.numberspace + 2),    # startpoint
                             (self.sizeX, i*(self.sizeY - 4)/self.numberspace + 2),    # endpoint
                             linewidth)                
                             
        if self.field[position[0]][position[1]] != 0:
            self.drawNumber(position[0],position[1],self.field[position[0]][position[1]], (128,128,128))
                             
                             
    def redrawRect(self, position):
        # redraws the displayed rectangular area
        pygame.display.update(  position[0]*(self.sizeX - 4)/self.numberspace - 1,
                                position[1]*(self.sizeY - 4)/self.numberspace - 1,
                                (self.sizeX-4)/self.numberspace+10,
                                (self.sizeY-4)/self.numberspace+10 )    



    def updateSquare(self, number):
        self.field[self.selected[0]][self.selected[1]] = number
        self.unhighlightSquare()
        self.drawNumber(self.selected[0],self.selected[1],number, (128,128,128))
        self.selected = None
        
        
        
        

    def valid_move(self, field):
        for i in range(self.numberspace):
            for j in range(self.numberspace):
                for k in range(self.numberspace):
                    if field[i][j] == field[i][k] and k != j and field[i][k] != 0:
                        return False
        
        for i in range(self.numberspace):
            for j in range(self.numberspace):
                for k in range(self.numberspace):
                    if field[j][i] == field[k][i] and k != j and field[k][i] != 0:
                        return False
        
        blocksize = int(np.sqrt(self.numberspace))
        blockcount = blocksize
        for blockX in range(blockcount):
            for blockY in range(blockcount):
                for offsetC in self.offsets:
                    for offset in self.offsets:
                        if     field[blocksize*blockX+offset[0]][blocksize*blockY+offset[1]]    \
                            == field[blocksize*blockX+offsetC[0]][blocksize*blockY+offsetC[1]]  \
                            and offsetC != offset                                               \
                            and field[blocksize*blockX+offsetC[0]][blocksize*blockY+offsetC[1]] != 0:
                            
                            return False
        return True
        
    def check_solved(self):
        # checks if the current configuration is valid and solved
        for i in range(self.numberspace):
            for j in range(self.numberspace):
                if self.field[i][j] == 0:
                    return False
        return self.valid_move()
        
    def solveGrid(self):
        # automatically solves the sudoku
        
        def findUnsolved(self):
            # returns a list of empty spots on the grid
            unsolved = []
            for i in range(self.numberspace):
                for j in range(self.numberspace):
                    if self.initialfield[i][j] == 0:
                        unsolved.append([i,j])
            return unsolved
        
        def solveStep(self, unsolved, grid):
            # loops over the empty spots and tries to find a valid solution there
            x,y = unsolved.pop()
            laststep = len(unsolved) == 0
            for i in range(self.numberspace):
                grid[x][y] = i+1
                
                if self.valid_move(grid):
                    if laststep:
                        self.solutions.append(copy.deepcopy(grid))
                    else:
                        solveStep(self, unsolved[:], grid)
            grid[x][y] = 0

        unsolvedlist = findUnsolved(self)
        solveStep(self, unsolvedlist, copy.deepcopy(self.initialfield))




def main():

    sizeX, sizeY = 540, 600
    numberspace = 9
    
    field = [[1,2,3,4,5,6,7,8,9], \
             [4,5,6,0,0,0,0,0,0], \
             [7,8,9,0,0,0,5,0,0], \
             [0,0,0,1,2,3,0,0,0], \
             [0,0,0,0,0,0,3,1,2], \
             [2,0,0,7,8,9,0,0,0], \
             [5,0,0,0,0,0,1,2,3], \
             [8,9,7,0,0,0,4,5,6], \
             [3,1,2,0,0,0,8,9,7] ]
    
    sudokufield = sudoku(sizeX, sizeY, numberspace, field)
    
    
    keytable = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, \
                pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, \
                pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9 }
    
    
    running = True
    while(running):
        for keystroke in pygame.event.get():
            if keystroke.type == pygame.KEYDOWN:
                if keystroke.key in keytable:
                    if sudokufield.selected != None:
                        sudokufield.updateSquare(keytable[keystroke.key])
                if keystroke.key == pygame.K_SPACE:
                    if len(sudokufield.solutions) == 0:
                        sudokufield.solveGrid()
                        
                    sudokufield.field = sudokufield.solutions.pop()
                    sudokufield.draw()
                    
            if keystroke.type == pygame.MOUSEBUTTONDOWN:
                if sudokufield.selected != None:
                    sudokufield.unhighlightSquare()
                    sudokufield.redrawRect(sudokufield.selected)
                sudokufield.select(pygame.mouse.get_pos())
                sudokufield.highlightSquare()
            
            if keystroke.type == pygame.QUIT:
                running = False
                    
                    
if __name__ == "__main__":
    main()