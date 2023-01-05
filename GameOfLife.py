from tkinter import *
from tkinter.ttk import Label
import random

# Initializations
matrixSize = 50
cellSize = 10
margin = 20
tempo = 400
generation = 1
cells = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
currentState = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
nextState = [[0 for x in range(matrixSize)] for y in range(matrixSize)]
ALIVE_COLOR = "red"
DEAD_COLOR = "white"


def manualInit(event):
    x = event.x - margin//2
    y = event.y - margin//2
    currentState[x//cellSize][y//cellSize] = int(not(bool(currentState[x//cellSize][y//cellSize])))
    if currentState[x//cellSize][y//cellSize] == 1:
        color = ALIVE_COLOR
    else:
        color = DEAD_COLOR
    canvas.itemconfig(cells[x//cellSize][y//cellSize], fill=color)
    global textAlive
    textAlive.set(str(" Alive cells : {}".format(sum(map(sum, currentState)))))


def init():
    for x in range(matrixSize):
        for y in range(matrixSize):
            cells[x][y] = canvas.create_rectangle(margin//2 + x*cellSize, margin//2 + y*cellSize,
                                                  margin//2 + (x+1)*cellSize,
                                                  margin//2 + (y+1)*cellSize,
                                                  outline="gray", fill="white")


def clear():
    for x in range(matrixSize):
        for y in range(matrixSize):
            currentState[x][y] = 0
            nextState[x][y] = 0
    global generation
    generation = 1
    textGeneration.set("Generation 1")
    textAlive.set(str(" Alive cells : {}".format(sum(map(sum, currentState)))))
    draw()


def randomGrid():
    for x in range(matrixSize):
        for y in range(matrixSize):
            currentState[x][y] = random.choice([0, 1])
    textAlive.set(str(" Alive cells : {}".format(sum(map(sum, currentState)))))
    draw()


def draw():
    for x in range(matrixSize):
        for y in range(matrixSize):
            if currentState[x][y] == 1:
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

    nbNeighbours = 0
    if currentState[beforeColumn][beforeRow] == 1:
        nbNeighbours += 1
    if currentState[beforeColumn][y] == 1:
        nbNeighbours += 1
    if currentState[beforeColumn][afterRow] == 1:
        nbNeighbours += 1
    if currentState[x][beforeRow] == 1:
        nbNeighbours += 1
    if currentState[x][afterRow] == 1:
        nbNeighbours += 1
    if currentState[afterColumn][beforeRow] == 1:
        nbNeighbours += 1
    if currentState[afterColumn][y] == 1:
        nbNeighbours += 1
    if currentState[afterColumn][afterRow] == 1:
        nbNeighbours += 1

    #print("({},{}) has {} neightbours.".format(x, y, nbNeighbours))
    return nbNeighbours


def evolve():
    for x in range(matrixSize):
        for y in range(matrixSize):
            nbNeighbours = getLivingNeighbours(x, y)
            if currentState[x][y] == 1:
                if nbNeighbours == 2 or nbNeighbours == 3:
                    nextState[x][y] = 1
                elif currentState[x][y] == 1 and (nbNeighbours > 3):
                    nextState[x][y] = 0
                else:
                    nextState[x][y] = 0
            if currentState[x][y] == 0 and nbNeighbours == 3:
                nextState[x][y] = 1

    for x in range(matrixSize):
        for y in range(matrixSize):
            currentState[x][y] = nextState[x][y]

    textAlive.set(str(" Alive cells : {}".format(sum(map(sum, currentState)))))
    draw()

def simulate():
    evolve()
    global windowID, generation
    generation += 1
    textGeneration.set("Generation {}".format(generation))
    windowID = window.after(tempo, simulate)


def stop():
    window.after_cancel(windowID)


window = Tk()
window.title("Jeu de la vie")

canvas = Canvas(window, width=matrixSize * cellSize + margin, height=matrixSize * cellSize + margin, highlightthickness=0)
canvas.grid(row=3, columnspan=3)
canvas.bind('<Button-1>', manualInit)

clearButton = Button(window, text="Clear", command=clear)
clearButton.grid(row=0, column=0)

randomButton = Button(window, text="Random", command=randomGrid)
randomButton.grid(row=0, column=1)

evolveButton = Button(window, text="Evolve", command=evolve)
evolveButton.grid(row=0, column=2)

simulateButton = Button(window, text="simulate", command=simulate)
simulateButton.grid(row=1, column=0)

stopButton = Button(window, text="stop", command=stop)
stopButton.grid(row=1, column=1)

textGeneration = StringVar()
textGeneration.set("Generation 1")
generationLabel = Label(window, textvariable=textGeneration)
generationLabel.grid(row=4, column=0, pady=10)

textAlive = StringVar()
textAlive.set(str(" Alive cells : 0"))
aliveLabel = Label(window, textvariable=textAlive)
aliveLabel.grid(row=4, column=1, pady=10)

init()

# Display the main window
window.mainloop()
