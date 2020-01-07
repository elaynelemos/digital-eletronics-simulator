from components import Element, Coords

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Window(Element):
    factor:float = 0.1

    def __init__(self):
        super().__init__()
        self.center     = Coords(0,0)
        self.size       = Coords(0,0)
        self.zoom       = 1.0
        self.elements   = []
    def setCenter(self,center:Coords): 
        self.center = center
        return self

    def setSize(self,size:Coords):
        self.size = size
        return self
    def setZoom(self, zoom):
        if(isinstance(zoom, bool)):
            self.zoom = self.zoom * (1+Window.__factor) if zoom else self.zoom / (1+Window.__factor)
        elif(isinstance(zoom, float)):
            self.zoom = float
        return self

    def getElement(self,index=None):
        if index == None:
            return self.elements
        elif (isinstance(zoom, int) and index>=0 and index< len(self.elements)):
            return self.elements[index]
        

    def draw(self):
        for i in self.elements:
            i.draw()
        return self