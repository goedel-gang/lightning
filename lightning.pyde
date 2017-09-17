from lichtenberg import Lichtenberg

SIZE = 5
SPEED = 1

def setup():
    global licht, p
    size(1280, 720)
    background(0)
    licht = Lichtenberg(0, height / 2, SIZE)
    p = False

def draw():
    background(0)
    colorMode(HSB, 255, 255, 255)
    for _ in range(SPEED):
        licht.update()
        licht.draw(p)

def keyPressed():
    global p
    if keyCode == ord('F'):
        print(frameRate)
    elif keyCode == ord(' '):
        p = not p