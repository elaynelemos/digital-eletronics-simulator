"""
*   Universidade Federal do Vale do São Francisco - Univasf
*   Colegiado de Engenharia de Computação
*   Orientador: Prof. Dr. Jorge Cavalcanti
*   Discentes: Elayne Lemos, elayne.l.lemos@gmail.com
*              Jônatas de Castro, jonatascastropassos@gmail.com
*              Ezequias Antunes, ezequiasantunes@gmail.com
*   Atividade: pt-br/ este arquivo implementa o analisador lógico que vai avaliar a saída  
*                     do circuito no simulador.
*              en-us/ this file implements the logic analyzer which will evaluate the output
*                     of the circuit at the simulator.
*
"""

from typing import List
from components import *

class LogicAnalyzer:
    __entries:List[Entry] = []
    __wires:List[Wire] = []
    __checkers:List[Checker] = []
    
    def __init__(self, entries:List[Entry], wires:List[Wire],checkers:List[Checker]) -> None:
        self.setEntries(entries)
        self.setWires(wires)
        self.setCheckers(checkers)


    def setEntries(self, entries:List[Entry]) -> bool:
        try:
            for i in entries:
                if isEntry(i):
                    self.__entries.append(i)
                else:
                    raise AttributeError("Error! Entry attribute expected. Entries not defined. You tried to assign an", type(i))
        except AttributeError as ae:
            print(ae)
            self.__entries = []
            return False
        else:
            return True

    def setWires(self, wires:List[Wire]) -> bool:
        try:
            for i in wires:
                if isinstance(i, List):
                    self.__wires.append(i)
                else:
                    raise AttributeError("Error! List attribute expected. List not defined. You tried to assign an", type(i))
        except AttributeError as ae:
            print(ae)
            self.__wires = []
            return False
        else:
            return True

    def setCheckers(self, checkers:List[Checker]) -> bool:
        try:
            for i in checkers:
                if isChecker(i):
                    self.__checkers.append(i)
                else:
                    raise AttributeError("Error! Checker attribute expected. Checkers not defined. You tried to assign an", type(i))
        except AttributeError as ae:
            print(ae)
            self.__checkers = []
            return False
        else:
            return True


    def getEntries(self) -> List[Entry]:
        return self.__entries
    
    def getWires(self) -> List[Wire]:
        return self.__wires

    def getCheckers(self) -> List[Checker]:
        return self.__checkers

    def __netList(self):
        for wire in self.getWires():
            for wire2 in self.getWires():
                if(wire != wire2):
                    if(wire[1].equals(wire2[0])):
                        wire2[0] = wire[0]
                    if(wire[1].equals(wire2[1])):
                        wire2[1] = wire[0]

            for entry in self.getEntries():
                if(wire[1].equals(entry.getTechCoords())):
                    entry.setTechCoords(wire[0])
            for check in self.getCheckers():
                if(wire[1].equals(check.getTechCoords())):
                    check.setTechCoords(wire[0])


    def __validateLists(self):
        for i in self.__entries:
            for k in self.__entries:
                if i!= k and i.getTechCoords().equals(k.getTechCoords()):
                            raise RuntimeError("Error! Entries connected. "+str(i)+ " with " + str(k)+".")
    
        return True

    def __defineValues(self) -> bool:
        t = {}
        thereUnchecked = True

        while thereUnchecked:
            thereUnchecked=False
            for check in self.getCheckers():
                thereUnchecked = True if (not check.getChecked()) else thereUnchecked
                if not check.getChecked():
                    isConnected = False
                    for i in self.getEntries():
                        if i.getTechCoords().equals(check.getTechCoords()):
                            isConnected = True
                            if(i.getGate()!= None):
                                gate = i.getGate()
                                checked = True
                                for j in gate.getChecks():
                                    checked = checked and j.getChecked()
                                if checked:    # caso 3
                                    check.setValue(gate.gateOut().getValue())
                                    check.setChecked(True)
                            else:   # casos 1 e 2
                                check.setValue(i.getValue())
                                check.setChecked(True)
                    if not isConnected:
                        check.setValue(None)
                        check.setChecked(True)
                                
        # o caso 4 não consta no meio porque ele é resultado da combinação iterativa desses casos,
        # observe que se uma porta é conectada a outra, mas o check que aponta para ela aparecer primeiro, 
        # essa sequencia saltará a verificação dessa, devido a falta de informações, e percorrerá quantas vezes forem
        # necessárias para completar a verificação
        return True

    def __prepareCheckers(self) -> None:
        for i in self.__checkers:
            i.setChecked(False)
            i.setValue(None)


    def analyze(self) -> bool:
        if self.__validateLists() is False:
            return None
        self.__netList()            
        self.__prepareCheckers()
        return self.__defineValues()


