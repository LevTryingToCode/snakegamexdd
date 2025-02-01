import os
import random
import msvcrt
import time
import threading
from playsound3 import playsound

# Constants
width = 20
height = 20

# Variables
gameOver = False
x, y = width // 2, height // 2
fruitX, fruitY = random.randint(0, width - 1), random.randint(0, height - 1)
score = 0
tailX, tailY = [0] * 100, [0] * 100
nTail = 0

# Directions
STOP = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
dir = STOP

def Setup():
    global gameOver, dir, x, y, fruitX, fruitY, score
    gameOver = False
    dir = STOP
    x, y = width // 2, height // 2
    fruitX, fruitY = random.randint(0, width - 1), random.randint(0, height - 1)
    score = 0

def Draw():
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(width + 2):
        print("#", end="")
    print()

    for i in range(height):
        for j in range(width):
            if j == 0:
                print("#", end="")
            if i == y and j == x:
                print("O", end="")
            elif i == fruitY and j == fruitX:
                print("F", end="")
            else:
                print_char = " "
                for k in range(nTail):
                    if tailX[k] == j and tailY[k] == i:
                        print_char = "o"
                print(print_char, end="")
            if j == width - 1:
                print("#", end="")
        print()

    for i in range(width + 2):
        print("#", end="")
    print()
    print(f"Score: {score}")

def Input():
    global dir, gameOver
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('utf-8')
        if key == 'a':
            dir = LEFT
        elif key == 'd':
            dir = RIGHT
        elif key == 'w':
            dir = UP
        elif key == 's':
            dir = DOWN
        elif key == 'x':
            gameOver = True

def Logic():
    global x, y, fruitX, fruitY, score, nTail, gameOver
    prevX, prevY = tailX[0], tailY[0]
    tailX[0], tailY[0] = x, y
    for i in range(1, nTail):
        prev2X, prev2Y = tailX[i], tailY[i]
        tailX[i], tailY[i] = prevX, prevY
        prevX, prevY = prev2X, prev2Y

    if dir == LEFT:
        x -= 1
    elif dir == RIGHT:
        x += 1
    elif dir == UP:
        y -= 1
    elif dir == DOWN:
        y += 1

    if x >= width:
        x = 0
    elif x < 0:
        x = width - 1
    if y >= height:
        y = 0
    elif y < 0:
        y = height - 1

    for i in range(nTail):
        if tailX[i] == x and tailY[i] == y:
            gameOver = True
            threading.Thread(target=playsound, args=("gameover yeeeeeeeeeeee.mp3",)).start()

    if x == fruitX and y == fruitY:
        score += 10
        fruitX, fruitY = random.randint(0, width - 1), random.randint(0, height - 1)
        nTail += 1
        threading.Thread(target=playsound, args=("fart.mp3",)).start()

def main():
    Setup()
    while not gameOver:
        Draw()
        Input()
        Logic()
        time.sleep(0.2)

if __name__ == "__main__":
    main()