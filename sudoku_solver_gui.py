import numpy as np
import copy
import pygame
pygame.font.init()



class field:
    def __init__(self, sizeX, sizeY, numberspace):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.window = pygame.display.set_mode( (sizeX,sizeY) )
        self.numberspace = numberspace
        self.draw()
    

    def select(self, position):
        if self.sizeX < position[0] or self.sizeY < position[1]:
            return False
        else:
            return (int(position[0]/self.sizeX * self.numberspace), \
                    int(position[1]/self.sizeY * self.numberspace)  )

    def draw(self):
        gridcolor = (100,100,100)
        self.window.fill( (255,255,255) )
        for i in range(self.numberspace+1):
            if i % np.sqrt(self.numberspace) == 0:
                linewidth = 5
            else:
                linewidth = 1
            pygame.draw.line( self.window, gridcolor,                       
                             (0         , i*(self.sizeY - 4)/self.numberspace + 2),             # startpoint
                             (self.sizeX, i*(self.sizeY - 4)/self.numberspace + 2),    # endpoint
                             linewidth)
            pygame.draw.line( self.window, gridcolor,                       
                             (i*(self.sizeX - 4)/self.numberspace + 2, 0),             # startpoint
                             (i*(self.sizeX - 4)/self.numberspace + 2, self.sizeY),    # endpoint
                             linewidth)
        pygame.display.update()

def main():

    sizeX, sizeY = 540, 600
    numberspace = 16
    
    sudokufield = field(sizeX, sizeY, numberspace)
    
    
    keytable = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, \
                pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, \
                pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9 }
    
    
    running = True
    while(running):
        for keystroke in pygame.event.get():
            if keystroke.type == pygame.KEYDOWN:
                if keystroke.key in keytable:
                    action = keytable[keystroke.key]
                    print(action)
            if keystroke.type == pygame.MOUSEBUTTONDOWN:
                sudokufield.select(pygame.mouse.get_pos())
                key = None
                
            if keystroke.type == pygame.QUIT:
                running = False
                    
                    
if __name__ == "__main__":
    main()