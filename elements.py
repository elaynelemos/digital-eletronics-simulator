from components import Element, Coords
from components import Entry, Checker, Display, NotGate, AndGate, NandGate, OrGate, NorGate, XorGate, XnorGate, KeyBoard
from logicanalyzer import*
from util import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


componentClasses = [Entry, Checker, Display, NotGate, AndGate,
                    NandGate, OrGate, NorGate, XorGate, XnorGate, KeyBoard]

EVENT_TYPE_MOUSE_WALKING_NOT_PRESS = 0
EVENT_TYPE_KEY_ASCII = 1
#Types of wires
TYPE_WIRE_Z = 0
TYPE_WIRE_Z_INVERT = 1 
ROTATE = 0
DUPLICATE = 1
DELETE = 2

#This class is resposible for draw the wires in window. All the operations needed 
#to do this are here
class WireManager(Element):
    __startWire: Coords = Coords(0,0)          #Wire star coordinate
    __endWire: Coords = Coords(0,0)            #Wire end coordinate
    __drawWire: bool = False            #Determine if the user want draw a wire
    __typeWire: int = None              #Determine type wire
    __wireCanceled: bool = False
    __start: bool = True
    def __init__(self):
        super().__init__()
        self.dotsWires = []
        self.setTypeWire(TYPE_WIRE_Z_INVERT)

    def getDotsWires(self):
        return self.dotsWires
    def setTypeWire(self,type: int):
        self.__typeWire = type
    def setEndWire(self,coords = Coords):
        self.__endWire = coords
    def getEndWire(self)->Coords:
        return self.__endWire
    def setStartWire(self,coords = Coords):
        self.__startWire = coords
    def getStartWire(self)->Coords:
        return self.__drawWire
    def setDrawWire(self,yes: bool):
        self.__drawWire = yes
    def getDrawWire(self)->bool:
        return self.__drawWire
    

    def validPoint(self,x: float)->int:
      
        valor = (x -x%POINT_SPACE + POINT_SPACE) if x%POINT_SPACE>0 else (x - x%POINT_SPACE)
        return int(valor)
    
    #Procedure needed for translate the coordinate wires
    def updateCoordDotsWires(self,translate: Coords):
        for i in self.dotsWires:
            for j in range(len(i)):
                coord = (Coords(i[j].getX()+translate.getX(), i[j].getY()+translate.getY()))
                i[j] = coord

    #Procedure for draw the current wire,whose wire yet not been completed by the user
    def drawWireCurrent(self):
        Color(0.0,0.0,0.0).apply()
        glBegin(GL_LINE_STRIP)

        Coords(self.validPoint(self.__startWire.getX()),self.validPoint(self.__startWire.getY())).apply()
        if self.__typeWire == TYPE_WIRE_Z_INVERT:
            Coords(self.validPoint(self.__startWire.getX()),self.validPoint((self.__endWire.getY() + self.__startWire.getY())/2)).apply()
            Coords(self.validPoint(self.__endWire.getX()),self.validPoint((self.__endWire.getY()+self.__startWire.getY())/2)).apply()
        if self.__typeWire == TYPE_WIRE_Z:
            Coords(self.validPoint((self.__startWire.getX() + self.__endWire.getX())/2),self.validPoint(self.__startWire.getY())).apply()
            Coords(self.validPoint((self.__startWire.getX()+self.__endWire.getX())/2),self.validPoint(self.__endWire.getY())).apply()
        Coords(self.validPoint(self.__endWire.getX()),self.validPoint(self.__endWire.getY())).apply()
        glEnd()

    #Take the coordinates of the last wire the user made and add it to the wire list to draw 
    # porsteriomente
    def addDotsToWire(self):
        list = []
        list.append(Coords(self.validPoint(self.__startWire.getX()),self.validPoint(self.__startWire.getY())))
        if self.__typeWire == TYPE_WIRE_Z_INVERT:
            list.append(Coords(self.validPoint(self.__startWire.getX()),self.validPoint((self.__endWire.getY() + self.__startWire.getY())/2)))
            list.append(Coords(self.validPoint(self.__endWire.getX()),self.validPoint((self.__endWire.getY()+self.__startWire.getY())/2)))
        if self.__typeWire == TYPE_WIRE_Z:
            list.append( Coords(self.validPoint((self.__startWire.getX() + self.__endWire.getX())/2),self.validPoint(self.__startWire.getY())))
            list.append(Coords(self.validPoint((self.__startWire.getX()+self.__endWire.getX())/2),self.validPoint(self.__endWire.getY())))
        list.append(Coords(self.validPoint(self.__endWire.getX()),self.validPoint(self.__endWire.getY())))
        self.dotsWires.append(list)
        

    def isInside(self, coords):
        for i in self.elements:
            if i.isInside(coords) == True:
                return i
        return None
            


    #Draw all wires already terminated    
    def drawAllWires(self):
        for i in self.dotsWires:

            Color(0.0,0.0,0.0).apply()
            glBegin(GL_LINE_STRIP)
            for j in i:
               j.apply()
            glEnd()

    #Draw wire
    def draw(self):
        self.drawAllWires()
        if self.__drawWire == True:
            self.drawWireCurrent()




    def event(self, event_type: int, key=None, button=None, state=None, coords=None, window =None) -> bool:
       
        m = glutGetModifiers()
        
        if window is not None and window.getDragComponent()== False:
            
            if event_type == EVENT_TYPE_MOUSE:
          
                if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
                    self.__drawWire = True
                    self.__wireCanceled = False
                    self.setStartWire(coords)

                #if button == GLUT_RIGHT_BUTTON and state == GLUT_UP:
            if m == GLUT_ACTIVE_CTRL:
                    self.__drawWire = False
                    if self.__wireCanceled == False:
                        self.addDotsToWire()    

            if event_type == EVENT_TYPE_KEY_ASCII and key ==  b'\x1b':
                self.__drawWire = False
                self.__wireCanceled = True
               
            
            if event_type == EVENT_TYPE_MOUSE_WALKING_NOT_PRESS:
                
                if self.__drawWire == True:
                    self.setEndWire(coords)
        else:
            self.__drawWire = False   
        
        return False

#This class is responsible for draw the elements like gaters and entrys and grid 
class Window(Element):

    factor: float = 0.1
    __dragComponent: bool = False
    __currentComponentDragged: int = 0 
    __simulation: bool = False
    __logicAnalyzer: LogicAnalyzer = None

    def __init__(self):
        super().__init__()
        self.center = Coords(0, 0)
        self.size = Coords(0, 0)
        self.zoom = 1.0
        self.elements = []
        self.windowStartPosition = Coords(0,0)
        self.checks = []
        self.keyboards = []
        self.entrys = []
        self.gates = []
        self.displays = []
        self.wires = []
        self.logic = None

    def breakListElements(self):
        for i in self.elements:
            if isinstance(i,(NotGate, AndGate,NandGate, OrGate, NorGate, XorGate, XnorGate)):    
                self.gates.append(i)
            elif isinstance(i,KeyBoard):
                self.keyboards.append(i)
            elif isinstance(i,Checker):
                self.checks.append(i)
            elif isinstance(i,Entry):
                self.entrys.append(i)
            elif isinstance(i,Display):
                self.displays.append(i)

    def ativateSimulation(self):
        self.breakListElements()
        checks = []
        entrys = []
        
        
        for i in self.gates:
            checks.extend(i.getChecks())
            entrys.append(i.gateOut())

        for i in self.displays:
            checks.extend(i.getChecks())

        for i in self.keyboards:
            entrys.extend(i.getEntries())

        #for i in self.wires:
            #wire.append(Wire(i))
        
        checks.extend(self.checks)
        entrys.extend(self.entrys)
        self.__logicAnalyzer = LogicAnalyzer(entrys, self.wires, checks)
        self.wires.clear()

    def deactivateSimulation(self):
        self.__logicAnalyzer = None
        self.wires.clear()
        print("sim")

    
    def isSimulation(self)->bool:
        return self.logicAnalyzer == None

    def setDragComponent(self, drag):
        self.__dragComponent = drag

    def getDragComponent(self):
        return self.__dragComponent
    #Set the window position in the current coordinates plane
    def setWindowStartPosition(self, windowStartPosition: Coords):
        self.windowStartPosition = windowStartPosition
        
    def getWindowStartPosition(self)->Coords:
        return self.windowStartPosition

    #Set the window center in the current coordinates plane
    def setCenter(self, center: Coords):
        self.center = center
        return self

    def getCenter(self)->Coords:
        return self.center

    #Set the window center in the current coordinates plane
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

    def validPoint(self,x: float)->int:
        if x>=0:
            valor = (x -x%POINT_SPACE + POINT_SPACE) if x%POINT_SPACE>0 else (x - x%POINT_SPACE)
            return int(valor)
        else: 
            valor = (x - x%POINT_SPACE) if x%POINT_SPACE>0 else (x -x%POINT_SPACE + POINT_SPACE) 
            return int(valor)

    def draw(self):
        if self.__logicAnalyzer is not None:
            self.__logicAnalyzer.analyze()
         # self.logicAnalyzer.apply()
        #Draw the windows grid
        Color(0.0,0.0,0.0).apply()
        glPointSize(1.0)
        glBegin(GL_POINTS)
        for i in range(self.validPoint(self.windowStartPosition.getX()),self.validPoint(self.size.getX()), 5):
            for j in range(self.validPoint(self.windowStartPosition.getY()),self.validPoint(self.size.getY()), 5):
                Coords(i,j).apply()
        glEnd()        
        
       
        #self.center.draw(radius=1.0)
        #Draw the elements in window
        for i in self.elements:
            i.draw()
        return self
       
    def adjustCenter(self):
        self.setCenter(Coords(self.validPoint((self.size.getX()/2)+self.windowStartPosition.getX()), self.validPoint((self.size.getY()/2)+self.windowStartPosition.getY())))
       
    def updateCoordsElementsWindows(self, translate: Coords):
         for i in self.elements:
                i.setCoords(Coords(i.getCoords().getX()+translate.getX(),i.getCoords().getY()+translate.getY()))

    def getIndexComponentIsInside(self, coords: Coords):
        for i in range(len(self.elements)):
            if self.elements[i].isInside(coords) == True:
                return i
        return -1

    def prepareWireForSimulation(self, wireManager: WireManager):
        for i in wireManager.getDotsWires():
            l = []
            l.append(i[0])
            l.append(i[-1])
            self.wires.append(l)

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        print('Logic',self.__logicAnalyzer)
        
      
        if self.__logicAnalyzer is not None:
            print("sim")
            for i in range(len(self.elements)):
                if(self.elements[len(self.elements)-i-1].event(event_type, key, button, state, coords)):
                    return True
            return False
        else:
            if event_type == EVENT_TYPE_MOUSE and button == GLUT_LEFT_BUTTON and state == GLUT_UP:
           
                if len(self.elements)> 0:
                    if self.__dragComponent == False:
                        index = self.getIndexComponentIsInside(coords)
                        if index != -1:
                            self.__currentComponentDragged = index
                            self.__dragComponent = True
                            return True
                    else:
                        self.__dragComponent = False
                        return True
            
            if event_type == EVENT_TYPE_MOUSE_WALKING_NOT_PRESS:
                if self.__dragComponent == True:
                    self.elements[ self.__currentComponentDragged].setTranslation(Coords(self.validPoint(coords.getX()),self.validPoint(coords.getY())))
                    return True

        return False

    def isInside(self, coords) -> bool:
        return False
"""
class Menu(Element):
    __indexComponent: int = -1

    def __init__(self, coords =Coords(0,0)):
        self.super().__init__()

    def menu(self, a):   
        pass
    def rotateElement(window: Window):
        if window is not None:
            index = window.getIndexComponentIsInside()
            if index != -1:
                self.__indexComponent = index

    def rotate(self, selection):
        if selection == 0:
            pass
        if selection == 1:
            pass
    def createMenu(self):

        #submenu2 = glutCreateMenu(self.rotate)
        #glutAddMenuEntry("90 degrees left",0)
        #glutAddMenuEntry("90 degrees left",1)
	    
        menu =  glutCreateMenu(self.menu)
        #glutAddSubMenu("Rotate", submenu2)
        glutAddMenuEntry("Rotate", 0)
        glutAddMenuEntry("Delete",1)
        glutAddMenuEntry("Duplicate",2)
     
        glutAttachMenu(GLUT_RIGHT_BUTTON)

    
        
    def isInside(self):
        pass

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_RIGHT_BUTTON:
            self.createMenu()
        return None
"""

# Painel contends the logics ports and others components like checker and entry 
# for choose by user.
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
        self.iconsComponnent = []
        span = self.initPainelComponents
        for i in componentClasses:
            span = span + self.sizeCell
            self.iconsComponnent.append(i(coords=Coords(
                14-self.__coords.getX(), span-self.sizeCell/2), size=self.sizeCell*0.8))

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

            self.iconsComponnent[i].draw(n=False)

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
    def component(self, coord: Coords, elementsPositionStart: Coords = Coords(0,0)):

        if self.isInside(coord.getX(), coord.getY()) == True:
            component = self.componentChoosed(coord.getY())
          
            if component == ENTRY:
                return Entry(elementsPositionStart).setValue(True)
                
            elif component == CHECKER:
                return Checker(elementsPositionStart)
            elif component == DISPLAY:
                return Display(elementsPositionStart)
            elif component == NOTGATE:
                return NotGate(elementsPositionStart)
            elif component == ANDGATE:
                return AndGate(elementsPositionStart)
            elif component == NANDGATE:
                return NandGate(elementsPositionStart)
            elif component == ORGATE:
                return OrGate(elementsPositionStart)
            elif component == NORGATE:
                return NorGate(elementsPositionStart)
            elif component == XORGATE:
                return XorGate(elementsPositionStart)
            elif component == XNORGATE:
                return XnorGate(elementsPositionStart)
            elif component == KEYBOARD:
                return KeyBoard(elementsPositionStart)
            else:
                return None

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        
        return None

# The Panel contains the workspace. Here can assemble the components and simulate them.
class Panel(Element):

    # Coordinate of glut windows, value required to built the painel.
    __coords: Coords = None
    __window: Window = None  # All components will be stored here.
    __wireManager: WireManager = None
    __translation: Coords = None
    __activateMenu: bool = False
    __indexComponent: int = -1
    __coordsClick: Coords= None
    

    def __init__(self, coords):
        super().__init__()
        self.setCoords(coords)
        self.setWindow(Window())
        self.shift = 15         
        self.getWindow().setWindowStartPosition(Coords(27-self.__coords.getX(),24- self.__coords.getY() ))
        self.getWindow().setSize(Coords(self.__coords.getX()*2 - 27,self.__coords.getY()*2 -24))
        self.setWireManager(WireManager())
        self.translateWindows(Coords(0,0))
        self.__window.adjustCenter()
    
    def translateWindows(self,coords: Coords):

        self.__translation = coords
    
    def translate(self, coords:Coords):
        self.__window.updateCoordsElementsWindows(coords)
        self.__wireManager.updateCoordDotsWires(coords)

    def setWireManager(self, wireManager: WireManager):
        self.__wireManager = wireManager

    def getWireManager(self)->WireManager:
        return  self.__wireManager

    def setCoords(self, coords: Coords) -> bool:
        self.__coords = coords
        if self.__window is not None:
            self.getWindow().setWindowStartPosition(Coords(27-self.__coords.getX(),self.shift +24- self.__coords.getY() ))
            self.getWindow().setSize(Coords(self.__coords.getX()*2 - 27,self.__coords.getY()*2 - self.shift +24))
       

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
        glVertex2f((27-self.__coords.getX()),self.shift +24- self.__coords.getY())
        glVertex2f(27-self.__coords.getX(),self.shift + self.__coords.getY())
        glVertex2f(self.__coords.getX()-3, self.shift +self.__coords.getY())
        glVertex2f(self.__coords.getX()-3,self.shift + 24-self.__coords.getY())
        glEnd()
        glLineWidth(3)

        # draw panel contents
        if self.__window is not None:
          
            self.__window.draw()
            self.__wireManager.draw()


        
    def rotate(self, selection):
        if selection == 0:
            if self.__indexComponent == -1:
                pass
            else:
                self.__window.elements[self.__indexComponent].setRotation()
            return 0
        
        if selection == 1:
            if len(self.__window.elements)>0 and self.__indexComponent != -1:
                if self.__window.getDragComponent() ==False:
                    self.__window.elements.pop(self.__indexComponent)
                

            return 0
        
            
    def createMenu(self):

     
        menu =  glutCreateMenu(self.rotate)
        glutAddMenuEntry("Rotate", 0)
        glutAddMenuEntry("Delete",1)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        return 0
    
    def isInside(self, x: int, y: int) -> bool:
        if (((27-self.__coords.getX()) < x and x < (self.__coords.getX()-3)) and ((self.shift + 23 - self.__coords.getY()) < y < (self.__coords.getY()))):
            return True
        else:
            return False

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        if event_type == EVENT_TYPE_MOUSE:
            if button == GLUT_LEFT_BUTTON:
                
                self.__indexComponent = self.__window.getIndexComponentIsInside(coords)
                print(self.__indexComponent)
                if self.__indexComponent!=-1:
                    self.createMenu()
                 
               

               
            if self.isInside(coords.getX(), coords.getY()) == True:
                self.__wireManager.event(event_type, key, button, state, coords,self.__window)

        if event_type == EVENT_TYPE_KEY_ASCII:
            self.__wireManager.event(event_type, key, button, state, coords,self.__window)

        self.__window.event( event_type, key, button, state, coords)
        return None
        
        

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
    def event(self, event_type: int, key=None, button=None, state=None, coords=None)->bool:
        pass


#The following classes are tools (draw like icons) that assist the user in the components assembly process.
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

    def isInside(self, x: int, y: int)->bool:
        return super().isInside(x,y)
    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_UP and self.isInside(coords.getX(),coords.getY()):
            windowsBar.getPanel().getWindow().prepareWireForSimulation(windowsBar.getPanel().getWireManager())
            windowsBar.getPanel().getWindow().ativateSimulation()
            print("Start Simulation: ")
           

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

    def isInside(self, x: int, y: int)->bool:
        return super().isInside(x,y)
    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_UP and self.isInside(coords.getX(),coords.getY())== True:
            windowsBar.getPanel().getWindow().deactivateSimulation()
            print("Stop Simulation: ")
        pass
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
    
    
    def isInside(self, x: int, y: int)->bool:
        return super().isInside(x,y)

    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_UP: 
            if self.isInside(coords.getX(), coords.getY()) == True:
                windowsBar.getPanel().translate(Coords(-POINT_SPACE,0))
       

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

    def isInside(self, x: int, y: int)->bool:
        return super().isInside(x,y)

    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        return None
       


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

    def isInside(self, x: int, y: int)->bool:
        return super().isInside(x,y)
    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_UP: 
            if self.isInside(coords.getX(), coords.getY()) == True:
                coordsWindow = windowsBar.getPanel().translate(Coords(POINT_SPACE,0))
                #windowsBar.getPanel().getWindow().setCenter(Coords(coordsWindow.getX()+5.0, coordsWindow.getY()))





class IconLineTypeInverterZ(Icon):
    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def draw(self):
        
        Color(14/255, 43/255, 92/255).apply()
        glBegin(GL_LINE_STRIP)
        Coords((-super().getCoords().getX()),-super().getCoords().getY()).apply()
        Coords((-super().getCoords().getX()),2.5 - super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()),2.5-super().getCoords().getY()).apply()
        Coords((5-super().getCoords().getX()),5 -super().getCoords().getY()).apply()
        glEnd()
      
    def isInside(self, x: int, y: int)->bool:
        return super().isInside(x,y)
    

    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_UP: 
            if self.isInside(coords.getX(), coords.getY()) == True:
                windowsBar.getPanel().getWireManager().setTypeWire(TYPE_WIRE_Z_INVERT)
               




class IconLineTypeZ(Icon):
    def __init__(self, coord: Coords(0, 0)):
        super().__init__(coord)

    def draw(self):
        Color(14/255, 43/255, 92/255).apply()
        glBegin(GL_LINE_STRIP)
        Coords((-super().getCoords().getX()),0-super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()),0- super().getCoords().getY()).apply()
        Coords((3-super().getCoords().getX()),5-super().getCoords().getY()).apply()
        Coords((6-super().getCoords().getX()),5 -super().getCoords().getY()).apply()
        glEnd()
       

    def isInside(self, x: int, y: int)->bool:
        return super().isInside(x,y)
    
    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        if event_type == EVENT_TYPE_MOUSE and state == GLUT_UP: 
            if self.isInside(coords.getX(), coords.getY()) == True:
                windowsBar.getPanel().getWireManager().setTypeWire(TYPE_WIRE_Z)
                
      
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

    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        pass
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

    def event(self, event_type: int, key=None, button=None, state=None, coords=None, windowsBar = None)->bool:
        pass
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
    def getPanelComponents(self):
        return self.__painelComponents

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
        glColor3f(169/255,207/255,233/255)
      
        rect(Coords(24-self.__windowSize.getX(),self.shift + 20- self.__windowSize.getY()),
        Coords(24-self.__windowSize.getX(),self.__windowSize.getY()),
        Coords(27 - self.__windowSize.getX(),self.__windowSize.getY()),
        Coords(27 -self.__windowSize.getX(),self.shift +  20-self.__windowSize.getY()))

        rect(Coords(24-self.__windowSize.getX(),self.shift + 20- self.__windowSize.getY()),
        Coords(24-self.__windowSize.getX(),self.shift + 24 -  self.__windowSize.getY()),
        Coords(self.__windowSize.getX(),self.shift + 24 - self.__windowSize.getY()),
        Coords(self.__windowSize.getX(),self.shift +  20-self.__windowSize.getY()))

        rect(Coords(self.__windowSize.getX() - 2.98,self.shift + 20- self.__windowSize.getY()),
        Coords(self.__windowSize.getX() - 2.98,self.__windowSize.getY()),
        Coords(self.__windowSize.getX(),self.__windowSize.getY()),
        Coords(self.__windowSize.getX(),self.shift +  20-self.__windowSize.getY()))

        

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

        Color(0.0,0.0,0.0).apply()
        line(Coords((68-self.__windowSize.getX()),self.shift  +16- self.__windowSize.getY()),
            Coords(72-self.__windowSize.getX(), self.shift  +12-self.__windowSize.getY()),3.0)
        
        line(Coords((68-self.__windowSize.getX()),self.shift  +12- self.__windowSize.getY()),
        Coords(72-self.__windowSize.getX(), self.shift  +16-self.__windowSize.getY()),3)
        glPopMatrix()

    def draw(self):

        if self.__focus == True:
            self.bar()
            self.drawLines()
           
        else:
            self.bar()

    def event(self, event_type: int, key=None, button=None, state=None, coords=None) -> bool:
        if event_type == EVENT_TYPE_MOUSE:
            if state == GLUT_UP:
                self.addComponentWindow(coords)
       
        if self.__panel is not None:
            self.__panel.event(event_type, key,button, state, coords)


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
   

    def drawShadow(self):
        Color(228/255, 233/255, 237/255).apply()  
        rect(Coords(-self.__width,-self.__height), Coords(-self.__width,self.__height),Coords(27-self.__width,self.__height),Coords(27-self.__width,-self.__height))
        rect(Coords(27-self.__width,-self.__height), Coords(27-self.__width,38-self.__height),Coords(self.__width,38-self.__height),Coords(self.__width,-self.__height))
        
    def draw(self):
        
        
        if self.__whatAbaIsFocus > -1:
            self.workSet[self.__whatAbaIsFocus].getPanel().draw()
            self.drawShadow()
            self.workSet[self.__whatAbaIsFocus].getPanelComponents().draw()
        #self.drawShadow()
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
        x = self.__width - 130
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
       
    def event(self, event_type: int, key=None, button=None, state=None, coords: Coords = None) -> bool:

        if state == GLUT_UP:    
            self.monitoreWindowsTools(coords)                       #check if any icons have been triggered
            self.windowBarFocusNow(coords.getX(), coords.getY())    #check if any bars have been triggered and assign focus to her
            self.verifyBars(coords.getX(), coords.getY())           #check if any bars have close, if true remove its
           
        
        #If there is a tab in focus triggered the event in its tab
        if  self.__whatAbaIsFocus > -1: 
                self.workSet[self.__whatAbaIsFocus].event(event_type, key=key, button=button, state=state, coords=coords)
                if len(self.tools) > 0:
                    for i in self.tools:
                        i.event(event_type, key, button, state, coords, self.workSet[self.__whatAbaIsFocus])
        return None
