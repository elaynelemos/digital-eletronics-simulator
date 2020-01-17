from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from components import *
from elements import *
from util import *
from logicanalyzer import *


window: Window = Window()
screen = {}

# esta primeira parte simula a interação com a interface gráfica

# primeiro caso : Check Conectado a nada
# Neste caso, deverá constar None em seu valor
checker_1 = Checker(coords=Coords(0*POINT_SPACE, 0*POINT_SPACE))
# segundo caso : Check Conectado diretamente a um Entry Válido
# Neste caso, deverá constar o valor do Entry em seu valor
checker_2 = Checker(coords=Coords(1*POINT_SPACE, 0*POINT_SPACE))
Entry_2 = Entry(coords=Coords(1*POINT_SPACE, 0*POINT_SPACE))
Entry_2.setValue(True)
# terceiro caso : Check conectado a uma porta lógica conectada diretamente a entries válidos
"""
    Neste caso, deverá constar o valor da saída da porta em seu valor,
    issó após a verificação das entradas da porta
"""
checker_3 = Checker(coords=Coords(7*POINT_SPACE, 0*POINT_SPACE))
Gate_3 = AndGate(coords=Coords(5*POINT_SPACE, 0*POINT_SPACE))

Entry_3_1 = Entry(coords=Coords(2*POINT_SPACE, -1*POINT_SPACE))
Entry_3_2 = Entry(coords=Coords(2*POINT_SPACE, 1*POINT_SPACE))
Entry_3_1.setValue(True)
Entry_3_2.setValue(True)
# quarto caso : Check conectado a uma porta lógica com entradas conectadas a outras portas lógicas
"""
    Neste caso, o checker deverá constar o valor da saída da porta em seu valor
    isso após a verificação das entradas que receberão a saida das outras duas portas
    isso após a verificação das entradas
"""
checker_4 = Checker(coords=Coords(18*POINT_SPACE, 0*POINT_SPACE))
Gate_4_1 = AndGate(coords=Coords(16*POINT_SPACE, 0*POINT_SPACE))
Gate_4_2 = AndGate(coords=Coords(11*POINT_SPACE, -1*POINT_SPACE))
Gate_4_3 = OrGate(coords=Coords(11*POINT_SPACE, 1*POINT_SPACE))
Entry_4_1 = Entry(coords=Coords(8*POINT_SPACE, -2*POINT_SPACE))
Entry_4_2 = Entry(coords=Coords(8*POINT_SPACE, 0*POINT_SPACE))
Entry_4_3 = Entry(coords=Coords(8*POINT_SPACE, 2*POINT_SPACE))
Entry_4_1.setValue(True)
Entry_4_2.setValue(True)
Entry_4_3.setValue(False)
"""
    Para não bagunçar a leitura, não foram feitas operações de rotações, nem incluida a utilização dos wires
    Para conseguir exeplificar este ultimo caso, dentro dessas condições, a Entry_4_2 é utilizada nas 2 portas Gate_4_2 e Gate_4_3
"""
# Concatenação
"""
    Esta parte simulará o algoritmo de zequinha, que concatenará todos os componentes nas 3 listas
    neste caso, serão apenas 2 listas, e a terceira(de wires) estará vazia, pelo motivo já explicado
"""
def restartSimulation():
    window.ativateSimulation()

def init():
    glClearColor(228/255, 233/255, 237/255, 1.0)
    
    #glClearColor(.9, 0.8, .6, 1.0)
    
    # Insert Code to inicialization

    #window.elements.append(checker_1)
    #window.elements.append(checker_2)
    #window.elements.append(Entry_2)
    #window.elements.append(checker_3)
    #window.elements.append(Gate_3)
    #window.elements.append(Entry_3_1)
    #window.elements.append(Entry_3_2)
    window.elements.append(checker_4)
    window.elements.append(Gate_4_1)
    window.elements.append(Gate_4_2)
    window.elements.append(Gate_4_3)
    window.elements.append(Entry_4_1)
    window.elements.append(Entry_4_2)
    window.elements.append(Entry_4_3)
#
    

    #window.elements.append(KeyBoard())
    restartSimulation()

def showScreen():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLineWidth(STROKE_WIDTH)
    if window.logic is not None:
        window.logic.analyze()
        pass

    window.draw()
    
    glFlush()


def convert(x, y):
    return Coords((2*x-screen['width'])/5.0, (2*y-screen['height'])/5.0)


def keyboard_ascii(key, x, y):
    if key == b'\x1b':  # ESC
        exit()
    if window.event(EVENT_TYPE_KEY_ASCII, coords=convert(x, y), key=key):
        
        showScreen()

    if key == b'G' or key == b'G':
        if(window.isSimulation()):
            
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
    if window.event(EVENT_TYPE_MOUSE,button = button, state = state,coords = convert(x,y)):
        restartSimulation()
        print(window.logic)
        showScreen()
   
def mouseWalkingNotPressed(x,y):
    if window.event(EVENT_TYPE_MOUSE_WALKING_NOT_PRESS,coords = convert(x,y)):
        showScreen()
    pass

def windowResizeHandler(width, height):
    screen['width'] = width
    screen['height'] = height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-width/5, width/5, height/5, -height/5)
    showScreen()


glutInit()

glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowPosition(0, 0)
glutInitWindowSize(500, 500)

wind = glutCreateWindow("Hello World")
glutDisplayFunc(showScreen)
#glutIdleFunc(showScreen)
windowResizeHandler(500, 500)
glutReshapeFunc(windowResizeHandler)

glutPassiveMotionFunc(mouseWalkingNotPressed)
glutKeyboardFunc(keyboard_ascii)
glutSpecialFunc(keyboard_special)
glutMouseFunc(mouse)

init()

glutMainLoop()
