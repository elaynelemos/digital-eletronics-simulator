from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
print("Imports successful!")

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-100.0,100.0,-100.0,100.0)

    #Insert Code to inicialization

def showScreen():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #Insert Code to draw
    
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
    return
def keyboard_special(key,x,y):
    # Assign functions to keys of keyboard without ASCII code    
    return
def mouse(key,x,y):
    # Assign functions to keys of mouse
    return
    

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

