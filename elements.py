from components import Element, Coords
from components import Entry, Checker, Display, NotGate, AndGate, NandGate, OrGate, NorGate, XorGate, XnorGate, KeyBoard
from util import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

componentClasses = [Entry, Checker, Display, NotGate, AndGate,
                    NandGate, OrGate, NorGate, XorGate, XnorGate, KeyBoard]


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


# Painel contends the logics ports and others components like checker and entry.
class PainelComponents(Element):
    # coordinate of glut windows, value required to built the painelComponents.
    __coords: Coords = None

    def __init__(self, coords):
        super().__init__()
        self.setCoords(coords)
        self.totalCells = 11  # Number of components.
        # Each component where in a cell. This attribute determine the size of it.
        self.sizeCell = 10
        self.initPainelComponents = (35 - self.__coords.getY())

    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        self.initPainelComponents = (35 - self.__coords.getY())

        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def drawLines(self):
        span = self.initPainelComponents

        for i in range(self.totalCells):

            glLineWidth(0.1)
            Color(155/255, 198/255, 225/255).apply()

            span = span + self.sizeCell

            glBegin(GL_LINES)
            Coords(5-self.__coords.getX(), span).apply()
            Coords(23-self.__coords.getX(), span).apply()
            glEnd()

            componentClasses[i](coords=Coords(
                14-self.__coords.getX(), span-self.sizeCell/2), size=self.sizeCell*0.8).draw()

        glLineWidth(3)

    def draw(self):

        glBegin(GL_POLYGON)
        Color(169/255, 207/255, 233/255).apply()
        Coords((4-self.__coords.getX()), 35 - self.__coords.getY()).apply()
        Coords(4-self.__coords.getX(), self.__coords.getY()).apply()
        Color(194/255, 233/255, 240/255).apply()
        Coords(24-self.__coords.getX(), self.__coords.getY()).apply()
        Coords(24-self.__coords.getX(), 35-self.__coords.getY()).apply()
        glEnd()

        glLineWidth(0.1)
        glBegin(GL_LINE_LOOP)

        Color(32/255, 78/255, 98/255).apply()
        Coords((4-self.__coords.getX()), 35 - self.__coords.getY()).apply()
        Coords(4-self.__coords.getX(), self.__coords.getY()).apply()
        Coords(24-self.__coords.getX(), self.__coords.getY()).apply()
        Coords(24-self.__coords.getX(), 35-self.__coords.getY()).apply()
        glEnd()
        glLineWidth(3)

        self.drawLines()

    def isInside(self, x: int, y: int):
        if(((4-self.__coords.getX()) < x and x < (24-self.__coords.getX())) and ((35 - self.__coords.getY()) < y and y < self.__coords.getY())):
            return True
        else:
            return False
    # Find the component choosed
    def componentChoosed(self, y: int):

        span = self.sizeCell
        for indexCell in range(self.totalCells):
            if y < (span + self.initPainelComponents):
                return indexCell
            span = span + self.sizeCell

    # Return the component choosed
    def component(self, coord: Coords):

        if self.isInside(coord.getX(), coord.getY()) == True:
            component = self.componentChoosed(coord.getY())
            if component == ENTRY:
                return Entry()
            elif component == CHECKER:
                return Checker()
            elif component == DISPLAY:
                return Display()
            elif component == NOTGATE:
                return NotGate()
            elif component == ANDGATE:
                return AndGate()
            elif component == NANDGATE:
                return NandGate()
            elif component == ORGATE:
                return OrGate()
            elif component == NORGATE:
                return NorGate()
            elif component == XORGATE:
                return XorGate()
            elif component == XNORGATE:
                return XnorGate()
            elif component == KEYBOARD:
                return KeyBoard()
            else:
                return None

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        if event_type == GLUT_UP and coords is not None:
            return None

# The Panel contains the workspace. Here can assemble the components and simulate them.


class Panel(Element):

    # Coordinate of glut windows, value required to built the painel.
    __coords: Coords = None
    __window: Window = None  # All components will be stored here.

    def __init__(self, coords):
        super().__init__()
        self.setCoords(coords)
        self.setWindow(Window())
        self.shift = 15

    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords

    def addComponentWindow(self, component):
        if self.__window is not None:
            self.__window.elements.append(component)

    def setWindow(self, window: Window):
        self.__window = window

    def getWindow(self):
        return self.__window

    def draw(self):

        Color(.9, 0.8, .6).apply()
        glBegin(GL_POLYGON)
        glVertex2f((27-self.__coords.getX()),
                   self.shift + 23 - self.__coords.getY())
        glVertex2f(27-self.__coords.getX(), self.shift + self.__coords.getY())
        glVertex2f(self.__coords.getX()-3, self.shift + self.__coords.getY())
        glVertex2f(self.__coords.getX()-3,
                   self.shift + 23-self.__coords.getY())
        glEnd()

        Color(131/255, 99/255, 33/255).apply()
        glLineWidth(0.1)
        glBegin(GL_LINE_LOOP)
        glVertex2f((27-self.__coords.getX()),
                   self.shift + 23 - self.__coords.getY())
        glVertex2f(27-self.__coords.getX(), self.shift + self.__coords.getY())
        glVertex2f(self.__coords.getX()-3, self.shift + self.__coords.getY())
        glVertex2f(self.__coords.getX()-3,
                   self.shift + 23-self.__coords.getY())
        glEnd()
        glLineWidth(3)

        # draw panel contents
        if self.__window is not None:
            self.__window.draw()

    def isInside(self, x: int, y: int) -> bool:
        if (((27-self.__coords.getX()) < x and x < (self.__coords.getX()-3)) and ((self.shift + 23 - self.__coords.getY()) > y > (self.shift + 23-self.__coords.getY()))):
            return True
        else:
            return False

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        return None
        # if event_type == GLUT_UP and coords is not None:
        #   return None


class IconZoomMore(Element):
    __coords: Coords = None

    def __init__(self, coord: Coords(0, 0)):
        super().__init__()
        self.setCoords(coord)

    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def draw(self):
        Color(176/255, 193/255, 203/255).apply()

        glBegin(GL_QUADS)
        Coords((2-self.__coords.getX()), 1-self.__coords.getY()).apply()
        Coords((3-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        Coords((5-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), -1-self.__coords.getY()).apply()
        glEnd()

        glBegin(GL_POLYGON)
        Coords((-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 2-self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((0-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        glEnd()
        Color(0.0, 0.0, 0.0).apply()

        glBegin(GL_LINES)
        Coords((-1-self.__coords.getX()), 3-self.__coords.getY()).apply()
        Coords((3-self.__coords.getX()), 3-self.__coords.getY()).apply()
        glEnd()

        glBegin(GL_LINES)
        Coords((1-self.__coords.getX()), 1-self.__coords.getY()).apply()
        Coords((1-self.__coords.getX()), 5-self.__coords.getY()).apply()
        glEnd()

        glBegin(GL_POLYGON)
        Coords((2-self.__coords.getX()), 1-self.__coords.getY()).apply()
        Coords((3-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        Coords((5-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), -1-self.__coords.getY()).apply()
        glEnd()

        glLineWidth(0.1)
        glBegin(GL_LINE_LOOP)
        Coords((-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 2-self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((0-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        glEnd()

        glLineWidth(3)

    def isInside(self, x: int, y: int):
        if (((-2-self.__coords.getX()) < x and x < (4-self.__coords.getX())) and ((0 - self.__coords.getY()) < y and y < (6-self.__coords.getY()))):
            return True
        else:
            return False

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        return False


class IconZoom(Element):
    __coords: Coords = None

    def __init__(self, coord: Coords(0, 0)):
        super().__init__()
        self.setCoords(coord)

    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def getCoords(self) -> Coords:
        return self.__coords

    def draw(self):
        Color(176/255, 193/255, 203/255).apply()

        glBegin(GL_QUADS)
        Coords((2-self.__coords.getX()), 1-self.__coords.getY()).apply()
        Coords((3-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        Coords((5-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), -1-self.__coords.getY()).apply()
        glEnd()

        glBegin(GL_POLYGON)
        Coords((-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 2-self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((0-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        glEnd()
        Color(0.0, 0.0, 0.0).apply()

        glBegin(GL_POLYGON)
        Coords((2-self.__coords.getX()), 1-self.__coords.getY()).apply()
        Coords((3-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        Coords((5-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), -1-self.__coords.getY()).apply()
        glEnd()

        glLineWidth(0.1)
        glBegin(GL_LINE_LOOP)
        Coords((-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), -self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 2-self.__coords.getY()).apply()
        Coords((4-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((2-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((0-self.__coords.getX()), 6 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 4 - self.__coords.getY()).apply()
        Coords((-2-self.__coords.getX()), 2 - self.__coords.getY()).apply()
        glEnd()

        glLineWidth(3)

    def isInside(self, x: int, y: int):
        if (((-2-self.__coords.getX()) < x and x < (4-self.__coords.getX())) and ((0 - self.__coords.getY()) < y and y < (6-self.__coords.getY()))):
            return True
        else:
            return False

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        return False


class Icon(Element):
    __coords: Coords = None

    def __init__(self, coord: Coords(0, 0)):
        super().__init__()
        self.setCoords(coord)

    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def getCoords(self) -> Coords:
        return self.__coords

    def draw(self):
        return None

    def isInside(self, x: int, y: int):
        if (((-2-self.__coords.getX()) < x and x < (4-self.__coords.getX())) and ((0 - self.__coords.getY()) < y and y < (6-self.__coords.getY()))):
            return True
        else:
            return False

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        return False


class IconStart(Icon):
    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def draw(self):
        Color(238/255, 28/255, 36/255).apply()
        glBegin(GL_TRIANGLES)
        Coords((-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        glEnd()

        glLineWidth(0.3)
        Color(0.0, 0.0, 0.0).apply()
        glBegin(GL_LINE_LOOP)
        Coords((-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        glEnd()
        glLineWidth(3.0)

    def isInside(self, x: int, y: int) -> bool:
        return super().isInside(x, y)


class IconStop(Icon):

    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def draw(self):
        Color(63/255, 72/255, 204/255).apply()
        glBegin(GL_QUADS)
        Coords((-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()), 0 -
               super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        glEnd()

        glLineWidth(0.3)
        Color(0.0, 0.0, 0.0).apply()
        glBegin(GL_LINE_LOOP)
        Coords((-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()), 0 -
               super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        glEnd()
        glLineWidth(3.0)

    def isInside(self, x: int, y: int) -> bool:
        return super().isInside(x, y)


class IconPrevious(Icon):

    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def draw(self):
        Color(140/255, 216/255, 27/255).apply()
        glBegin(GL_POLYGON)
        Coords((-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((7-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((7-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        glEnd()

        glLineWidth(0.3)
        Color(0.0, 0.0, 0.0).apply()
        glBegin(GL_LINE_LOOP)
        Coords((-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((7-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((7-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        glEnd()
        glLineWidth(3.0)

    def isInside(self, x: int, y: int) -> bool:
        return super().isInside(x, y)


class IconMoreAba(Icon):

    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def draw(self):
        Color(1.0, 1.0, 1.0).apply()
        glBegin(GL_POLYGON)
        Coords((-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((6-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((6-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 0 -
               super().getCoords().getY()).apply()
        glEnd()

        Color(0.0, 0.0, 0.0).apply()
        glLineWidth(0.3)
        glBegin(GL_LINE_LOOP)
        Coords((-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((6-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((6-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 0 -
               super().getCoords().getY()).apply()
        glEnd()

        glBegin(GL_LINE_LOOP)
        Coords((4-super().getCoords().getX()), 0 -
               super().getCoords().getY()).apply()
        Coords((4-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((6-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        glEnd()
        glLineWidth(3)

        Color(156/255, 201/255, 22/255).apply()
        glBegin(GL_LINES)
        Coords((3-super().getCoords().getX()), 1 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 5 -
               super().getCoords().getY()).apply()
        glEnd()

        glBegin(GL_LINES)
        Coords((1-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        glEnd()

    def isInside(self, x: int, y: int) -> bool:
        return super().isInside(x, y)


class IconNext(Icon):
    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def draw(self):
        Color(140/255, 216/255, 27/255).apply()
        glBegin(GL_POLYGON)
        Coords((-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((7-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        glEnd()

        glLineWidth(0.3)
        Color(0.0, 0.0, 0.0).apply()
        glBegin(GL_LINE_LOOP)
        Coords((-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 2 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), -
               super().getCoords().getY()).apply()
        Coords((7-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 6 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()), 4 -
               super().getCoords().getY()).apply()
        glEnd()
        glLineWidth(3.0)

    def isInside(self, x: int, y: int) -> bool:
        return super().isInside(x, y)


class IconZoomLess(IconZoom):
    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def drawDetail(self):
        glBegin(GL_LINES)
        Coords((-1 - super().getCoords().getX()),
               3 - super().getCoords().getY()).apply()
        Coords((3 - super().getCoords().getX()),
               3-super().getCoords().getY()).apply()
        glEnd()

    def isInside(self, x: int, y: int) -> bool:
        return super().isInside(x, y)

    def draw(self):
        super().draw()
        self.drawDetail()


class IconZoomMore(IconZoom):
    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def drawDetail(self):
        Color(0.0, 0.0, 0.0).apply()
        glBegin(GL_LINES)
        Coords((-1-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()), 3 -
               super().getCoords().getY()).apply()
        glEnd()

        glBegin(GL_LINES)
        Coords((1-super().getCoords().getX()), 1 -
               super().getCoords().getY()).apply()
        Coords((1-super().getCoords().getX()), 5 -
               super().getCoords().getY()).apply()
        glEnd()

    def isInside(self, x: int, y: int) -> bool:
        return super().isInside(x, y)

    def draw(self):

        super().draw()
        self.drawDetail()


# WindowsBar, one aba windows. Each windows bars have one panel and one panelComponents. Each
# windowsBar can simulate independently
class WindowsBar(Element):

    __coords: Coords = None
    __windowSize: Coords = None
    __focus: bool = None
    __windowBarNumber: int = 0
    __distanceAba: int = 0
    __painelComponents: PainelComponents = None
    __panel: Panel = None

    def __init__(self,  windowBarNumber: int, window: Window = None, focus: bool = True, coords: Coords = Coords(0.0, 0.0)):
        super().__init__()
        self.setCoords(coords)
        self.setSizeWindow(coords)
        self.setWindowBarNumber(windowBarNumber)
        self.setDistanceAba(windowBarNumber*52)
        self.setFocus(focus)
        self.focus = self.__focus
        self.shift = 15
        self.__painelComponents = PainelComponents(Coords(100, 100))
        self.__panel = Panel(Coords(100, 100))

    def setWindowBarNumber(self, windowBarNumber: int):
        self.__windowBarNumber = windowBarNumber

    def getWindowBarNumber(self) -> int:
        return self.__windowBarNumber

    def setPanel(self, coord: Coords(0, 0)):
        self.__panel = panel

    def getPanel(self):
        return self.__panel

    def addComponentWindow(self,  coords: Coords):
        component = self.__painelComponents.component(coords)
        if component is not None:
            self.__panel.addComponentWindow(component)

    def updateWindowBarNumber(self, windowBarNumber: int):
        self.__windowBarNumber = windowBarNumber
        self.__distanceAba = windowBarNumber*52

    def setDistanceAba(self, distance: int):
        self.__distanceAba = distance

    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__coords.getX() < 0 or self.__coords.getY() < 0:
            return False
        else:
            return True

    def setSizeWindow(self, coords: Coords(0.0, 0.0)):
        self.__windowSize = coords
        self.__painelComponents = PainelComponents(coords)
        if self.__panel is not None:
            self.__panel.setCoords(coords)

    def setFocus(self, focus: bool):
        self.__focus = focus

    def getFocus(self) -> bool:
        return self.__focus

    def isInside(self):
        pass

    def drawLines(self):
        glColor3f(169/255, 207/255, 233/255)
        glBegin(GL_POLYGON)
        Coords((24-self.__windowSize.getX()), self.shift +
               20 - self.__windowSize.getY()).apply()
        Coords(24-self.__windowSize.getX(), self.shift +
               self.__windowSize.getY()).apply()
        Coords(self.__windowSize.getX(), self.shift +
               self.__windowSize.getY()).apply()
        Coords(self.__windowSize.getX(), self.shift +
               20-self.__windowSize.getY()).apply()
        glEnd()

    def close(self, x: int, y: int) -> bool:
        if (((68-self.__windowSize.getX() + self.__distanceAba) < x and x < (72-self.__windowSize.getX() + self.__distanceAba)) and ((self.shift + 12 - self.__windowSize.getY()) < y and y < (self.shift + 16-self.__windowSize.getY()))):
            return True
        else:
            return False

    def wereClickBar(self, x: int, y: int) -> bool:

        if (((32-self.__windowSize.getX() + self.__distanceAba) < x and x < (76-self.__windowSize.getX() + self.__distanceAba)) and ((self.shift + 8 - self.__windowSize.getY()) < y and y < (self.shift + 20-self.__windowSize.getY()))):
            self.setFocus(True)
            return True
        else:
            return False

    def onlyOneFocus(self, workSet):
        for i in workSet:
            if i.getFocus() == True:
                i.setFocus(False)
        workSet[len(workSet)-1].setFocus(True)

    def bar(self):

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glTranslatef(self.__distanceAba, 0.0, 0.0)
        glBegin(GL_POLYGON)
        Color(184/255, 216/255, 237/255).apply() if self.__focus == True else Color(218 /
                                                                                    255, 218/255, 218/255).apply()

        Coords(32-self.__windowSize.getX(), self.shift +
               8 - self.__windowSize.getY()).apply()
        Coords(76-self.__windowSize.getX(), self.shift +
               8-self.__windowSize.getY()).apply()
        Color(169/255, 207/255, 233/255).apply() if self.__focus == True else Color(205 /
                                                                                    255, 205/255, 205/255).apply()
        Coords(76-self.__windowSize.getX(), self.shift +
               20-self.__windowSize.getY()).apply()
        Coords((24-self.__windowSize.getX()), self.shift +
               20 - self.__windowSize.getY()).apply()
        Coords(24-self.__windowSize.getX(), self.shift +
               16-self.__windowSize.getY()).apply()
        glEnd()

        Color(0.0, 0.0, 0.0).apply()
        glBegin(GL_LINES)
        Coords((68-self.__windowSize.getX()), self.shift +
               16 - self.__windowSize.getY()).apply()
        Coords(72-self.__windowSize.getX(), self.shift +
               12-self.__windowSize.getY()).apply()
        glEnd()

        glBegin(GL_LINES)
        Coords((68-self.__windowSize.getX()), self.shift +
               12 - self.__windowSize.getY()).apply()
        Coords(72-self.__windowSize.getX(), self.shift +
               16-self.__windowSize.getY()).apply()
        glEnd()

        glPopMatrix()

    def draw(self):

        if self.__focus == True:
            self.bar()
            self.drawLines()
            self.__painelComponents.draw()
            if self.__panel is not None:
                self.__panel.draw()

        else:
            self.bar()

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        if self.__panel is not None:
            self.__panel.event(event_type, key=None,
                               button=None, state=None, coords=None)


ENTRY = 0
CHECKER = 1
DISPLAY = 2
NOTGATE = 3
ANDGATE = 4
NANDGATE = 5
ORGATE = 6
NORGATE = 7
XORGATE = 8
XNORGATE = 9
KEYBOARD = 10


# Windows Global. Windows that includes all others windows. One windowGlobal have various windowsBar
class WindowGlobal(Element):
    __width: int = None  # Width of the glut windows
    __height: int = None  # height of the glut windows
    __abaId: int = 0
    __windowFocus: int = -1
    __whatAbaIsFocus: int = -1  # Current windos bar is focus

    def __init__(self, sizeWindowGlobal=Coords(100, 100)):
        super().__init__()
        self.setSizeWindowGlobal(sizeWindowGlobal)
        self.workSet = []  # list of windowsBar
        self.tools = []  # list of Tools, like button start and stop simulation and zoom
        self.__abaId = 0
    # Alls components like windowsBars, painelComponents are draws based on size the glut window

    def setSizeWindowGlobal(self, sizeWindowGlobal: Coords):
        self.__width = sizeWindowGlobal.getX()
        self.__height = sizeWindowGlobal.getY()

    def drawTools(self):
        if self.tools != None:
            for i in self.tools:
                i.draw()

    def drawAbas(self):
        for i in self.workSet:
            i.draw()

    def draw(self):
        self.drawAbas()
        self.drawPainelOfTools()
        self.drawTools()
        return self

    # Draw bars of Tools
    def drawPainelOfTools(self):
        spanInElements = 15
        widthPainel = spanInElements*len(self.tools) + spanInElements
        heightPainel = 5
        glBegin(GL_QUADS)
        Color(169/255, 207/255, 233/255).apply()
        Coords((- self.__width), spanInElements - self.__height).apply()
        Coords((widthPainel - self.__width),
               spanInElements - self.__height).apply()
        Color(198/255, 233/255, 240/255).apply()
        Coords((widthPainel-self.__width), - self.__height).apply()
        Coords((-self.__width), - self.__height).apply()
        glEnd()

    def isInside(self):
        pass

    # Check if any windowsBar have been close, case true removes its
    def verifyBars(self, x: int, y: int) -> bool:

        index = 0
        elementRemoved = False
        for i in range(len(self.workSet)):
            index = i
            if(self.workSet[i].close(x, y)):
                self.workSet.pop(i)
                self.__abaId = self.__abaId-1
                elementRemoved = True
                break

        someoneFocus = False
        if elementRemoved == True:
            for i in range(len(self.workSet)):
                if index <= i:
                    self.workSet[i].updateWindowBarNumber(
                        self.workSet[i].getWindowBarNumber() - 1)
                if self.workSet[i].getFocus() == True:
                    someoneFocus = True

            if (someoneFocus == False) and len(self.workSet) > 0:
                self.workSet[len(self.workSet)-1].setFocus(True)
                self.__whatAbaIsFocus = self.workSet[len(
                    self.workSet)-1].getWindowBarNumber()
        return elementRemoved

    # Check if any event is triggered in the windowBar. Case true, assign focus to this windowBar and remove
    # focus from the previous windowBar
    def windowBarFocusNow(self, x: int, y: int):
        newFocus = -1
        isFocus = -1
        for i in range(len(self.workSet)):
            if self.workSet[i].wereClickBar(x, y) == True:
                newFocus = i
            if self.workSet[i].getFocus() == True:
                isFocus = i
        if len(self.workSet) > 1:
            if newFocus != -1:
                for i in self.workSet:
                    i.setFocus(False)

                self.workSet[newFocus].setFocus(True)
                self.__whatAbaIsFocus = self.workSet[newFocus].getWindowBarNumber(
                )

    # Configure the coordinates of the Tools. This coordinates are based on the size of glut window

    def configurePositionTools(self):
        y = self.__height - 5
        x = self.__width - 100
        spanInElements = 15
        if self.tools is not None:
            for i in self.tools:
                i.setCoords(Coords(x, y))
                x = x+spanInElements

    # Configure the coordidantes of the windowsBars. This coordinates are based on the size of the glut window
    def configureWorkSetPosition(self):
        for i in self.workSet:
            i.setSizeWindow(Coords(self.__width, self.__height))

   # Check if the icon moreAba was triggered. If true add a new aba and remove the focus the previous aba
    def monitoreWindowsTools(self, coords: Coords):
        for i in self.tools:
            if isinstance(i, IconMoreAba):
                if i.isInside(coords.getX(), coords.getY()) == True:
                    windowBar = WindowsBar(self.__abaId)
                    windowBar.setSizeWindow(
                        Coords(self.__width, self.__height))
                    self.workSet.append(windowBar)
                    windowBar.onlyOneFocus(self.workSet)
                    self.__whatAbaIsFocus = self.__abaId
                    self.__abaId = self.__abaId+1

    def addComponent(self, coords: Coords):

        # melhorar
        for i in self.workSet:
            if i.getFocus() == True:
                i.addComponentWindow(coords)
                break

    def event(self, event_type: int, key=None, button=None, state=None, coords: Coords = None) -> bool:

        # check if any icons have been triggered
        self.monitoreWindowsTools(coords)
        # check if any bars have been triggered and assign focus to her
        self.windowBarFocusNow(coords.getX(), coords.getY())
        # check if any bars have close, if true remove its
        self.verifyBars(coords.getX(), coords.getY())
        self.addComponent(coords)

        # If there is a tab in focus triggered the event in its tab
        if self.__whatAbaIsFocus > -1:
            self.workSet[self.__whatAbaIsFocus].event(
                event_type, key=key, button=button, state=state, coords=coords)

        return None
