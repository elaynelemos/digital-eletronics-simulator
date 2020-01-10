from components import Element, Coords
from util import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Window(Element):
    factor: float = 0.1

    def __init__(self):
        super().__init__()
        self.center = Coords(0, 0)
        self.size = Coords(0, 0)
        self.zoom = 1.0
        self.elements = []

    def setCenter(self, center: Coords):
        self.center = center
        return self

    def setSize(self, size: Coords):
        self.size = size
        return self

    def setZoom(self, zoom):
        if(isinstance(zoom, bool)):
            self.zoom = self.zoom * \
                (1+Window.__factor) if zoom else self.zoom / (1+Window.__factor)
        elif(isinstance(zoom, float)):
            self.zoom = float
        return self

    def getElement(self, index=None):
        if index == None:
            return self.elements
        elif (isinstance(zoom, int) and index >= 0 and index < len(self.elements)):
            return self.elements[index]

    def draw(self):
        for i in range(20):
            for j in range(20):
                self.center.sum(Coords(i*POINT_SPACE, j*POINT_SPACE)
                                ).draw(radius=0.5, color=Color(r=0.5, g=0.5, b=0.5))
        for i in range(20):
            for j in range(1, 20):
                self.center.sum(Coords(i*POINT_SPACE, -j*POINT_SPACE)
                                ).draw(radius=0.5, color=Color(r=0.5, g=0.5, b=0.5))
        for i in range(1, 20):
            for j in range(20):
                self.center.sum(Coords(-i*POINT_SPACE, j*POINT_SPACE)
                                ).draw(radius=0.5, color=Color(r=0.5, g=0.5, b=0.5))
        for i in range(1, 20):
            for j in range(1, 20):
                self.center.sum(Coords(-i*POINT_SPACE, -j*POINT_SPACE)
                                ).draw(radius=0.5, color=Color(r=0.5, g=0.5, b=0.5))
        self.center.draw(radius=1.0)

        for i in self.elements:
            i.draw()
        return self

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:

        for i in range(len(self.elements)):
            if self.elements[len(self.elements)-i-1].event(event_type, key=key, button=button, state=state, coords=coords):
                return True
        return False

    def isInside(self, coords) -> bool:
        return False
