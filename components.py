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
import sys

#classes
class Coords:
    __x: int = 0
    __y: int = 0
    def __init__(self, x:int, y:int) -> None:
        try:     
            i = int(x)
            if float(i) != float(x):
                raise ValueError("X coordinate is not an integer.")
            
            i = int(y)
            if float(i) != float(y):
                raise ValueError("Y coordinate is not an integer.")
        except ValueError as ve:
            print(ve)
        self.setX(x)
        self.setY(y)

    def getX(self) -> int:
        return self.__x 
    def getY(self) -> int:
        return self.__y
    
    def setX(self, x) -> None:
        self.__x = x
    def setY(self, y) -> None:
        self.__y = y    


class Entry:
    __value:bool = False
    __coords:Coords

    def __init__(self, value:bool, coords:Coords) -> None:
        self.setValue(value)
        self.setCoords(coords)

    def getValue(self) -> bool:
        return self.__value
    def getCoords(self) -> Coords:
            return self.__coords
    def getCoordX(self) -> int:
        return self.__coords.getX()   
    def getCoordY(self) -> int:
        return self.__coords.getY()

    def setValue(self, value:bool) -> None:
        try:
            self.__value = value
            if not(isinstance(value,bool)):
                raise ValueError("Logic value expected. You entered an: ", type(value))
        except ValueError as ve:
            print(ve)    
    def setCoords(self, coords:Coords):
        self.__coords = coords


class Gate:
    __coords:Coords
    def __init__(self, gatetype:int, in1:bool, in2:bool, coords:Coords) -> None:
        try:
            i = int(gatetype)
            if float(i) != float(gatetype):
                raise ValueError("Wrong type for gate classification! Integer expected.")
            elif i>5 or i<1:
                raise ValueError("Wrong range for gate classification! Expected between 1 and 5 including both.")  

            if in1!=True and in1!=False:
                raise ValueError("The first entry is not a boolean.")

            if in2!=True and in2!=False:
                raise ValueError("The second entry is not a boolean.")
        except ValueError as ve:
            print(ve)
            return
        
        #gate types: 1=or, 2=and, 3=xor, 4=nor, 5=nand
        self.setGateType(gatetype)
        self.setIn1(in1) #first entry
        self.setIn2(in2) #second entry
        self.setCoords(coords) #position of the gate
    
    def getGateType(self):
        return self.__gatetype    
    def getIn1(self):
        return self.__in1    
    def getIn2(self):
        return self.__in2
    def getCoords(self):
            return self.__coords
    def getCoordX(self):
        return self.__coords.getX()   
    def getCoordY(self):
        return self.__coords.getY()

    def setGateType(self, gatetype):
        self.__gatetype = int(gatetype)
    def setIn1(self, in1):
        self.__in1 = bool(in1)
    def setIn2(self, in2):
        self.__in2 = bool(in2)
    def setCoords(self, coords:Coords):
        self.__coords = coords

    def gateOutput(self) -> bool:
        if self.getGateType()==1:
            return(self.getIn1() or self.getIn2())
        elif self.getGateType()==2:
            return(self.getIn1() and self.getIn2())
        elif self.getGateType()==3:
            return(self.getIn1() != self.getIn2())
        elif self.getGateType()==4:
            return(not(self.getIn1() or self.getIn2()))
        elif self.getGateType()==5:
            return(not(self.getIn1() and self.getIn2()))


class Wire:
    __coords:List[Coords] = []
    def __init__(self, points:List[Coords]) -> None:
        try:
            if len(points) < 2:
                raise AttributeError("Not enough points to a wire!")
            self.insertWireP(points)
        except AttributeError as ae:
            print(ae)
    
    def insertWireP(self, points:List[Coords]) -> bool:
        ctrl = True
        try:
            for i in points:
                for j in self.__coords:
                    if j.getX()==i.getX() and j.getY()==i.getY():
                        ctrl = False
                        break
                if ctrl:
                    self.__coords.append(i)
                ctrl = True
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            return False
        else:
            return True

    def getWireP(self) -> List[Coords]:
        return self.__coords

    def getWireStartP(self) -> Coords:
        return self.__coords[0]
    def getWireEndP(self) -> Coords:
        return self.__coords[len(self.__coords)-1]
    def getWireNextP(self, reference:Coords) -> Coords:
        for i in self.__coords:
            if i.getX()==reference.getX() and i.getY()==reference.getY():
                return self.__coords[self.__coords.index(i) + 1]


#functions
def isEntry(component) -> bool:
    return isinstance(component, Entry)
def isGate(component) -> bool:
    return isinstance(component, Gate)
def isWire(component) -> bool:
    return isinstance(component, Wire)

def isEqualPoints(c1:Coords, c2:Coords) -> bool:
    if c1.getX()==c2.getX() and c1.getY()==c2.getY():
        return True
    return False

def wiredComponent(w:Wire, component) -> bool:
    if isGate(component) and (isEqualPoints(w.getWireStartP(), component.getCoords()) or isEqualPoints(w.getWireEndP(), component.getCoords())):
        return True
    elif  isEntry(component) and isEqualPoints(w.getWireStartP(), component.getCoords()):
        return True
    else:
        return False

def connectedComponents(w:Wire, c1, c2) -> bool:
    return (wiredComponent(w, c1) and wiredComponent(w, c2) and not(isEqualPoints(c1.getCoords(), c2.getCoords())))




"""
#basic test ahead
e1 = Entry(False, Coords(10,20))
e2 = Entry(False, Coords(10,30))
w = Wire((Coords(10,20),Coords(50,20),Coords(10,20),Coords(90,40)))
g = Gate(1, e1.getValue(), e2.getValue(), Coords(20,40))

print(connectedComponents(w,e1,g))
"""
