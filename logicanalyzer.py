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
                if isWire(i):
                    self.__wires.append(i)
                else:
                    raise AttributeError("Error! Wire attribute expected. Wires not defined. You tried to assign an", type(i))
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


    def __validateLists(self):
        try:
            for i in self.__entries:
                for j in self.__wires:
                    if isEqualPoints(i.getCoords(), j.getWireEndP()):
                        for k in self.__entries:
                            if isEqualPoints(j.getWireStartP(), k.getCoords()):
                                raise RuntimeError("Error! Entries connected.")
            for i in self.__checkers:
                for j in self.__wires:
                    if isEqualPoints(i.getCoords(), j.getWireEndP()):
                        for k in self.__checkers:
                            if isEqualPoints(j.getWireStartP(), k.getCoords()):
                                raise RuntimeError("Error! Checkers connected.")
        except RuntimeError as re:
            print(re)
            return False
        else:
            return True

    def __defineValues(self) -> bool:
        for i in self.__entries:
            if i.getGate() is None:
                for j in self.__checkers:
                    if isEqualPoints(i.getCoords(), j.getCoords()):
                        j.setValue(i.getValue())
                        j.setChecked(True)
                for j in self.__wires:
                    if isEqualPoints(i.getCoords(), j.getWireStartP()):
                        for k in self.__checkers:
                            if isEqualPoints(j.getWireEndP(), k.getCoords()):
                                k.setValue(j.getValue())
                                i.setChecked(True)                     
        for i in self.__checkers:
            ctrl = True
            for j in self.__entries:
                if isEqualPoints(i.getCoords(), j.getCoords()):
                    ctrl = False
                    break
            for j in self.__wires:
                if isEqualPoints(i.getCoords(), j.getWireEndP()):
                    for k in self.__entries:
                        if isEqualPoints(j.getWireStartP(), k.getCoords()):
                            ctrl = False
                            break
                    if not ctrl:
                        break
            if ctrl:
                i.setChecked(True)
                i.setValue(None)
        for i in self.__checkers:
            while i.getChecked() is False:
                a = i
                while a.getChecked() is False:
                    eq = True
                    for j in self.__entries:
                        if isEqualPoints(a.getCoords(), j.getCoords()):
                            checkers = j.getGate().getChecks()
                            for k in checkers:
                                if k.getChecked() is False:
                                    a = k
                                    eq = False
                                    break
                            if eq:
                                a.setValue(j.getGate().gateOut().getValue())
                                a.setChecked(True)
                            else:
                                break
                    for j in self.__wires:
                        if isEqualPoints(a.getCoords(), j.getWireEndP()):
                            for k in self.__entries:
                                if isEqualPoints(j.getWireStartP(), k.getCoords()):
                                    checkers = k.getGate().getChecks()
                                    for p in checkers:
                                        if p.getChecked() is False:
                                            a = p
                                            eq = False
                                            break
                                    if eq:
                                        a.setValue(k.getGate().gateOut().getValue())
                                        a.setChecked(True)
                                    else:
                                        break
                            if eq is False:
                                break
        return True

    def __prepareCheckers(self) -> None:
        for i in self.__checkers:
            i.setChecked(False)


    def analyze(self) -> bool:
        if self.__validateLists() is False:
            return None
        self.__prepareCheckers()
        return self.__defineValues()


