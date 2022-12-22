from tkinter import *
import random

# Initializations
matrixSize = 50
cellSize = 10
cells = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
currentState = [[False for x in range(matrixSize)] for y in range(matrixSize)]
nextState = [[False for x in range(matrixSize)] for y in range(matrixSize)]
ALIVE_COLOR = "red"
DEAD_COLOR = "white"


def manualInit(event):
    currentState[event.x//cellSize][event.y//cellSize] = not(currentState[event.x//cellSize][event.y//cellSize])
    if currentState[event.x//cellSize][event.y//cellSize]:
        color = ALIVE_COLOR
    else:
        color = DEAD_COLOR
    canvas.itemconfig(cells[event.x//cellSize][event.y//cellSize], fill=color)


def init():
    for x in range(matrixSize):
        for y in range(matrixSize):
            cells[x][y] = canvas.create_rectangle(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize, outline="gray", fill="white")


def clear():
    for x in range(matrixSize):
        for y in range(matrixSize):
            currentState[x][y] = False
    draw()


def randomGrid():
    for x in range(matrixSize):
        for y in range(matrixSize):
            currentState[x][y] = random.choice([True, False])
    draw()


def draw():
    for x in range(matrixSize):
        for y in range(matrixSize):
            if currentState[x][y]:
                color = ALIVE_COLOR
            else:
                color = DEAD_COLOR
            canvas.itemconfig(cells[x][y], fill=color)


def getLivingNeighbours(x, y):
    beforeRow = y-1
    if beforeRow < 0:
        beforeRow = matrixSize - 1
    afterRow = y+1
    if afterRow == matrixSize:
        afterRow = 0
    beforeColumn = x-1
    if beforeColumn < 0:
        beforeColumn = matrixSize - 1
    afterColumn = x+1
    if afterColumn == matrixSize:
        afterColumn = 0

    nbNeighbours  = 0
    if currentState[beforeColumn][beforeRow]:
        nbNeighbours += 1
    if currentState[beforeColumn][y]:
        nbNeighbours += 1
    if currentState[beforeColumn][afterRow]:
        nbNeighbours += 1
    if currentState[x][beforeRow]:
        nbNeighbours += 1
    if currentState[x][afterRow]:
        nbNeighbours += 1
    if currentState[afterColumn][beforeRow]:
        nbNeighbours += 1
    if currentState[afterColumn][y]:
        nbNeighbours += 1
    if currentState[afterColumn][afterRow]:
        nbNeighbours += 1

    return nbNeighbours


def evolve():
    for x in range(matrixSize):
        for y in range(matrixSize):
            nbNeighbours = getLivingNeighbours(x, y)
            if currentState[x][y] and (nbNeighbours == 2 or nbNeighbours == 3):
                nextState[x][y] = True
            if currentState[x][y] and (nbNeighbours > 3):
                nextState[x][y] = False
            if not(currentState[x][y]) and nbNeighbours == 3:
                nextState[x][y] = True

    for x in range(matrixSize):
        for y in range(matrixSize):
            currentState[x][y] = nextState[x][y]

    draw()


window = Tk()
window.title("Jeu de la vie")

canvas = Canvas(window, width=matrixSize * cellSize, height=matrixSize * cellSize, highlightthickness=0)
canvas.grid(row=1, columnspan=3)
canvas.bind('<Button-1>', manualInit)

clearButton = Button(window, text="Clear", command=clear)
clearButton.grid(row=0, column=0)

randomButton = Button(window, text="Random", command=randomGrid)
randomButton.grid(row=0, column=1)

evolveButton = Button(window, text="Evolve", command=evolve)
evolveButton.grid(row=0, column=2)

init()

# Display the main window
window.mainloop()
