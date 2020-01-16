"""
*   Universidade Federal do Vale do São Francisco - Univasf
*   Colegiado de Engenharia de Computação
*   Orientador: Prof. Dr. Jorge Cavalcanti
*   Discentes: Elayne Lemos, elayne.l.lemos@gmail.com
*              Jônatas de Castro, jonatascastropassos@gmail.com
*              Ezequias Antunes, ezequiasantunes@gmail.com
*   Atividade: pt-br/ este arquivo define as constantes a serem utilizadas pelo simulador de 
*                     eletrônica digital.
*              en-us/ this file defines the constants those will be used at the digital
*                     eletronics simulator.
*
"""

from typing import List
from components import *

class LogicAnalyzer:
    __entries:List[Entry] = []
    __wires:List[Wire] = []
    __checkers:List[Checker] = []

    def __init__(self, entries:List[Entry], wires:List[Wire],checkers:List[Checker]) -> None:
        try:
            for i in entries:
                if isEntry(i):
                    self.__entries.append(i)
                else:
                    raise AttributeError("Error! Entry attribute expected. You tried to assign an", type(i))
            for i in wires:
                if isWire(i):
                    self.__wires.append(i)
                else:
                    raise AttributeError("Error! Wire attribute expected. You tried to assign an", type(i))
            for i in checkers:
                if isChecker(i):
                    self.__checkers.append(i)
                else:
                    raise AttributeError("Error! Checker attribute expected. You tried to assign an", type(i))
        except AttributeError as ae:
            print(ae)
            self.__entries = []
            self.__wires = []
            self.__checkers = []

    def defineValues(self) -> bool:
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
            a = i
            while i.getChecked() is False:
                while a.getChecked() is False:
                    eq = True
                    print(a.getChecked())
                    for j in self.__entries:
                        if isEqualPoints(a.getCoords(), j.getCoords()):
                            checkers = j.getGate().getChecks()
                            for k in checkers:
                                if k.getChecked() is False:
                                    a = k
                                    eq = False
                                    print("entrou")
                                    break
                            if eq:
                                a.setValue(j.getGate().gateOut().getValue())
                                a.setChecked(True)
                                print(a.getChecked())
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


    def prepareCheckers(self) -> None:
        for i in self.__checkers:
            i.setChecked(False)

    def analyze(self) -> bool:
        self.prepareCheckers()
        return self.defineValues()


#versão com verificação
"""
    def defineValues(self) -> bool:
        try:
            for i in self.__entries:
                for j in self.__entries:
                    if isEqualPoints(i.getCoords(), j.getCoords()):
                        raise RuntimeError("Error! Entries connected:", i.id(), j.id())
                for j in self.__wires:
                    if isEqualPoints(i.getCoords(), j.getWireEndP()):
                        for k in self.__entries:
                            if isEqualPoints(j.getWireStartP(), k.getCoords()):
                                raise RuntimeError("Error! Entries connected:", i.id(), k.id())
        except RuntimeError as re:
            print(re)
            return False
        else:
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
                a = i
                while i.getChecked() is False:
                    while a.getChecked() is False:
                        for j in self.__entries:
                            if isEqualPoints(a.getCoords(), j.getCoords()):
                                checkers = j.getGate().getChecks()
                                for k in checkers:
                                    if k.getChecked() is False:
                                        a = k
                                        break
                                if i==a:
                                    i.setValue(j.getGate().gateOut().getValue())
                                    i.setChecked(True)
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
                                                break
                                        if i==a:
                                            i.setValue(k.getGate().gateOut().getValue())
                                            i.setChecked(True)
                                        else:
                                            break
                                if i!=a:
                                    break
            return True



"""



#versão sem verificação
"""
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
            a = i
            while i.getChecked() is False:
                while a.getChecked() is False:
                    for j in self.__entries:
                        if isEqualPoints(a.getCoords(), j.getCoords()):
                            checkers = j.getGate().getChecks()
                            for k in checkers:
                                if k.getChecked() is False:
                                    a = k
                                    break
                            if i==a:
                                i.setValue(j.getGate().gateOut().getValue())
                                i.setChecked(True)
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
                                            break
                                    if i==a:
                                        i.setValue(k.getGate().gateOut().getValue())
                                        i.setChecked(True)
                                    else:
                                        break
                            if i!=a:
                                break
        return True

"""