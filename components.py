"""
*   Universidade Federal do Vale do São Francisco - Univasf
*   Colegiado de Engenharia de Computação
*   Orientador: Prof. Dr. Jorge Cavalcanti
*   Discentes: Elayne Lemos, elayne.l.lemos@gmail.com
*              Jônatas de Castro, jonatascastropassos@gmail.com
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

RELATIVE_GATEIN_X = 0
RELATIVE_GATEIN_Y = 0
RELATIVE_GATEOUT_X = 0
RELATIVE_GATEOUT_Y = 0

ORIENTATION_LR = 0
ORIENTATION_UD = 1
ORIENTATION_RL = 2
ORIENTATION_DU = 3
N_ENTRIES = 2

COLOR_TRUE = Color(r=192.0/255)
COLOR_FALSE = Color(b=192.0/255)

"""COMPONENT CLASSES > look at Coords, stopped there
"""

#Entry: Represents a logic entry. It has a value itself. 
#       Then cannot be connected to other entries (only outputs its own value).
class Entry(Element):
    #the attributes (private) only can be reached by getters and setters.
    __value:bool = None
    __coords:Coords = None
    __orientation = ORIENTATION_LR
    __size = 15.0

    #the constructor of Entry receives a logic value and the Coords where the entry should be placed.
    def __init__(self, coords:Coords = Coords(0.0,0.0)) -> None:
        super().__init__()
        self.setCoords(coords)

    def getValue(self) -> bool:
        return self.__value
    def getCoords(self) -> Coords:
            return self.__coords
    def getCoordX(self) -> float:
        return self.__coords.getX()   
    def getCoordY(self) -> float:
        return self.__coords.getY()

    def setValue(self, value:bool) -> bool: #returns True if succeeds.
        try:
            if not(isinstance(value,bool)):
                raise ValueError("ValueError: Logic value expected to entry. You entered a(n): ", type(value))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__value = value
            return True

    def toogleV(self) -> bool:
        try:
            if self.__value is not None:
                self.__value = xor(self.__value,True)
                return True
            else:
                raise AttributeError("Entry value not defined!")
        except AttributeError as ae:
            print(ae)
            return False

    def setCoords(self, coords:Coords) -> bool: #returns True if both coords are valid.
        self.__coords = coords
        if self.__coords.getX()<0 or self.__coords.getY()<0:
            return False
        else:
            return True
    
    def setRotation(self,sense=False):
        self.__orientation = self.__orientation+ (1 if sense else -1)
        self.__orientation = 0 if self.__orientation>3 else self.__orientation
        self.__orientation = 3 if self.__orientation<0 else self.__orientation

    def draw(self):
        c = Coords(0,0).copy(self.getCoords())

        # definindo a rotação do componente
        if self.__orientation%2==0: # LR or RL
            c = c.sum(Coords(-self.__size*2/3,0)) if int(self.__orientation/2)==0 else c.sum(Coords(self.__size*2/3,0))
        else:                       # UD or DU
            c = c.sum(Coords(0,-self.__size*2/3)) if int(self.__orientation/2)==0 else c.sum(Coords(0,self.__size*2/3))
            
        Color().apply()
        glBegin(GL_LINES)
        self.getCoords().apply()
        c.apply()
        glEnd()

        #Retangulo
        if self.__value:
            COLOR_TRUE.apply()
        else:
            COLOR_FALSE.apply()

        glBegin(GL_POLYGON)
        rect_around(c,1/3*self.__size)
        glEnd()

        #borda
        COLOR_STROKE.apply()
        glLineWidth(STROKE_WIDTH)
        glBegin(GL_LINES)
        rect_around(c,1/3*self.__size)
        glEnd()

        #number
        if self.__value:
            digit_around(c,1/3*self.__size,1)
        else:
            digit_around(c,1/3*self.__size,0)

        self.getCoords().draw()
        
        return self


#Gate: Represents the main logic gates (or, and, xor, nor, nand) those must receives a pair of 
#      logic values and are able to output its interpretation.
class Gate(Element):
    id: int     = 0
    #the attributes (private) only can be reached by getters and setters.
    __gatetype:int = None
    __entry:List[Entry] = []
    __coords:Coords = None
    __out:Coords = None

    #the constructor of Gate receives the gate type, two logic values and the Coords where it
    #should be placed.
    def __init__(self, gatetype:int, coords:Coords) -> None: 
        self.setGateType(gatetype) #gate types: 1=or, 2=and, 3=xor, 4=nor, 5=nand
        self.setCoords(coords) #position of the gate
        self.setName("G" + str(Gate.id))
    
    def getGateType(self) -> int:
        return self.__gatetype    
    def getIn(self,i:int) -> Entry:
        try:
            if self.__entry[i] is not None:
                return self.__entry[i]
            else:
                raise AttributeError("Entry not defined!")
        except AttributeError as ae:
            print(ae)
            return None 

    def getCoords(self) -> Coords:
            return self.__coords
    def getCoordX(self) -> int:
        return self.__coords.getX()   
    def getCoordY(self) -> int:
        return self.__coords.getY()

    def getOutCoords(self) -> Coords:
        return self.__out
    def getOutCoordX(self) -> int:
        return self.__out.getX()
    def getOutCoordY(self) -> int:
        return self.__out.getY()

    def setGateType(self, gatetype) -> bool: #returns True if succeeds.
        try:
            if not(isinstance(gatetype, int)) or isinstance(gatetype, bool): #Type validation.
                raise ValueError("ValueError: integer expected to gate classification. You entered a(n): ", type(gatetype))
            elif gatetype<1 or gatetype>5: #validation of gate classification.
                raise ValueError("ValueError: gate classification not defined! Expected between 1 and 5 including both. You entered", gatetype)
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__gatetype = gatetype
            return True
        
    def setIn(self, entry) -> bool: #returns True if succeeds.
        try:
            for i in entry:
                if i.getValue() is not None:
                    self.__entry.append(i)
                else:
                    raise ValueError("ValueError: Logic value expected to the gate entries. You entered a(n): ", type(i))
        except ValueError as ve:
            print(ve)
            self.__entry = []
            return False
        else:
            return True
        
    def setCoords(self, coords:Coords) -> bool: #returns True if both coords are valid.
        self.__coords = coords
        if self.__coords.getX()<0 or self.__coords.getY()<0:
            return False
        else:
            return True

    def gateOut(self) -> Entry:
        A = Entry(Coords(self.getCoordX()+self.getOutCoordX(), self.getCoordY()+self.getOutCoordY()))
        if self.getGateType()==1:
            A.setValue(self.getIn(0).getValue() or self.getIn(1).getValue())
        elif self.getGateType()==2:
            A.setValue(self.getIn(0).getValue() and self.getIn(1).getValue())
        elif self.getGateType()==3:
            A.setValue(self.getIn(0).getValue() != self.getIn(1).getValue())
        elif self.getGateType()==4:
            A.setValue(not(self.getIn(0).getValue() or self.getIn(1).getValue()))
        elif self.getGateType()==5:
            A.setValue(not(self.getIn(0).getValue() and self.getIn(1).getValue()))
        return A

    def draw(self):
        return self


#Wire: Represents the connector of the logic circuit. It's defined as a list of unique 
#      Coords. Once connected to an logic component carries its value from start to end points.
class Wire(Element):
    fill:Color  = Color(g=64.0/255)
    #the attributes (private) only can be reached by getters and setters.
    __points:List[Coords] = []

    #the constructor of Wire receives a list of Coords (points) to define itself.
    def __init__(self, points:List[Coords]) -> None:
        super().__init__()
        self.insertWireP(points)

    #TODO #fix insertion function 
    def insertWireP(self, points:List[Coords]) -> bool: #returns true if points is correctly inserted.
        ctrl = True
        try:
            for i in points:
                x = i.getX()
                y = i.getY()
                if x>=0 and y>=0:
                    for j in self.__points:
                        if j.getX()==x and j.getY()==y:
                            ctrl = False
                            break
                    if ctrl:
                        self.__points.append(i)
                    ctrl = True
            #self.refactorWire()
            if len(self.__points)<2: #validation of condition to be a wire (line).
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
        if l>0:
            return self.__points[l-1]
        else:
            return self.__points[0]
    def getWireNextP(self, reference:Coords) -> Coords:
        for i in self.__points:
            if i.getX()==reference.getX() and i.getY()==reference.getY():
                return self.__points[self.__points.index(i) + 1]
    
    #TODO fix refactor function
    def refactorWire(self) -> None: #reduce the number of points if they are at the same line.
        ctrl = len(self.__points)-2
        i = 0
        while (ctrl - i):
            if self.__points[i].getX()==self.__points[i+1].getX() and self.__points[i].getX()==self.__points[i+2].getX():
                del(self.__points[i+1])
                ctrl = len(self.__points)-2
            else:
                i = i+1
        i = 0
        while (ctrl - i):
            if self.__points[i].getY()==self.__points[i+1].getY() and self.__points[i].getY()==self.__points[i+2].getY():
                del(self.__points[i+1])
                ctrl = len(self.__points)-2
            else:
                i = i+1

    def draw(self):
        return self

"""FUNCTIONS
"""
#Each is[Component](): verifies the respective data type of a component. Returns True if its correct.
def isEntry(component) -> bool:
    return isinstance(component, Entry)
def isGate(component) -> bool:
    return isinstance(component, Gate)
def isWire(component) -> bool:
    return isinstance(component, Wire)

#isEqualPoints(): receives two pairs of Coords and returns True if they have the same x and y.
def isEqualPoints(c1:Coords, c2:Coords) -> bool:
    if c1.getX()==c2.getX() and c1.getY()==c2.getY():
        return True
    return False

#wiredComponent(): receives an Wire and other component then verifies if the component is connected
#                  to the Wire begin or end (True if positive). Entry can only be connected to the
#                  Wire start point.
def wiredComponent(w:Wire, component) -> bool:
    if isGate(component) and (isEqualPoints(w.getWireStartP(), component.getCoords()) or isEqualPoints(w.getWireEndP(), component.getCoords())):
        return True
    elif  isEntry(component) and isEqualPoints(w.getWireStartP(), component.getCoords()):
        return True
    else:
        return False

#connectedComponents(): to be connected the components c1 and c2 must be wired one at start and
#                       other to end of the Wire component.
def connectedComponents(w:Wire, c1, c2) -> bool:
    return (wiredComponent(w, c1) and wiredComponent(w, c2) and
    not(isEqualPoints(c1.getCoords(), c2.getCoords())))

"""
e = Wire([Coords(10,20),Coords(10,20),Coords(10,40),Coords(10,30)])
print(len(e.getWireP()))

e.refactorWire()
print(len(e.getWireP()))

print(e.getWireEndP().getY())

e.insertWireP([Coords(50,70)])

print(e.getWireEndP().getY())
"""

"""
    #basic test ahead
    e1 = Entry(False, Coords(10,20))
    e2 = Entry(False, Coords(10,30))
    w = Wire((Coords(10,20),Coords(50,20),Coords(10,20),Coords(90,40)))
    g = Gate(1, e1.getValue(), e2.getValue(), Coords(20,40))

    print(connectedComponents(w,e1,g))
"""

"""    def refactorWire(self) -> None: #reduce the number of points if they are at the same line.
        l = len(self.__coords)-3
        print(l)
        for i in range(l):
            if self.__coords[i].getX()==self.__coords[i+1].getX() and self.__coords[i].getX()==self.__coords[i+2].getX():
                self.__coords.pop(i+1)
                print(len(self.__coords))
        for i in range(l):
            if self.__coords[i].getY()==self.__coords[i+1].getY() and self.__coords[i].getY()==self.__coords[i+2].getY():
                self.__coords.pop(i+1)
                
"""