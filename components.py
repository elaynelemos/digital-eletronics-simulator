"""
*   Universidade Federal do Vale do São Francisco - Univasf
*   Colegiado de Engenharia de Computação
*   Orientador: Prof. Dr. Jorge Cavalcanti
*   Discentes: Elayne Lemos, elayne.l.lemos@gmail.com
*              Jônatas de Castro, jonatascastropassos@gmail.com
               Ezequias Antunes, ezequiasantunes18@gmail.com
*   Atividade: pt-br/ este código parametriza os elementos entrada (Entry), porta (Gate) e conector (Wire) 
*                     do simulador de eletrônica digital enquanto define a manipulação básica.
*              en-us/ this code parametrize the elements Entry, Gate and Wire of the digital eletronics
*                     simulator while defines the basic manipulation of it.
*
"""

from __future__ import annotations

from typing import List
from operator import xor
from util import *
# import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math


N_ENTRIES = 2


# Entry: Represents a logic entry. It has a value itself.
#       Then cannot be connected to other entries (only outputs its own value).
class Entry(Element):
    # the attributes (private) only can be reached by getters and setters.
    __value: bool = None
    __coords: Coords = None
    __orientation = ORIENTATION_LR
    __size = POINT_SPACE*4
    __gate = None
    __keyboard = None
    id = 0
    # the constructor of Entry receives a logic value and the Coords where the entry should be placed.
    def __init__(self, coords: Coords = Coords(0.0, 0.0), size=POINT_SPACE*4, gate=None,keyboard = None):
        #super().__init__()
        self.setName("E"+str(Entry.id))
        Entry.id+=1
        self.__size = size
        self.setCoords(coords)
        self.__gate = gate
        self.__keyboard = keyboard

    def getValue(self) -> bool:
        return self.__value

    def getCoords(self) -> Coords:
        return self.__coords

    def setValue(self, value: bool):  # returns True if succeeds.
        try:
            if value != None and not(isinstance(value, bool)):
                raise ValueError(
                    "ValueError: Logic value expected to entry. You entered a(n): ", type(value))
        except ValueError as ve:
            return self
        else:
            self.__value = value
            return self

    def toogleV(self) -> bool:
        try:
            if self.__value is not None:
                self.__value = xor(self.__value, True)
                return True
            else:
                raise AttributeError("Entry value not defined!")
        except AttributeError as ae:
            print(ae)
            return False

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        return True

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation

    def setTranslation(self, coords=Coords):
        self.setCoords(coords)
        return self

    def __getC(self):
        return line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*3/4)

    def __getD(self):
        return line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*1/4, l=True)

    def isGateOut(self):
        return self.__gate != None

    def getGate(self):
        return self.__gate

    def draw(self, n = True):
        # line
        c = self.__getC()
        d = self.__getD()

        # Polygon
        if self.__value == True:
            COLOR_TRUE.apply()
        elif self.__value == False:
            COLOR_FALSE.apply()
        else:
            COLOR_NONE.apply()

        glBegin(GL_POLYGON)
        rect_around(c, 1/4*self.__size, p=3-self.__orientation)
        d.apply()
        glEnd()

        # bord
        COLOR_STROKE.apply()
        # glLineWidth(STROKE_WIDTH)
        glBegin(GL_LINE_LOOP)
        rect_around(c, 1/4*self.__size, p=3-self.__orientation)
        d.apply()
        glEnd()

        # number
        if self.__value == True:
            digit_around(c, 1/4*0.6*self.__size, 1)
        elif self.__value == False:
            digit_around(c, 1/4*0.6*self.__size, 0)
        else:
            digit_around(c, 1/4*0.6*self.__size, -1)

        # name
        Color().apply()
        if(n):
            text_right(self.getName(),c.sum(Coords(0,5/12*self.__size*(-1 if self.__orientation != ORIENTATION_UD else 1))))

        # self.getCoords().draw()

        return self

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        print("esta invertendo")
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_UP and self.isInside(coords):
         
            self.toogleV()
            return True
        return False

    def isInside(self, coords) -> bool:
        c = self.__getC()
        d = self.__getD()
        m = c.middle(d)
        m1 = line_orientation(m, (self.__orientation+1) %
                              4, a=self.__size/4, l=False)
        m2 = line_orientation(m, (self.__orientation+3) %
                              4, a=self.__size/4, l=False)
        return coords.in_around(c, self.__size/4) or is_inside_triangle(coords, [d, m1, m2])

    def __str__(self):
        return super().__str__()+ (" of "+str(self.__keyboard) if self.__keyboard is not None else "") + (" of "+str(self.__gate) if self.__gate is not None else "")


class Checker(Element):
    # the attributes (private) only can be reached by getters and setters.
    __value: bool = None
    __coords: Coords = None
    __orientation = ORIENTATION_RL
    __size = POINT_SPACE*3
    __checked = False
    __display = None
    __gate = None
    id = 0
    # the constructor of Entry receives a logic value and the Coords where the entry should be placed.
    def __init__(self, coords: Coords = Coords(0.0, 0.0), size=POINT_SPACE*3, display = None, gate = None):
        #super().__init__()
        self.setName("C"+str(Checker.id))
        Checker.id+=1
        self.__size = size
        self.setCoords(coords)
        self.__display = display
        self.__gate = gate

    def getValue(self) -> bool:
        return self.__value

    def getChecked(self) -> bool:
        return self.__checked

    def getCoords(self) -> Coords:
        return self.__coords

    def setValue(self, value: bool) -> bool:  # returns True if succeeds.
        try:
            if not(isinstance(value, bool)) and value != None:
                raise ValueError(
                    "ValueError: Logic value expected to entry. You entered a(n): ", type(value))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__value = value
            return True

    def setChecked(self, checked: bool) -> bool:
        self.__checked = checked

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        return True

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation

    def setTranslation(self, coords=Coords):
        self.setCoords(coords)
        return self

    def draw(self,n= True):
        # line
        c = line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*2/3, l=True)

        # Polygon
        if self.__value == True:
            COLOR_TRUE.apply()
        elif self.__value == False:
            COLOR_FALSE.apply()
        else:
            COLOR_NONE.apply()

        glBegin(GL_POLYGON)
        rect_around(c, 1/3*self.__size, p=3-self.__orientation)
        glEnd()

        # bord
        COLOR_STROKE.apply()
        # glLineWidth(STROKE_WIDTH)
        glBegin(GL_LINE_LOOP)
        rect_around(c, 1/3*self.__size, p=3-self.__orientation)
        glEnd()

        # number
        if self.__value == True:
            digit_around(c, 1/4*0.6*self.__size, 1)
        elif self.__value == False:
            digit_around(c, 1/4*0.6*self.__size, 0)
        else:
            digit_around(c, 1/4*0.6*self.__size, -1)

        # name
        Color().apply()
        if(n):
            text_right(self.getName(),c.sum(Coords(0,5/12*self.__size*(-1 if self.__orientation != ORIENTATION_UD else 1))))

        # self.getCoords().draw()

        return self

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:

        return False

    def isInside(self, coords) -> bool:
        c = line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*2/3)
        return coords.in_around(c, self.__size/3)

    def __str__(self):
        return super().__str__()+ (" of "+str(self.__display) if self.__display is not None else "")+ (" of "+str(self.__gate) if self.__gate is not None else "")


class Display(Element):
    __checks: List[Checker] = None
    __coords: Coords = None
    __fill: Color = Color()
    __ligh_on: Color = Color(r=1.0)
    __ligh_off: Color = Color(r=0.2)
    __orientation = ORIENTATION_RL
    __size = POINT_SPACE*4
    id = 0
    def __init__(self, coords: Coords = Coords(0.0, 0.0), size=POINT_SPACE*4):
        self.setName("D"+str(Display.id))
        Display.id+=1
        self.setCoords(coords)
        self.__size = size
        self.__updateCoords()

    def __updateCoords(self):
        c = Coords(0.0, 0.0)
        self.__checks = []
        for i in range(4):
            self.__checks.append(Checker(display = self))
            # definindo a rotação do componente
            if self.__orientation % 2 == 0:  # LR or RL
                self.__checks[i].setCoords(c.sum(Coords(self.__size*1/2, self.__size*1/4 - i*self.__size*1/4)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(-self.__size*1/2, -self.__size*1/4 + i*self.__size*1/4)))
            else:                       # UD or DU
                self.__checks[i].setCoords(c.sum(Coords(-self.__size*1/4 + i*self.__size*1/4, self.__size*1/2)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(self.__size*1/4 - i*self.__size*1/4, -self.__size*1/2)))

    def getCheck(self, i: int):
        if(i < 4 and i >= 0):
            return self.__checks[i]
        return None

    def getChecks(self):
        return self.__checks

    def setCheck(self, i: int, v: bool):
        if(i < 4 and i >= 0):
            self.__checks[i].setValue(v)
        return self

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        return True

    def getCoords(self) -> Coords:
        return self.__coords

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation

        self.__updateCoords()
        return self

    def setTranslation(self, coords=Coords):
        c = line_orientation(
            Coords(0.0,0.0), self.__orientation, a=self.__size*1/2, l=False)
        c = line_orientation(c, (self.__orientation+1) % 4, a=self.__size*1/4)
        #c = c.mul(-1)
        self.setCoords(coords.sum(c))
        return self

    def rectCenter(self):
        return line_orientation(line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*1/8, l=False), (self.__orientation+1) % 4, a=self.__size*1/8, l=False)

    def draw(self,n= True):
        v = 0
        for i in range(4):
            v += (2**i)*(1 if self.__checks[i].getValue() else 0)

        # Rect

        self.__fill.apply()

        glBegin(GL_POLYGON)
        rect_around(self.rectCenter(), (self.__size*3/8 if self.__orientation % 2 == 0 else self.__size *
                                        1/2), (self.__size*1/2 if self.__orientation % 2 == 0 else self.__size*3/8))
        glEnd()

        # OFF Digit
        self.__ligh_off.apply()
        digit_around(self.rectCenter(), self.__size *
                     (0.9 if self.__orientation % 2 == 0 else 0.75)/3, 8, p=True)

        # ON Digit
        self.__ligh_on.apply()
        digit_around(self.rectCenter(), self.__size *
                     (0.9 if self.__orientation % 2 == 0 else 0.75)/3, v)

        # set center
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.__coords.glTranslate()

        for ckeck in self.__checks:
            point = line_orientation(
                ckeck.getCoords(), self.__orientation, l=True, a=self.__size/4)
            if ckeck.getValue() == True:
                COLOR_TRUE.apply()
            elif ckeck.getValue() == False:
                COLOR_FALSE.apply()
            else:
                COLOR_NONE.apply()
            rect_polygon_around(point, self.__size/16)

        glPopMatrix()
        c = self.rectCenter()
        # name
        Color().apply()
        if(n):
            if self.__orientation%2 == 0:
                text_right(self.getName(),c.sum(Coords(0,-5/8*self.__size)))
            elif self.__orientation == ORIENTATION_UD:
                text_right(self.getName(),c.sum(Coords(0,-5/8*self.__size)))
            elif self.__orientation == ORIENTATION_DU:
                text_right(self.getName(),c.sum(Coords(0,5/8*self.__size)))

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        # if(event_type==EVENT_TYPE_MOUSE and state == GLUT_DOWN and self.isInside(coords)):
         #   print("Clicou dentro")
        return False

    def isInside(self, coords) -> bool:
        return coords.in_around(self.rectCenter(), (self.__size*3/8 if self.__orientation % 2 == 0 else self.__size/2), b=(self.__size/2 if self.__orientation % 2 == 0 else self.__size*3/8))


class KeyBoard(Element):
    __entries: List[Entry] = []
    __coords: Coords = None
    __fill: Color = Color(r=0.8, g=0.7, b=0.6)
    __ligh_on: Color = Color(r=1.0)
    __ligh_off: Color = Color(r=0.2)
    __orientation = ORIENTATION_LR
    __size = POINT_SPACE*4
    id = 0
    def __init__(self, coords: Coords = Coords(0.0, 0.0), size=POINT_SPACE*4):
        self.setName("K"+str(KeyBoard.id))
        KeyBoard.id+=1
        self.setCoords(coords)
        self.__size = size
        self.__updateCoords()

    def __updateCoords(self):
        c = Coords(0.0, 0.0)
        self.__entries = []
        for i in range(4):
            self.__entries.append(Entry(keyboard = self))
            # definindo a rotação do componente
            if self.__orientation % 2 == 0:  # LR or RL
                self.__entries[i].setCoords(c.sum(Coords(self.__size*1/2, -self.__size*1/4 + i*self.__size*1/4)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(-self.__size*1/2, self.__size*1/4 - i*self.__size*1/4)))
            else:                       # UD or DU
                self.__entries[i].setCoords(c.sum(Coords(self.__size*1/4 - i*self.__size*1/4, self.__size*1/2)) if int(
                    self.__orientation/2) == 0 else c.sum(Coords(-self.__size*1/4 + i*self.__size*1/4, -self.__size*1/2)))

    def getEntry(self, i: int):
        if(i < 4 and i >= 0):
            return self.__entries[i]
        return None

    def getEntries(self):
        return self.__entries

    def getCoords(self) -> Coords:
        return self.__coords

    def setEntry(self, v: bytes):
        b0 = v in [b'1', b'3', b'5', b'7', b'9',
                   b'B', b'b', b'D', b'd', b'F', b'f']
        b1 = v in [b'2', b'3', b'6', b'7', b'A',
                   b'a', b'B', b'b', b'E', b'e', b'F', b'f']
        b2 = v in [b'4', b'5', b'6', b'7', b'C',
                   b'c', b'D', b'd', b'E', b'e', b'F', b'f']
        b3 = v in [b'8', b'9', b'A', b'a', b'B', b'b',
                   b'C', b'c', b'D', b'd', b'E', b'e', b'F', b'f']
        self.__entries[0].setValue(b0)
        self.__entries[1].setValue(b1)
        self.__entries[2].setValue(b2)
        self.__entries[3].setValue(b3)

        return b0 or b1 or b2 or b3 or v == b'0'

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        return True

    def __setCenter(self):
        self.rectCenter().glTranslate()
        glRotatef(90.0*self.__orientation, 0.0, 0.0, 1.0)

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation

        self.__updateCoords()
        return self

    def setTranslation(self, coords=Coords):
        c = line_orientation(
            Coords(0.0,0.0), self.__orientation, a=self.__size*1/2, l=False)
        c = line_orientation(c, (self.__orientation+1) % 4, a=self.__size*1/4)
        #c = c.mul(-1)
        self.setCoords(coords.sum(c))
        return self

    def rectCenter(self):
        return line_orientation(line_orientation(
            self.getCoords(), self.__orientation, a=self.__size*1/8, l=False), (self.__orientation+3) % 4, a=self.__size*1/8, l=False)

    def draw(self,n= True):
        v = 0
        for i in range(4):
            v += (2**i)*(1 if self.__entries[i].getValue() else 0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.__setCenter()

        self.__fill.apply()
        glBegin(GL_POLYGON)
        rect_around(Coords(0.0, 0.0), self.__size*3/8, b=self.__size/2)
        glEnd()

        COLOR_STROKE.apply()
        glBegin(GL_LINE_LOOP)
        rect_around(Coords(0.0, 0.0), self.__size*3/8, b=self.__size/2)
        glEnd()

        self.__ligh_off.apply()
        glBegin(GL_POLYGON)
        rect_around(Coords(0.0, -self.__size*5/16),
                    self.__size/4, b=self.__size/8)
        glEnd()

        glPushMatrix()
        Coords(0.0, -self.__size*5/16).glTranslate()
        glRotatef(-90.0*self.__orientation, 0.0, 0.0, 1.0)

        self.__ligh_on.apply()
        digit_around(Coords(0.0, 0.0), self.__size *
                     (0.40 if self.__orientation % 2 == 0 else 0.65)/4, v)

        glPopMatrix()

        COLOR_STROKE.apply()
        glBegin(GL_LINES)
        for i in range(5):
            Coords(self.__size/8*(-2+i), -self.__size/8).apply()
            Coords(self.__size/8*(-2+i), self.__size*3/8).apply()

        for i in range(5):
            Coords(-self.__size/4, self.__size/8 * (-1 + i)).apply()
            Coords(self.__size/4, self.__size/8 * (-1 + i)).apply()
        glEnd()

        glPopMatrix()

        for entry in self.__entries:
            point = line_orientation(entry.getCoords().sum(
                self.__coords), self.__orientation, self.__size/4)
            if entry.getValue() == True:
                COLOR_TRUE.apply()
            elif entry.getValue() == False:
                COLOR_FALSE.apply()
            else:
                COLOR_NONE.apply()
            rect_polygon_around(point, self.__size/16)
        c = self.rectCenter()
        # name
        Color().apply()
        if(n):
            if self.__orientation%2 == 0:
                text_right(self.getName(),c.sum(Coords(0,-5/8*self.__size)))
            elif self.__orientation == ORIENTATION_UD:
                text_right(self.getName(),c.sum(Coords(0,-5/8*self.__size)))
            elif self.__orientation == ORIENTATION_DU:
                text_right(self.getName(),c.sum(Coords(0,5/8*self.__size)))

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        if(event_type == EVENT_TYPE_MOUSE and state == GLUT_DOWN and self.isInside(coords)):
            print("Clicou dentro")
        if event_type == EVENT_TYPE_KEY_ASCII and self.isInside(coords):
            return self.setEntry(key)

        return False

    def isInside(self, coords) -> bool:
        return coords.in_around(self.rectCenter(), (self.__size*3/8 if self.__orientation % 2 == 0 else self.__size/2), b=(self.__size/2 if self.__orientation % 2 == 0 else self.__size*3/8))

# Gate: Represents the main logic gates (or, and, xor, nor, nand) those must receives a pair of
#      logic values and are able to output its interpretation.


class Gate(Element):
    id: int = 0
    # the attributes (private) only can be reached by getters and setters.
    __checks: List[Checker] = []
    __coords: Coords = None
    __out: Entry = None

    __fill: Color = Color(r=0.4, g=0.6, b=0.4)
    __orientation = ORIENTATION_LR
    __size = POINT_SPACE*5

    # the constructor of Gate receives the gate type, two logic values and the Coords where it
    # should be placed.
    def __init__(self, coords: Coords = Coords(0.0, 0.0), size=POINT_SPACE*5):
        self.setCoords(coords)  # position of the gate
        self.setName("G" + str(Gate.id))
        Gate.id += 1
        self.__size = size
        self.__updateCoords()

    def getIn(self, i: int) -> Checker:
        try:
            if self.__checks is not None and len(self.__checks) > i and self.__checks[i] is not None:
                return self.__checks[i]
            else:
                raise AttributeError("Entry not defined!")
        except AttributeError as ae:
            print(ae)
            return None

    def getChecks(self):
        return self.__checks

    def resetEntries(self):
        self.__checks = []
        self.__out = Entry(gate=self)

    def getCoords(self) -> Coords:
        return self.__coords

    def getFill(self):
        return self.__fill

    def getOrientation(self):
        return self.__orientation

    def getSize(self):
        return self.__size

    def setIn(self, i: int, v: bool) -> bool:  # returns True if succeeds.
        try:
            if self.__checks is not None and len(self.__checks) > i and self.__checks[i] is not None:
                self.__checks[i].setValue(v)
                return True
            else:
                raise AttributeError("Entry not defined!")
        except AttributeError as ae:
            print(ae)
            return False

    # returns True if both coords are valid.
    def setCoords(self, coords: Coords) -> Gate:
        self.__coords = coords
        self.__updateCoords()
        return self

    def setRotation(self, sense=False):
        self.__orientation = self.__orientation + (1 if sense else -1)
        self.__orientation = 0 if self.__orientation > 3 else self.__orientation
        self.__orientation = 3 if self.__orientation < 0 else self.__orientation
        self.__updateCoords()

    def setTranslation(self, coords: Coords):
        c = line_orientation(
            Coords(0.0,0.0), (self.__orientation+2) % 4, a=self.__size*2/5)
        c = c.mul(-1)
        self.setCoords(coords.sum(c))
        return self

    def __updateCoords(self) -> Gate:
        self.resetEntries()

        # If is not a Not Gate, then will have two entries
        self.__checks.append(Checker(gate = self))
        self.__checks.append(Checker(gate = self))

        # Configures orientation
        self.__out.setCoords(line_orientation(
            self.__coords, (self.__orientation+2) % 4, a=self.__size*2/5, l=False))
        middle = line_orientation(
            self.__coords, self.__orientation, a=self.__size*3/5, l=False)
        self.__checks[1].setCoords(line_orientation(
            middle, (self.__orientation+1) % 4, a=self.__size/5, l=False))
        self.__checks[0].setCoords(line_orientation(
            middle, (self.__orientation+3) % 4, a=self.__size/5, l=False))

    def gateOut(self) -> Entry:
        return self.__out

    def getCenter(self):
        return line_orientation(self.__coords, self.__orientation, a=self.__size*1/10, l=False)

    def setCenter(self):
        self.getCenter().glTranslate()
        glRotatef(90.0*self.__orientation, 0.0, 0.0, 1.0)

    def normalize(self, coords: Coords) -> Coords:
        coords = coords.sum(self.getCenter().mul(-1))
        if self.__orientation == 1:
            temp = coords.getY()
            coords.setY(-coords.getX())
            coords.setX(temp)
        if self.__orientation == 2:
            coords.setX(-coords.getX())
            coords.setY(-coords.getY())
        if self.__orientation == 3:
            temp = coords.getY()
            coords.setY(coords.getX())
            coords.setX(-temp)
        return coords

    def getD(self):
        return line_orientation(self.__out.getCoords(), self.__orientation, self.__size/5, l=False)

    def draw(self,n= True):
        # self.getCoords().draw()
        for check in self.__checks:
            line_orientation(check.getCoords(), (self.__orientation+2) % 4, self.__size/2)
        line_orientation(self.__out.getCoords(), self.__orientation, self.__size/5)

        # name
        Color().apply()
        c = self.getCenter()
        if(n):
            if self.__orientation%2 == 0:
                text_right(self.getName(),c.sum(Coords(0,-self.__size*3/10)))
            else:
                text_right(self.getName(),c.sum(Coords(self.__size*4/10,0)))

        return self

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        return False


class NotGate(Gate):
    def __init__(self, coords: Coords = Coords(0.0, 0.0), size=POINT_SPACE*5):
        super().__init__(coords, size=size)
        self.__updateCoords()

    def __updateCoords(self) -> Gate:
        self.resetEntries()

        # If is not a Not Gate, then will have two entries
        self.getChecks().append(Checker(gate = self))

        # Configures orientation
        self.gateOut().setCoords(line_orientation(self.getCoords(),
                                                  (self.getOrientation()+2) % 4, a=self.getSize()*2/5, l=False))
        self.getIn(0).setCoords(line_orientation(self.getCoords(),
                                                 self.getOrientation(), a=self.getSize()*3/5, l=False))

    def setCoords(self, coords: Coords) -> Gate:
        super().setCoords(coords)
        self.__updateCoords()
        return self

    def setTranslation(self, coords: Coords):
        c = line_orientation(
            Coords(0.0,0.0), (self.getOrientation()+2) % 4, a=self.getSize()*2/5)
        c = c.mul(-1)
        self.setCoords(coords.sum(c))
        return self


    def setRotation(self, sense=False):
        super().setRotation(sense=sense)
        self.__updateCoords()

    def gateOut(self) -> Entry:
        entry = super().gateOut()
        if None in self.getChecks():
            return entry.setValue(None)
        return entry.setValue(not self.getIn(0).getValue())

    def draw(self,n= True):
        super().draw(n=n)
        point = self.getD()

        # set center
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.setCenter()

        # Polygon
        self.getFill().apply()
        glBegin(GL_POLYGON)
        Coords(self.getSize()*3/10, 0.0).apply()
        Coords(-self.getSize()*3/10, -self.getSize()/5).apply()
        Coords(-self.getSize()*3/10, self.getSize()/5).apply()
        glEnd()

        # bord
        # Polygon
        COLOR_STROKE.apply()
        glBegin(GL_LINE_LOOP)
        Coords(self.getSize()*3/10, 0.0).apply()
        Coords(-self.getSize()*3/10, -self.getSize()/5).apply()
        Coords(-self.getSize()*3/10, self.getSize()/5).apply()
        glEnd()

        glPopMatrix()

        point.draw(color=Color(r=1.0, g=1.0, b=1.0), stroke=Color(),radius = self.getSize()*3/40)

        return self

    def isInside(self, coords) -> bool:
        coords = self.normalize(coords)
        ret = is_inside_triangle(coords, [Coords(self.getSize()*3/10, 0.0), Coords(-self.getSize()*3/10, -self.getSize()/5), Coords(-self.getSize()*3/10, self.getSize()/5)])
        print(ret)
        return ret

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        if(event_type == EVENT_TYPE_MOUSE and state == GLUT_DOWN and self.isInside(coords)):
            print("Clicou dentro")
        return False


class AndGate(Gate):
    def gateOut(self) -> Entry:
        entry = super().gateOut()
        if None in self.getChecks():
            return entry.setValue(None)
        return entry.setValue(self.getIn(0).getValue() and self.getIn(1).getValue())

    def listPoints(self):
        ret = []
        ret.append(Coords(self.getSize()*1/10, self.getSize()/5))
        ret.append(Coords(self.getSize()*9/40, self.getSize()*3/20))
        ret.append(Coords(self.getSize()*11/40, self.getSize()/10))
        ret.append(Coords(self.getSize()*3/10, 0))
        ret.append(Coords(self.getSize()*11/40, -self.getSize()/10))
        ret.append(Coords(self.getSize()*9/40, -self.getSize()*3/20))
        ret.append(Coords(self.getSize()*1/10, -self.getSize()/5))
        ret.append(Coords(-self.getSize()*3/10, -self.getSize()/5))
        ret.append(Coords(-self.getSize()*3/10, self.getSize()/5))
        return ret

    def draw(self,n= True):
        super().draw(n=n)

        # set center
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.setCenter()
        l = self.listPoints()
        # Polygon
        self.getFill().apply()
        glBegin(GL_POLYGON)
        for i in l:
            i.apply()
        glEnd()

        # bord
        # Polygon
        COLOR_STROKE.apply()
        glBegin(GL_LINE_LOOP)
        for i in l:
            i.apply()
        glEnd()

        glPopMatrix()

        return self

    def isInside(self, coords) -> bool:
        ret = False
        coords = self.normalize(coords)
        cs = self.listPoints()
        c1 = cs[0]
        del(cs[0])
        for i in range(len(cs)-1):
            ret = ret or is_inside_triangle(coords,[c1,cs[i],cs[i+1]])
        
        return ret

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        #if(event_type == EVENT_TYPE_MOUSE and state == GLUT_DOWN and self.isInside(coords)):
        #    print("Clicou dentro")
        return False


class NandGate(AndGate):
    def gateOut(self) -> Entry:
        entry = super().gateOut()
        if None in self.getChecks():
            return entry.setValue(None)
        return entry.setValue(not(self.getIn(0).getValue()
                                  and self.getIn(1).getValue()))

    def draw(self,n= True):
        super().draw(n=n)
        point = self.getD()
        point.draw(color=Color(r=1.0, g=1.0, b=1.0), stroke=Color(),radius = self.getSize()*3/40)
        return self


class OrGate(Gate):

    def gateOut(self) -> Entry:
        entry = super().gateOut()
        if None in self.getChecks():
            return entry.setValue(None)
        return entry.setValue(self.getIn(0).getValue() or self.getIn(1).getValue())

    def listPoints(self):
        ret = []
        ret.append(Coords(self.getSize()*2/10, -self.getSize()/10))
        ret.append(Coords(self.getSize()*1/10, -self.getSize()*3/20))
        ret.append(Coords(0, -self.getSize()*0.19))
        ret.append(Coords(-self.getSize()*0.3, -self.getSize()*0.2))
        ret.append(Coords(-self.getSize()*0.22, -self.getSize()*0.1))
        ret.append(Coords(-self.getSize()*0.2, 0))
        ret.append(Coords(-self.getSize()*0.22, +self.getSize()*0.1))
        ret.append(Coords(-self.getSize()*0.3, +self.getSize()*0.2))
        ret.append(Coords(0, self.getSize()*0.19))
        ret.append(Coords(self.getSize()*1/10, self.getSize()*3/20))
        ret.append(Coords(self.getSize()*2/10, self.getSize()/10))
        ret.append(Coords(self.getSize()*3/10, 0))
        return ret

    def draw(self,n= True):
        super().draw(n=n)

        # set center
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.setCenter()
        l = self.listPoints()
        # Polygon
        self.getFill().apply()
        glBegin(GL_POLYGON)
        for i in l:
            i.apply()
        glEnd()

        # bord
        # Polygon
        COLOR_STROKE.apply()
        glBegin(GL_LINE_LOOP)
        for i in l:
            i.apply()
        glEnd()

        


        glPopMatrix()

        return self

    def isInside(self, coords) -> bool:
        ret = False
        coords = self.normalize(coords)
        cs = self.listPoints()
        c1 = cs[0]
        del(cs[0])
        for i in range(len(cs)-1):
            ret = ret or is_inside_triangle(coords,[c1,cs[i],cs[i+1]])
        
        return ret

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        #if(event_type == EVENT_TYPE_MOUSE and state == GLUT_DOWN and self.isInside(coords)):
        #    print("Clicou dentro")
        return False


class NorGate(OrGate):

    def gateOut(self) -> Entry:
        entry = super().gateOut()
        if None in self.getChecks():
            return entry.setValue(None)
        return entry.setValue(not(self.getIn(0).getValue()
                                  or self.getIn(1).getValue()))

    def draw(self,n= True):
        super().draw(n=n)
        point = self.getD()
        point.draw(color=Color(r=1.0, g=1.0, b=1.0), stroke=Color(),radius = self.getSize()*3/40)
        return self


class XorGate(OrGate):

    def gateOut(self) -> Entry:
        entry = super().gateOut()
        if None in self.getChecks():
            return entry.setValue(None)
        return entry.setValue(self.getIn(0).getValue() != self.getIn(1).getValue())

    def draw(self,n= True):
        super().draw(n=n)

        # set center
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        self.setCenter()

        # bord
        COLOR_STROKE.apply()
        glBegin(GL_LINE_STRIP)

        Coords(-self.getSize()*0.37, -self.getSize()*0.2).apply()
        Coords(-self.getSize()*0.29, -self.getSize()*0.1).apply()
        Coords(-self.getSize()*0.27, 0).apply()
        Coords(-self.getSize()*0.29, +self.getSize()*0.1).apply()
        Coords(-self.getSize()*0.37, +self.getSize()*0.2).apply()

        glEnd()

        glPopMatrix()

        return self


class XnorGate(XorGate):

    def gateOut(self) -> Entry:
        entry = super().gateOut()
        if None in self.getChecks():
            return entry.setValue(None)
        return entry.setValue(self.getIn(0).getValue() == self.getIn(1).getValue())

    def draw(self,n= True):
        super().draw(n=n)
        point = self.getD()
        point.draw(color=Color(r=1.0, g=1.0, b=1.0), stroke=Color(),radius = self.getSize()*3/40)
        return self

# Wire: Represents the connector of the logic circuit. It's defined as a list of unique
#      Coords. Once connected to an logic component carries its value from start to end points.


class Wire(Element):
    fill: Color = Color(g=64.0/255)
    # the attributes (private) only can be reached by getters and setters.
    __points: List[Coords] = []

    # the constructor of Wire receives a list of Coords (points) to define itself.
    def __init__(self, points: List[Coords]) -> None:
        super().__init__()
        self.insertWireP(points)

    # TODO #fix insertion function
    # returns true if points is correctly inserted.
    def insertWireP(self, points: List[Coords]) -> bool:
        ctrl = True
        try:
            for i in points:
                x = i.getX()
                y = i.getY()
                if x >= 0 and y >= 0:
                    for j in self.__points:
                        if j.getX() == x and j.getY() == y:
                            ctrl = False
                            break
                    if ctrl:
                        self.__points.append(i)
                    ctrl = True
            # self.refactorWire()
            # validation of condition to be a wire (line).
            if len(self.__points) < 2:
                raise AttributeError("Not enough points to a wire!")
        except AttributeError as ae:
            self.__points = []
            print(ae)
            return False
        else:
            return True

    def getWireP(self) -> List[Coords]:
        return self.__points

    def getWireStartP(self) -> Coords:
        return self.__points[0]

    def getWireEndP(self) -> Coords:
        l = len(self.__points)
        if l > 0:
            return self.__points[l-1]
        else:
            return self.__points[0]

    def getWirePreEndP(self) -> Coords:
        l = len(self.__points)
        if l > 1:
            return self.__points[l-2]
        else:
            return self.__points[0]

    def getWireNextP(self, reference: Coords) -> Coords:
        for i in self.__points:
            if i.getX() == reference.getX() and i.getY() == reference.getY():
                return self.__points[self.__points.index(i) + 1]

    # TODO fix refactor function
    # reduce the number of points if they are at the same line.
    def refactorWire(self) -> None:
        ctrl = len(self.__points)-2
        i = 0
        while (ctrl - i):
            if self.__points[i].getX() == self.__points[i+1].getX() and self.__points[i].getX() == self.__points[i+2].getX():
                del(self.__points[i+1])
                ctrl = len(self.__points)-2
            else:
                i = i+1
        i = 0
        while (ctrl - i):
            if self.__points[i].getY() == self.__points[i+1].getY() and self.__points[i].getY() == self.__points[i+2].getY():
                del(self.__points[i+1])
                ctrl = len(self.__points)-2
            else:
                i = i+1

    def draw(self):
        return self
    def isInside(self):
        return False
    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        return False


# Each is[Component](): verifies the respective data type of a component. Returns True if its correct.
def isEntry(component) -> bool:
    return isinstance(component, Entry)


def isChecker(component) -> bool:
    return isinstance(component, Checker)


def isGate(component) -> bool:
    return isinstance(component, Gate)


def isWire(component) -> bool:
    return isinstance(component, Wire)

# isEqualPoints(): receives two pairs of Coords and returns True if they have the same x and y.
def isEqualPoints(c1: Coords, c2: Coords) -> bool:
    if c1.getX() == c2.getX() and c1.getY() == c2.getY():
        return True
    return False

# wiredComponent(): receives an Wire and other component then verifies if the component is connected
#                  to the Wire begin or end (True if positive). Entry can only be connected to the
#                  Wire start point.
def wiredComponent(w: Wire, component) -> bool:
    if isGate(component) and (isEqualPoints(w.getWireStartP(), component.getCoords()) or isEqualPoints(w.getWireEndP(), component.getCoords())):
        return True
    elif isEntry(component) and isEqualPoints(w.getWireStartP(), component.getCoords()):
        return True
    else:
        return False

# connectedComponents(): to be connected the components c1 and c2 must be wired one at start and
#                       other to end of the Wire component.
def connectedComponents(w: Wire, c1, c2) -> bool:
    return (wiredComponent(w, c1) and wiredComponent(w, c2) and
            not(isEqualPoints(c1.getCoords(), c2.getCoords())))

