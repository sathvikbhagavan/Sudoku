import pygame
import numpy as np
import time

#Puzzle
grid = np.array([[5,3,0,0,7,0,0,0,0],
                  [6,0,0,1,9,5,0,0,0],
                  [0,9,8,0,0,0,0,6,0],
                  [8,0,0,0,6,0,0,0,3],
                  [4,0,0,8,0,3,0,0,1],
                  [7,0,0,0,2,0,0,0,6],
                  [0,6,0,0,0,0,2,8,0],
                  [0,0,0,4,1,9,0,0,5],
                  [0,0,0,0,8,0,0,7,9]])

grid_copy = grid.copy()
solution = grid.copy()

#Button Class for making buttons
class Button:
    #Constructor 
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    #Drawing the button on the window
    def draw(self, win):
        
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
    
    #To check if the button is pressed or not 
    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False

#To check whether the given configuration of solution is right or not - used for solver/visualizer functions
def check(x,y,n,sol):
    for i in range(9):
        if sol[x][i] == n:
            return False
    for i in range(9):
        if sol[i][y] == n:
            return False
    a = int(x/3)
    b = int(y/3)
    startx = a*3
    starty = b*3
    for i in range(startx, startx+3):
        for j in range(starty, starty+3):
            if sol[i][j] == n:
                return False
    return True


#To find the solution beforehand and using it to validate user's solution
flag_sol = False
def solver_for_check():
    global solution
    global flag_sol
    for i in range(9):
        for j in range(9):
            if solution[i][j] == 0:
                for k in range(1,10):
                    if check(i,j,k,solution):
                        solution[i][j] = k
                        solver_for_check()
                        if not flag_sol:
                            solution[i][j] = 0
                return
    flag_sol = True

#To check the user's solution with the correct solution
def check_solve():
    
    pygame.draw.rect(win, (255,255,255), (205, 905, 390, 75))
    pygame.display.update()
    for i in range(9):
        for j in range(9):
            if grid_copy[i][j] != 0 and grid_copy[i][j] != solution[i][j]:
                    text = font.render('Wrong', 1, (0,0,0))
                    textRect = text.get_rect()
                    textRect.center = (450, 950)
                    win.blit(text, textRect)
                    pygame.display.update()
                    return
    for i in range(9):
        for j in range(9):
            if grid_copy[i][j] == 0:
                text = font.render('Incomplete', 1, (0,0,0))
                textRect = text.get_rect()
                textRect.center = (450, 950)
                win.blit(text, textRect)
                pygame.display.update()
                return
    pygame.draw.rect(win, (255,255,255), (0, 980, 900, 75))
    pygame.display.update()
    text = font.render('Correct', 1, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (400, 950)
    win.blit(text, textRect)
    pygame.display.update()
    return
                
#Solver Function
flag = False
def solver():
    global flag
    global grid
    font = pygame.font.SysFont('comicsans', 60)
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for k in range(1,10):
                    if check(i,j,k,grid):
                        grid[i][j] = k
                        text = font.render(str(grid[i][j]), 1, (0,0,0))
                        textRect = text.get_rect()
                        textRect.center = (100*j+50,100*i+50)
                        win.fill((255,255,255), textRect)
                        win.blit(text, textRect)
                        pygame.draw.rect(win, (0,255,0), (100*j+5, 100*i+5, 90, 90), 5)
                        pygame.display.update()
                        pygame.time.delay(2)
                        solver()
                        if not flag:
                            grid[i][j] = 0
                            win.fill((255,255,255), textRect)
                            text = font.render(str(grid[i][j]), 1, (0,0,0))
                            win.blit(text, textRect)
                            pygame.draw.rect(win, (255,0,0), (100*j+5, 100*i+5, 90, 90), 5)
                            pygame.display.update()
                return
            
    flag = True
    print(grid)
    return

#Setting up the game Window
pygame.init()
pygame.display.list_modes()
win = pygame.display.set_mode((900,1050))
pygame.display.set_caption("Sudoku")
win.fill((255,255,255))
pygame.display.update()
solver_for_check()

#Setting up the grid
for i in range(1,3):
    pygame.draw.line(win, (0,0,0),(300*i,0),(300*i,900),3)
    pygame.draw.line(win, (0,0,0),(0,300*i),(900,300*i),3)
for i in range(1,9):
	pygame.draw.line(win, (0,0,0),(i*100,0),(i*100,900),1)
	pygame.draw.line(win, (0,0,0),(0,i*100),(900,i*100),1)
pygame.draw.line(win, (0,0,0), (0,900), (900,900),3)
sudoku_blocks = []
for i in range(9):
    for j in range(9):
        s = Button((0,0,0), 100*j, 100*i, 100, 100, '')
        sudoku_blocks.append(s)

#Drawing the SOLVE  and CHECK button
solveButton = Button((0,0,0), 700, 915, 100, 50, 'SOLVE')
solveButton.draw(win)
checkButton = Button((0,0,0), 100, 915, 100, 50, 'CHECK')
checkButton.draw(win)

#Laying out the initial puzzle
for i in range(9):
    for j in range(9):
        if grid[j][i] != 0:
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(str(grid[j][i]), 1, (0,100,255))
            textRect = text.get_rect()
            textRect.center = (100*i + 50,100*j + 50)
            win.blit(text, textRect)
pygame.display.update()


#Pygame main loop
clicked = ()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for s in sudoku_blocks:
                if s.is_over(event.pos):
                    if len(clicked)>0:
                        last_left, last_top = clicked
                        pygame.draw.rect(win, (255,255,255), (100*last_left+5, 100*last_top+5, 90, 90),3)
                        pygame.display.update()
                        clicked = ()
                    x, y = event.pos
                    left, top = int(x/100), int(y/100)
                    pygame.draw.rect(win, (0,0,255), (100*left+5, 100*top+5, 90, 90),3)
                    pygame.display.update()
                    clicked = (left, top)
            if solveButton.is_over(event.pos):
                pygame.draw.rect(win, (255,255,255), (205, 905, 390, 75))
                pygame.display.update()
                solver()
		pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            elif checkButton.is_over(event.pos):
                check_solve()
        if event.type == pygame.KEYDOWN:
            number = ''
            left, top = clicked
            if event.unicode.isnumeric():
                number = event.unicode
            if number >='0' and number <= '9':
                font = pygame.font.SysFont('comicsans', 60)
                text = font.render(number, 1, (0,0,0))
                textRect = text.get_rect()
                textRect.center = (100*left + 50,100*top + 50)
                if grid[top][left] == 0:
                    if number == '0':
                        grid_copy[top][left] = int(number)
                        win.fill((255,255,255), textRect)
                        pygame.display.update()
                    else:
                        grid_copy[top][left] = int(number) 
                        win.fill((255,255,255), textRect)
                        win.blit(text, textRect)
                        pygame.display.update()    
pygame.quit()

