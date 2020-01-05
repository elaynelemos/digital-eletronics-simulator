from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import traceback

from abc import ABC, abstractmethod

import math

class Color:
    __r: float = 0.0
    __g: float = 0.0
    __b: float = 0.0
    def __init__(self,r=0.0,g=0.0,b=0.0,color=None):
        if(color != None):
            self.copy(color)
        self.setR(r).setG(g).setB(b)
    def getR(self):
        return self.__r
    def getG(self):
        return self.__g
    def getB(self):
        return self.__b
    def setR(self,r:float):
        try:
            if not isinstance(r, float): #Type validation.
                raise ValueError("ValueError: float expected to red color. You entered a(n): ", type(r))
        except ValueError as ve:
            print(ve)
            return self
        else:
            self.__r = r
            return self
    def setG(self,g:float):
        try:
            if not isinstance(g, float): #Type validation.
                raise ValueError("ValueError: float expected to green color. You entered a(n): ", type(g))
        except ValueError as ve:
            print(ve)
            return self
        else:
            self.__g = g
            return self
    def setB(self,b:float):
        try:
            if not isinstance(b, float): #Type validation.
                raise ValueError("ValueError: float expected to blue color. You entered a(n): ", type(b))
        except ValueError as ve:
            print(ve)
            return self
        else:
            self.__b = b
            return self
    def copy(self,color):
        self.setR(color.getR()).setG(color.getG()).setB(color.getB())
        return self
    def apply(self):
        glColor3f(self.__r,self.__g,self.__b)
        return self
    def applyClear(self):
        glClearColor(self.__r,self.__g,self.__b,1.0)
        return self
    def __str__(self):
        return "COLOR[r="+str(self.getR())+" g="+str(self.getG())+"b="+str(self.getB())+"]"

COLOR_STROKE = Color()#black
STROKE_WIDTH = 3.0

#Element: It's a abstract Class to define some Methods to next classes
class Element(ABC):
    
    id:int = 0
    
    __name: str =""

    def __init__(self):
        self.__name = "E"+ str(Element.id)
        Element.id += 1

    def getName(self):
        return self.__name

    def setName(self,name:str):
        try:
            if not isinstance(name, str): #Type validation.
                raise ValueError("ValueError: string expected to name. You entered a(n): ", type(name))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__name = name
            return True

    @abstractmethod
    def draw(self):

        return self
    def __str__(self):
        return "Name="+self.getName()


#Coords: It's the "data type" of a point on the screen.
class Coords(Element):
    #the attributes (private) only can be reached by getters and setters. Initiate coords with
    #invalid number for screen to be treated if there's any error in insertion.
    radius: float = 2.0
    fill:   Color = Color(r=1.0,g=1.0,b=1.0)
    stroke: Color = Color() # black
    n_sides: int  = 15
    __x: float = None
    __y: float = None
    
    #the constructor of Coords receives a coordinate pair.
    def __init__(self, x:float, y:float) -> None:
        super().__init__()
        self.setX(x)
        self.setY(y)

    def getX(self) -> float:
        return self.__x 
    def getY(self) -> float:
        return self.__y
    
    def setX(self, x:float) -> bool: #returns True if succeeds.
        #try:
            if math.isnan(x): #Type validation.
                raise ValueError("ValueError: float expected to X coordinate. You entered a(n): ", type(x))
        #except ValueError as ve:
            #traceback.print_exc()
         #   print(ve)
            
          #  return False
        #else:
            self.__x = x/1.0
            return True

    def setY(self, y:float) -> bool: #returns True if succeeds.
        try:
            if math.isnan(y): #Type validation.
                raise ValueError("ValueError: float expected to Y coordinate. You entered a(n): ", type(y))
        except ValueError as ve:
            print(ve)
            return False
        else:
            self.__y = y/1.0
            return True
    def copy(self,coords):
        self.setX(coords.getX())
        self.setY(coords.getY())
        return self
    
    def sum(self,coords):
        return Coords(self.getX()+coords.getX(),self.getY()+coords.getY())
    def mul(self,value):
        return Coords(self.getX()*value,self.getY()*value)
    
    def apply(self):
        glVertex3f(self.getX(), self.getY(), 0.0)
        return self
    
    def draw(self):
        Coords.fill.apply()
        glBegin(GL_POLYGON)
        for i in range(Coords.n_sides):
            glVertex3f(self.getX()+Coords.radius*math.sin(i*math.pi*2/Coords.n_sides), 
            self.getY()+Coords.radius*math.cos(i*math.pi*2/Coords.n_sides), 0)
        glEnd()

        COLOR_STROKE.apply()
        glLineWidth(STROKE_WIDTH)
        glBegin(GL_LINES)
        for i in range(Coords.n_sides):
            glVertex3f(self.getX()+Coords.radius*math.sin(i*math.pi*2/Coords.n_sides), 
            self.getY()+Coords.radius*math.cos(i*math.pi*2/Coords.n_sides), 0)
        glEnd()
        return self
    def __str__ (self):
        return "COORDS[x: "+str(self.getX())+" y:"+str(self.getY())+"]"

def rect_around(c:Coords,a:float,b:float=None):
    b = a if b==None else b
    c.sum(Coords(-a,-b)).apply()
    c.sum(Coords(-a,+b)).apply()
    c.sum(Coords(+a,+b)).apply()
    c.sum(Coords(+a,-b)).apply()
    return None

def digit_around(c:Coords,a:float,d:int,p:bool=False):
    b = a/2
    a = a*4/5
    w = a/8
    # 7 segments display based
    # segment a
    if d in [0,2,3,5,6,7,8,9]:
        glBegin(GL_POLYGON)
        rect_around(c.sum(Coords(0,-a)),b,w)
        glEnd()
    # segment b
    if d in [0,1,2,3,4,7,8,9]:
        glBegin(GL_POLYGON)
        rect_around(c.sum(Coords(b,-a/2)),w,a/2)
        glEnd()
    # segment c
    if d in [0,1,3,4,5,6,7,8,9]:
        glBegin(GL_POLYGON)
        rect_around(c.sum(Coords(b,+a/2)),w,a/2)
        glEnd()
    # segment d
    if d in [0,2,3,5,6,8,9]:
        glBegin(GL_POLYGON)
        rect_around(c.sum(Coords(0,+a)),b,w)
        glEnd()
    # segment e
    if d in [0,2,6,8]:
        glBegin(GL_POLYGON)
        rect_around(c.sum(Coords(-b,+a/2)),w,a/2)
        glEnd()
    # segment f
    if d in [0,4,5,6,8,9]:
        glBegin(GL_POLYGON)
        rect_around(c.sum(Coords(-b,-a/2)),w,a/2)
        glEnd()
    # segment g
    if d in [2,3,4,5,6,8,9]:
        glBegin(GL_POLYGON)
        rect_around(c,b,w)
        glEnd()
    # segment .
    if p:
        glBegin(GL_POLYGON)
        rect_around(c.sum(Coords(b+4*w,+a)),w,w)
        glEnd()
    return None