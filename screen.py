from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from components import Entry, Checker, Display, NotGate, AndGate, NandGate, OrGate, NorGate, XorGate, XnorGate, KeyBoard
from elements import Window,WindowsBar, WindowGlobal, IconZoomMore, IconPrevious, IconStart, IconStop, IconZoomLess, IconNext, IconMoreAba,PainelComponents, WireManager,IconLineTypeInverterZ,IconLineTypeZ
from util import Coords, alfa_num_around, EVENT_TYPE_MOUSE, EVENT_TYPE_KEY_ASCII
EVENT_TYPE_MOUSE_WALKING_NOT_PRESS = 0
EVENT_TYPE_KEY_ASCII = 1
window: Window = Window()
windowGlobal: WindowGlobal = WindowGlobal()
screen = {}

wireManager: WireManager = WireManager()
def init():
    glClearColor(228/255, 233/255, 237/255, 1.0)
    
    #glClearColor(.9, 0.8, .6, 1.0)
    
    
    window.elements.append(Display())
    window.elements[0].setRotation()
    window.elements[0].setTranslation(Coords(-50, -50))

    window.elements[0].setCheck(0, True)
    window.elements[0].getCheck(1).setValue(False)
    window.elements[0].getCheck(2).setValue(False)
    window.elements[0].getCheck(3).setValue(False)

    window.elements.append(NotGate())
    window.elements[1].setRotation(sense=True)
    window.elements[1].setTranslation(Coords(50, -50))

    window.elements.append(Entry())
    window.elements[2].setValue(True)
    window.elements[2].setTranslation(Coords(-20, -20))

    window.elements.append(Entry())
    window.elements[3].setValue(False)
    window.elements[3].setRotation()
    window.elements[3].setTranslation(Coords(-20, 20))

    window.elements.append(Checker())
    window.elements[4].setValue(True)
    window.elements[4].setTranslation(Coords(20, -20))

    window.elements.append(Checker())
    window.elements[5].setValue(False)
    window.elements[5].setRotation(sense=True)
    window.elements[5].setTranslation(Coords(20, 20))

    window.elements.append(KeyBoard())
    window.elements[6].setTranslation(Coords(-50, 50))
    
    windowGlobal.tools.append(IconLineTypeZ(Coords(0,0)))
    windowGlobal.tools.append(IconLineTypeInverterZ((Coords(0,0))))
    windowGlobal.tools.append(IconNext(Coords(0,0)))
    windowGlobal.tools.append(IconPrevious(Coords(0,0)))
    windowGlobal.tools.append(IconZoomMore(Coords(0,0)))
    windowGlobal.tools.append(IconZoomLess(Coords(0,0)))
    windowGlobal.tools.append(IconStop(Coords(0,0)))
    windowGlobal.tools.append(IconStart(Coords(0,0)))
    windowGlobal.tools.append(IconMoreAba(Coords(0,0)))
    windowGlobal.configurePositionTools()
    
    # Insert Code to inicialization


def showScreen():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #window.draw()
    #wireManager.draw()

    #print("showScreen")
    
    windowGlobal.draw()
    
    glFlush()


def convert(x, y):
    return Coords((2*x-screen['width'])/5.0, (2*y-screen['height'])/5.0)


def keyboard_ascii(key, x, y):
    #if key == b'\x1b':  # ESC
     #   exit()
    #if window.event(EVENT_TYPE_KEY_ASCII, coords=convert(x, y), key=key):
        #showScreen()
    print("ism")
    windowGlobal.event(EVENT_TYPE_KEY_ASCII, key, None,None,None)
    showScreen()    
    #windowGlobal.event(EVENT_TYPE_MOUSE, key, None,None,None)
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


def keyboard_special(key, x, y):
    # Assign functions to keys of keyboard without ASCII code
    
    return None


def mouse(button, state, x, y):
    # Assign functions to keys of mouse
    #if windowGlobal.event(EVENT_TYPE_MOUSE, None, button=button, state=state, coords=convert(x, y)):
    windowGlobal.event(EVENT_TYPE_MOUSE, None, button=button, state=state, coords=convert(x, y))   
    showScreen()
   
def mouseWalkingNotPressed(x,y):
    #if windowGlobal.event(EVENT_TYPE_MOUSE_WALKING_NOT_PRESS, None, None, None, coords=convert(x, y)):
    windowGlobal.event(EVENT_TYPE_MOUSE_WALKING_NOT_PRESS, None, None, None, coords=convert(x, y))    
    showScreen()

def windowResizeHandler(width, height):
    screen['width'] = width
    screen['height'] = height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-width/5, width/5, height/5, -height/5)
    windowGlobal.setSizeWindowGlobal(Coords(width/5.0,height/5.0))
    windowGlobal.configurePositionTools()
    windowGlobal.configureWorkSetPosition()
    showScreen()


glutInit()

glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowPosition(0, 0)
glutInitWindowSize(500, 500)

wind = glutCreateWindow("Hello World")
glutDisplayFunc(showScreen)
#glutIdleFunc(showScreen)
glutReshapeFunc(windowResizeHandler)
windowResizeHandler(500, 500)

glutPassiveMotionFunc(mouseWalkingNotPressed)
glutKeyboardFunc(keyboard_ascii)
glutSpecialFunc(keyboard_special)
glutMouseFunc(mouse)

init()

glutMainLoop()
