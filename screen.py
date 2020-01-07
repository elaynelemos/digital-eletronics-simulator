from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from components import Entry,Checker, Display
from util import Coords

def init():
    glClearColor(.9, 0.8, .6, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-100.0,100.0,100.0,-100.0)

    #Insert Code to inicialization

def showScreen():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    x: Entry = Entry()
    y: Checker = Checker()
    
    
    #Insert Code to draw
    x.setValue(True)
    x.setCoords(Coords(-20,-20))
    x.draw()

    y.setValue(True)
    y.setCoords(Coords(20,-20))
    y.draw()

    x.setValue(False)
    x.setRotation()
    x.setCoords(Coords(-20,20))
    x.draw()

    y.setValue(False)
    y.setRotation(sense=True)
    y.setCoords(Coords(20,20))
    y.draw()

    display: Display = Display()
    display.setCoords(Coords(-50,-50))
    display.getCheck(0).setValue(True)
    display.getCheck(1).setValue(False)
    display.getCheck(2).setValue(False)
    display.getCheck(3).setValue(True)
    
    
    display.draw()

    glFlush()

def keyboard_ascii (key,x,y):
    if key == b'\x1b':#ESC
        exit()
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
    

glutInit()

glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowPosition(0, 0)
glutInitWindowSize(500,500)

wind = glutCreateWindow("Hello World")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)

glutKeyboardFunc (keyboard_ascii)
glutSpecialFunc(keyboard_special)
glutMouseFunc(mouse)

init()

glutMainLoop()

