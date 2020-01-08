from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from components import Entry,Checker, Display,NotGate,AndGate,NandGate,OrGate,NorGate,XorGate,XnorGate,KeyBoard
from elements import Window
from util import Coords,alfa_num_around

window:Window = Window()

def init():
    glClearColor(.9, 0.8, .6, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-100.0,100.0,100.0,-100.0)

    window.elements.append(Display())
    window.elements[0].getCheck(0).setValue(False)
    window.elements[0].getCheck(1).setValue(False)
    window.elements[0].getCheck(2).setValue(False)
    window.elements[0].getCheck(3).setValue(False)
    window.elements[0].setRotation()

    window.elements[0].setCoords(Coords(-50,-50))
    
    window.elements[0].setRotation()
    window.elements[0].setRotation()

    window.elements.append(NotGate())

    window.elements.append(Entry())
    #window.elements[2].setValue(True)
    window.elements[2].setCoords(Coords(-20,-20))

    window.elements.append(Entry())
    window.elements[3].setValue(False)
    window.elements[3].setRotation()
    window.elements[3].setCoords(Coords(-20,20))
    
    window.elements.append(Checker())
    window.elements[4].setValue(True)
    window.elements[4].setCoords(Coords(20,-20))

    window.elements.append(Checker())
    window.elements[5].setValue(False)
    window.elements[5].setRotation(sense=True)
    window.elements[5].setCoords(Coords(20,20))

    window.elements.append(KeyBoard())
    window.elements[6].setRotation()
    window.elements[6].setCoords(Coords(-50,50))
    

    #Insert Code to inicialization

def showScreen():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    window.elements[1].setCoords(Coords(50,-50))
    
    window.draw()



    glFlush()

def keyboard_ascii (key,x,y):
    display = window.elements[0]
    if key == b'\x1b':#ESC
        exit()
    if key == b'0':
        display.getCheck(0).setValue(False)
        display.getCheck(1).setValue(False)
        display.getCheck(2).setValue(False)
        display.getCheck(3).setValue(False)
        window.elements[1] = NotGate()
        window.elements[6].setEntry(key)
    if key == b'1':
        display.getCheck(0).setValue(True)
        display.getCheck(1).setValue(False)
        display.getCheck(2).setValue(False)
        display.getCheck(3).setValue(False)
        window.elements[1] = AndGate()
    if key == b'2':
        display.getCheck(0).setValue(False)
        display.getCheck(1).setValue(True)
        display.getCheck(2).setValue(False)
        display.getCheck(3).setValue(False)
        window.elements[1] = OrGate()
    if key == b'3':
        display.getCheck(0).setValue(True)
        display.getCheck(1).setValue(True)
        display.getCheck(2).setValue(False)
        display.getCheck(3).setValue(False)
        window.elements[1] = XorGate()
    if key == b'4':
        display.getCheck(0).setValue(False)
        display.getCheck(1).setValue(False)
        display.getCheck(2).setValue(True)
        display.getCheck(3).setValue(False)
        window.elements[1] = NandGate()
    if key == b'5':
        display.getCheck(0).setValue(True)
        display.getCheck(1).setValue(False)
        display.getCheck(2).setValue(True)
        display.getCheck(3).setValue(False)
        window.elements[1] = NorGate()
    if key == b'6':
        display.getCheck(0).setValue(False)
        display.getCheck(1).setValue(True)
        display.getCheck(2).setValue(True)
        display.getCheck(3).setValue(False)
        window.elements[1] = XnorGate()

    window.elements[6].setEntry(key)

    showScreen()
    # Lista de caracteres
    # b'\x1b' : ESC
    # b'\x08' : BACKSPACE
    # b'\xe7' : ç
    # b'\xc7' : Ç
    # b'\r'   : Enter
    # b'\t'   : Tab
    # b'\\'   : \
    # b'a'    : a

    
    # Assign functions to keys of keyboard with ASCII code    
    return None
def keyboard_special(key,x,y):
    # Assign functions to keys of keyboard without ASCII code    
    return None
def mouse(key,x,y,s):
    # Assign functions to keys of mouse
    return None
"""
def windowResizeHandler(windowWidth:int, windowHeight:int):
    print(windowWidth)
    glClearColor(.9, 0.8, .6, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-windowWidth/4.0, windowWidth/4.0, -windowHeight/4.0, windowHeight/4.0)
    showScreen()
"""

glutInit()

glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowPosition(0, 0)
glutInitWindowSize(500,500)

wind = glutCreateWindow("Hello World")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
#glutReshapeFunc(windowResizeHandler)

glutKeyboardFunc (keyboard_ascii)
glutSpecialFunc(keyboard_special)
glutMouseFunc(mouse)

init()

glutMainLoop()

