import pygame
import numpy as np
import time
import get_grid
import argparse


# Arguement Parser
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model_directory", required=True,
	help="path to trained digit classifier")
ap.add_argument("-n", "--number", required=True,
	help="number of trained digit classifier")
ap.add_argument("-i", "--image", required=True,
	help="path to input Sudoku puzzle image")
args = vars(ap.parse_args())


# Getting the grid through ocr'ing the image 
grid = get_grid.get_grid(args['image'], args['model_directory'], int(args['number']))


# Variables
SIZE = 81 
OFFSET = 100
HEIGHT = 9*SIZE + OFFSET
WIDTH = 9*SIZE
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
WIDTH_BUTTON = 100
HEIGHT_BUTTON = 50


# Puzzle is the array which is modified while solving by a player
puzzle = grid.copy()


# Solution is the array in which the solution is computed
solution = grid.copy()


#Button Class for making buttons
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, WHITE)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
    
    def is_pressed(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


# To check whether the given configuration of solution is right or not 
#               - used for solver/visualizer functions
def check(x,y,n,sol):
    for i in range(9):
        if sol[x][i] == n:
            return False
    for i in range(9):
        if sol[i][y] == n:
            return False
    a = x//3
    b = y//3
    startx = a*3
    starty = b*3
    for i in range(startx, startx+3):
        for j in range(starty, starty+3):
            if sol[i][j] == n:
                return False
    return True


# To find the solution beforehand and using it to validate player's solution
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


# To check the user's solution with the correct solution
def check_solve():
    pygame.draw.rect(win, WHITE, (3*SIZE, 9*SIZE+5, 3*SIZE, OFFSET))
    pygame.display.update()
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0 and puzzle[i][j] != solution[i][j]:
                    text = font.render('Wrong', 1, BLACK)
                    textRect = text.get_rect()
                    textRect.center = (WIDTH//2, WIDTH+50)
                    win.blit(text, textRect)
                    pygame.display.update()
                    return
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                text = font.render('Incomplete', 1, BLACK)
                textRect = text.get_rect()
                textRect.center = (WIDTH//2, WIDTH+50)
                win.blit(text, textRect)
                pygame.display.update()
                return
    pygame.draw.rect(win, WHITE, (0, 980, 900, 75))
    pygame.display.update()
    text = font.render('Correct', 1, BLACK)
    textRect = text.get_rect()
    textRect.center = (WIDTH//2, WIDTH+50)
    win.blit(text, textRect)
    pygame.display.update()
    return


# Solver Function
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
                        text = font.render(str(grid[i][j]), 1, BLACK)
                        textRect = text.get_rect()
                        textRect.center = (SIZE*j+SIZE//2,SIZE*i+SIZE//2)
                        win.fill(WHITE, textRect)
                        win.blit(text, textRect)
                        pygame.draw.rect(win, pygame.Color('green'), (SIZE*j+5, SIZE*i+5, SIZE-10, SIZE-10), 5)
                        pygame.display.update()
                        pygame.time.delay(2)
                        solver()
                        if not flag:
                            grid[i][j] = 0
                            win.fill(WHITE, textRect)
                            text = font.render(str(grid[i][j]), 1, BLACK)
                            win.blit(text, textRect)
                            pygame.draw.rect(win, pygame.Color('red'), (SIZE*j+5, SIZE*i+5, SIZE-10, SIZE-10), 5)
                            pygame.display.update()
                return
            
    flag = True
    print(grid)
    return


# Setting up the game Window
pygame.init()
pygame.display.list_modes()
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sudoku")
win.fill(WHITE)
pygame.display.update()
solver_for_check()


# Setting up the grid
for i in range(1,3):
    pygame.draw.line(win, BLACK,(SIZE*3*i,0),(SIZE*3*i,WIDTH),3)
    pygame.draw.line(win, BLACK,(0,SIZE*3*i),(WIDTH,SIZE*3*i),3)
for i in range(1,9):
	pygame.draw.line(win, BLACK,(i*SIZE,0),(i*SIZE,WIDTH),1)
	pygame.draw.line(win, BLACK,(0,i*SIZE),(WIDTH,i*SIZE),1)
pygame.draw.line(win, BLACK, (0,9*SIZE), (9*SIZE,9*SIZE),3)
sudoku_blocks = []
for i in range(9):
    for j in range(9):
        s = Button(BLACK, SIZE*j, SIZE*i, SIZE, SIZE, '')
        sudoku_blocks.append(s)


# Drawing the SOLVE  and CHECK button
solveButton = Button(BLACK, SIZE*7, WIDTH+20, WIDTH_BUTTON, HEIGHT_BUTTON, 'SOLVE')
solveButton.draw(win)
checkButton = Button(BLACK, SIZE*1, WIDTH+20, WIDTH_BUTTON, HEIGHT_BUTTON, 'CHECK')
checkButton.draw(win)


# Laying out the initial puzzle
for i in range(9):
    for j in range(9):
        if grid[j][i] != 0:
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(str(grid[j][i]), 1, (0,0,255))
            textRect = text.get_rect()
            textRect.center = (SIZE*i + SIZE//2,SIZE*j + SIZE//2)
            win.blit(text, textRect)
pygame.display.update()


# Pygame main loop
clicked = ()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for s in sudoku_blocks:
                if s.is_pressed(event.pos):
                    if len(clicked)>0:
                        last_left, last_top = clicked
                        pygame.draw.rect(win, WHITE, (SIZE*last_left+5, SIZE*last_top+5, SIZE-10, SIZE-10),3)
                        pygame.display.update()
                        clicked = ()
                    x, y = event.pos
                    left, top = x//SIZE, y//SIZE
                    pygame.draw.rect(win, (0,0,255), (SIZE*left+5, SIZE*top+5, SIZE-10, SIZE-10),3)
                    pygame.display.update()
                    clicked = (left, top)
            if solveButton.is_pressed(event.pos):
                pygame.draw.rect(win, WHITE, (WIDTH//3, WIDTH+5, 4*SIZE-10, OFFSET))
                pygame.display.update()
                solver()
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)  
            elif checkButton.is_pressed(event.pos):
                check_solve()
        if event.type == pygame.KEYDOWN:
            number = ''
            if clicked:
                left, top = clicked
            if event.unicode.isnumeric():
                number = event.unicode
            if number >='0' and number <= '9':
                font = pygame.font.SysFont('comicsans', 60)
                text = font.render(number, 1, BLACK)
                textRect = text.get_rect()
                textRect.center = (SIZE*left + SIZE//2,SIZE*top + SIZE//2)
                if grid[top][left] == 0:
                    if number == '0':
                        puzzle[top][left] = int(number)
                        win.fill(WHITE, textRect)
                        pygame.display.update()
                    else:
                        puzzle[top][left] = int(number) 
                        win.fill(WHITE, textRect)
                        win.blit(text, textRect)
                        pygame.display.update()    
pygame.quit()

