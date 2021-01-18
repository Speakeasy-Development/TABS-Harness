# Input controllers
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://pynput.readthedocs.io/en/latest/mouse.html


x = 0
y = 0

mouse = Controller()

while True:

    currentX = mouse.position[0]
    currentY = mouse.position[1]

    if x != currentX or y != currentY:
        print('{}'.format(mouse.position))

        x = currentX
        y = currentY
