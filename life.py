from tkinter import *
from tkinter import font


grid = []
numGens = 0
m = 25
filename = "inLife.txt"
currentGeneration = 0


def readInput(fileName):
    
    #this section reads the file 
    global numGens
    global grid
    
    file = open(fileName, 'r')
    line = file.readline()
    numGens = int(line)
    row = 0
    
    line = file.readline()
    while line:
            grid.append([])
            for i in line:
                    if i != '\n':
                            grid[row].append(int(i))
            row += 1
            line = file.readline()
    file.close

def build_graph():
    global graph
    global m
    global gameWindow
    global currentGen
    global grid

    WIDTH = m*len(grid[0])
    HEIGHT = m*len(grid)
    
    gameWindow = Tk()
    gameWindow.geometry('%dx%d+%d+%d' % (WIDTH+200,HEIGHT+80,(gameWindow.winfo_screenwidth() - WIDTH)/2,(gameWindow.winfo_screenheight() - HEIGHT)/2))
    gameWindow.bind_all('<Escape>',lambda event: event.widget.destroy())

    fontHeader = font.Font(family = "Times New Roman", size = "24", underline = 1, weight = "bold")
    fontBody = font.Font(family = "Times New Roman", size = "16")

    TitleFrame = Frame(gameWindow, height = 40)
    TitleFrame.pack()
    GenerationFrame = Frame(gameWindow, height = 40)
    GenerationFrame.pack()
    GridFrame = Frame(gameWindow, height = HEIGHT)
    GridFrame.pack(side=BOTTOM)

    windowLabel = Label(TitleFrame, text = "Conway's Game of Life", font = fontHeader, bg = "green")
    windowLabel.pack()

    genLabel = Label( GenerationFrame, text = "Current Generation:   ", font = fontBody )
    genLabel.pack(side = LEFT)

    currentGen = Label( GenerationFrame, text = "0", font = fontBody)
    currentGen.pack(side = LEFT)
    
    gameWindow.overrideredirect(True)

    graph = Canvas(GridFrame, width = WIDTH, height = HEIGHT, background = 'white')
    graph.pack(side=BOTTOM)
    graph.after(40,update)

def update():
        global currentGen
        global currentGeneration
        global numGens

        if currentGeneration <= numGens:
            currentGen.config(text=currentGeneration)
            currentGeneration = currentGeneration+1
            draw()
            graph.after(500,update)

def draw():
        global m
        global graph
        global grid
        
        graph.delete(ALL)

        row = 0
        while row < len(grid):
                col = 0
                while col < len(grid[0]):
                      cell = grid[row][col]
                      startX = m*col
                      startY = m*row
                      endX = startX + m
                      endY = startY + m
                      if cell == 1:
                              graph.create_rectangle(startX,startY,endX,endY,fill="green",outline = "white")
                      else:
                             graph.create_rectangle(startX,startY,endX,endY,fill="white",outline = "white")
                      col = col + 1
                row = row + 1
        
        next_gen()
        graph.update()


def next_gen():
    global grid

    hight,width = len(grid),len(grid[0])
    
    after = []
    
    for y in range(hight):
            after.append([])
            for x in range(width):
                    count = 0
                    for ys in [y-1,y,y+1]:
                            for xs in [x-1,x,x+1]:
                                    if ys >= 0 and xs >= 0 and ys < hight and xs < width and (xs != x or ys != y):
                                            if grid[ys][xs] == 1:
                                                    count += 1
                    if grid[y][x] == 1:
                            if count < 2:
                                    after[y].append(0)
                            elif count > 3:
                                    after[y].append(0)
                            else:
                                    after[y].append(1)
                    elif grid[y][x] == 0:
                            if count == 3:
                                    after[y].append(1)
                            else:
                                    after[y].append(0)
    grid = after
    


def main():
        global filename

        readInput(filename)
        build_graph()

main()
