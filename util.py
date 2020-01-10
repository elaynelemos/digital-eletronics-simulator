from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import traceback

from abc import ABC, abstractmethod

import math

POINT_SPACE = 5.0

EVENT_TYPE_MOUSE = 0
EVENT_TYPE_KEY_ASCII = 1
EVENT_TYPE_KEY_ESPECIAL = 2

ORIENTATION_LR = 0
ORIENTATION_UD = 1
ORIENTATION_RL = 2
ORIENTATION_DU = 3


class Color:
    __r: float = 0.0
    __g: float = 0.0
    __b: float = 0.0

    def __init__(self, r=0.0, g=0.0, b=0.0, color=None):
        if(color != None):
            self.copy(color)
        self.setR(r).setG(g).setB(b)

    def getR(self):
        return self.__r

    def getG(self):
        return self.__g

    def getB(self):
        return self.__b

    def setR(self, r: float):
        try:
            if not isinstance(r, float):  # Type validation.
                raise ValueError(
                    "ValueError: float expected to red color. You entered a(n): ", type(r))
        except ValueError as ve:
            print(ve)
            return self
        else:
            self.__r = r
            return self

    def setG(self, g: float):
        try:
            if not isinstance(g, float):  # Type validation.
                raise ValueError(
                    "ValueError: float expected to green color. You entered a(n): ", type(g))
        except ValueError as ve:
            print(ve)
            return self
        else:
            self.__g = g
            return self

    def setB(self, b: float):
        try:
            if not isinstance(b, float):  # Type validation.
                raise ValueError(
                    "ValueError: float expected to blue color. You entered a(n): ", type(b))
        except ValueError as ve:
            print(ve)
            return self
        else:
            self.__b = b
            return self

    def copy(self, color):
        self.setR(color.getR()).setG(color.getG()).setB(color.getB())
        return self

    def apply(self):
        glColor3f(self.__r, self.__g, self.__b)
        return self

    def applyClear(self):
        glClearColor(self.__r, self.__g, self.__b, 1.0)
        return self

    def __str__(self):
        return "COLOR[r="+str(self.getR())+" g="+str(self.getG())+"b="+str(self.getB())+"]"


COLOR_STROKE = Color()  # black

COLOR_TRUE = Color(r=192.0/255)
COLOR_FALSE = Color(b=192.0/255)
COLOR_NONE = Color(r=96.0/255, g=96.0/255, b=96.0/255)

STROKE_WIDTH = POINT_SPACE/2

# Element: It's a abstract Class to define some Methods to next classes


class Element(ABC):

    id: int = 0

    __name: str = ""

    def __init__(self):
        self.__name = "E" + str(Element.id)
        Element.id += 1

    def getName(self):
        return self.__name

    def setName(self, name: str):
        try:
            if not isinstance(name, str):  # Type validation.
                raise ValueError(
                    "ValueError: string expected to name. You entered a(n): ", type(name))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__name = name
            return True

    @abstractmethod
    def draw(self):

        return self

    @abstractmethod
    def isInside(self, coords) -> bool:
        return False

    @abstractmethod
    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:

        return False

    def __str__(self):
        return "[Name: "+self.getName()+"]"+str(type(self))


# Coords: It's the "data type" of a point on the screen.
class Coords(Element):
    # the attributes (private) only can be reached by getters and setters. Initiate coords with
    # invalid number for screen to be treated if there's any error in insertion.
    __x: float = None
    __y: float = None

    # the constructor of Coords receives a coordinate pair.
    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.setX(x)
        self.setY(y)

    def getX(self) -> float:
        return self.__x

    def getY(self) -> float:
        return self.__y

    def setX(self, x: float) -> bool:  # returns True if succeeds.
        # try:
        if math.isnan(x):  # Type validation.
            raise ValueError(
                "ValueError: float expected to X coordinate. You entered a(n): ", type(x))
        # except ValueError as ve:
        # traceback.print_exc()
     #   print(ve)

      #  return False
        # else:
        self.__x = x/1.0
        return True

    def setY(self, y: float) -> bool:  # returns True if succeeds.
        try:
            if math.isnan(y):  # Type validation.
                raise ValueError(
                    "ValueError: float expected to Y coordinate. You entered a(n): ", type(y))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__y = y/1.0
            return True

    def copy(self, coords):
        self.setX(coords.getX())
        self.setY(coords.getY())
        return self

    def sum(self, coords):
        return Coords(self.getX()+coords.getX(), self.getY()+coords.getY())

    def mul(self, value):
        return Coords(self.getX()*value, self.getY()*value)

    def apply(self):
        glVertex3f(self.getX(), self.getY(), 0.0)
        return self

    def draw(self, color=Color(), n_sides=15, stroke=None, radius=POINT_SPACE/3):
        color.apply()
        glBegin(GL_POLYGON)
        for i in range(n_sides):
            glVertex3f(self.getX()+radius*math.sin(i*math.pi*2/n_sides),
                       self.getY()+radius*math.cos(i*math.pi*2/n_sides), 0)
        glEnd()

        if(stroke != None):
            stroke.apply()
            glLineWidth(STROKE_WIDTH)
            glBegin(GL_LINE_LOOP)
            for i in range(n_sides):
                glVertex3f(self.getX()+radius*math.sin(i*math.pi*2/n_sides),
                           self.getY()+radius*math.cos(i*math.pi*2/n_sides), 0)
            glEnd()
            return self

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        return False

    def isInside(self, coords) -> bool:
        return False

    def in_around(self, coord, a: int, b: int = None):
        b = a if b is None else b
        c0 = coord.sum(Coords(-a, -b))
        c1 = coord.sum(Coords(a, b))
        return self.__x >= c0.getX() and self.__x <= c1.getX() and self.__y >= c0.getY() and self.__y <= c1.getY()

    def __str__(self):
        return "COORDS[x: "+str(self.getX())+" y:"+str(self.getY())+"]"

    def glTranslate(self):
        glTranslatef(self.__x, self.__y, 0.0)


def rect_around(c: Coords, a: float, b: float = None, p: int = 0):
    b = a if b == None else b

    for i in range(4):
        if(i+p) % 4 == 0:
            c.sum(Coords(-a, -b)).apply()
        if(i+p) % 4 == 1:
            c.sum(Coords(-a, +b)).apply()
        if(i+p) % 4 == 2:
            c.sum(Coords(+a, +b)).apply()
        if(i+p) % 4 == 3:
            c.sum(Coords(+a, -b)).apply()

    return None


def rect_polygon_around(c: Coords, a: float, b: float = None, p: int = 0, angle: float = 0):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    c.glTranslate()
    glRotatef(angle, 0.0, 0.0, 1.0)

    glBegin(GL_POLYGON)
    rect_around(Coords(0.0, 0.0), a, b, p)
    glEnd()

    glPopMatrix()


def line_orientation(ci: Coords, o: int, a: float = POINT_SPACE, l=True) -> Coords:
    c = Coords(0, 0).copy(ci)

    # definindo a rotação do componente
    if o % 2 == 0:  # LR or RL
        c = c.sum(Coords(-a, 0)) if int(o/2) == 0 else c.sum(Coords(a, 0))
    else:                       # UD or DU
        c = c.sum(Coords(0, -a)) if int(o/2) == 0 else c.sum(Coords(0, a))

    # Line
    if(l):
        Color().apply()
        glBegin(GL_LINES)
        ci.apply()
        c.apply()
        glEnd()

    return c


def digit_around(c: Coords, a: float, d: int, p: bool = False, bin=False):
    b = a/2
    w = a/8
    # 7 segments display based
    # segment a
    if (bin and d & 1 != 0) or (not bin and d in [0, 2, 3, 5, 6, 7, 8, 9, 10, 12, 14, 15]):
        rect_polygon_around(c.sum(Coords(0, -a)), b, w)
    # segment b
    if (bin and d & 2 != 0) or (not bin and d in [0, 1, 2, 3, 4, 7, 8, 9, 10, 13]):
        rect_polygon_around(c.sum(Coords(b, -a/2)), w, a/2)
    # segment c
    if (bin and d & 4 != 0) or (not bin and d in [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]):
        rect_polygon_around(c.sum(Coords(b, +a/2)), w, a/2)
    # segment d
    if (bin and d & 8 != 0) or (not bin and d in [0, 2, 3, 5, 6, 8, 9, 11, 12, 13, 14]):
        rect_polygon_around(c.sum(Coords(0, +a)), b, w)
    # segment e
    if (bin and d & 16 != 0) or (not bin and d in [0, 2, 6, 8, 10, 11, 12, 13, 14, 15]):
        rect_polygon_around(c.sum(Coords(-b, +a/2)), w, a/2)
    # segment f
    if (bin and d & 32 != 0) or (not bin and d in [0, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15]):
        rect_polygon_around(c.sum(Coords(-b, -a/2)), w, a/2)
    # segment g
    if (bin and d & 64 != 0) or (not bin and d in [2, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15]):
        rect_polygon_around(c, b, w)
    # segment .
    if p or bin and d & 128 != 0:
        rect_polygon_around(c.sum(Coords(b+4*w, +a)), w, w)
    return None


def alfa_num_around(c: Coords, a: float, d, p: bool = False, sc: bool = False, bin=False):
    b = a/2
    w = a/8

    # 14 segments display based

    # segments a-f (display 7 segments based)
    if bin:
        digit_around(c, a, d & 0x3F, p=p, bin=bin)
    else:
        v = 0
        v += 1 if d in [b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'I', b'O', b'P', b'Q',
                        b'R', b'S', b'T', b'Z', b'2', b'3', b'5', b'6', b'7', b'8', b'9', b'0', b'\0'] else 0
        v += 2 if d in [b'A', b'B', b'D', b'H', b'J', b'M', b'N', b'O', b'P', b'Q',
                        b'R', b'U', b'W', b'1', b'2', b'3', b'4', b'7', b'8', b'9', b'0', b'\0'] else 0
        v += 4 if d in [b'A', b'B', b'D', b'G', b'H', b'J', b'M', b'N', b'O', b'Q', b'S',
                        b'U', b'W', b'1', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0', b'\0'] else 0
        v += 8 if d in [b'B', b'C', b'D', b'E', b'G', b'I', b'J', b'L', b'O', b'Q',
                        b'S', b'U', b'Z', b'2', b'3', b'5', b'6', b'8', b'9', b'0', b'\0'] else 0
        v += 16 if d in [b'A', b'C', b'E', b'F', b'G', b'H', b'J', b'K', b'L', b'M', b'N',
                         b'O', b'P', b'Q', b'R', b'U', b'V', b'W', b'2', b'6', b'8', b'0', b'\0'] else 0
        v += 32 if d in [b'A', b'C', b'E', b'F', b'G', b'H', b'K', b'L', b'M', b'N', b'O', b'P',
                         b'Q', b'R', b'S', b'U', b'V', b'W', b'4', b'5', b'6', b'8', b'9', b'0', b'\0'] else 0
        digit_around(c, a, v, p, bin=True)

    # segment g
    if (bin and d & 64 != 0) or (not bin and d in [b'A', b'E', b'F', b'H', b'K', b'P', b'R', b'S', b'2', b'4', b'5', b'6', b'8', b'9', b'\0']):
        rect_polygon_around(c.sum(Coords(-b/2, 0)), b/2, w)

    # segment h
    if (bin and d & 128 != 0) or (not bin and d in [b'M', b'N', b'X', b'Y', b'\0']):
        rect_polygon_around(c.sum(Coords(-b/2, -a/2)), a/2, w, angle=63.7)

    # segment j
    if (bin and d & 256 != 0) or (not bin and d in [b'B', b'D', b'I', b'T', b'\0']):
        rect_polygon_around(c.sum(Coords(0, -a/2)), w, a/2)
    # segment k
    if (bin and d & 512 != 0) or (not bin and d in [b'K', b'M', b'V', b'X', b'Y', b'Z', b'1', b'0', b'\0']):
        rect_polygon_around(c.sum(Coords(b/2, -a/2)), a/2, w, angle=-63.7)
    # segment m
    if (bin and d & 1024 != 0) or (not bin and d in [b'A', b'B', b'G', b'H', b'P', b'R', b'S', b'2', b'3', b'4', b'5', b'6', b'8', b'9', b'\0']):
        rect_polygon_around(c.sum(Coords(b/2, 0)), b/2, w)
    # segment n
    if (bin and d & 2048 != 0) or (not bin and d in [b'K', b'N', b'Q', b'R', b'W', b'X', b'\0']):
        rect_polygon_around(c.sum(Coords(b/2, a/2)), a/2, w, angle=63.7)
    # segment p
    if (bin and d & 4096 != 0) or (not bin and d in [b'B', b'D', b'I', b'T', b'Y', b'\0']):
        rect_polygon_around(c.sum(Coords(0, a/2)), w, a/2)
    # segment r
    if (bin and d & 8192 != 0) or (not bin and d in [b'V', b'W', b'X', b'Z', b'0', b'\0']):
        rect_polygon_around(c.sum(Coords(-b/2, a/2)), a/2, w, angle=-63.7)
