"""
*   Universidade Federal do Vale do São Francisco - Univasf
*   Colegiado de Engenharia de Computação
*   Orientador: Prof. Dr. Jorge Cavalcanti
*   Discentes: Elayne Lemos, elayne.l.lemos@gmail.com
*              Jônatas de Castro, jonatascastropassos@gmail.com
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
        self.__entries = entries
        self.__wires = wires
        self.__checkers = checkers
    

    def defineValues() -> None:
        for i in self.__checkers:
            if i.getValue() is None and i.getChecked() is False:
                for j in self.__wires:
                    if isEqualPoints(i.getCoords(), j.getWireEndP()):
                        for k in self.__entries:
                            if isEqualPoints(j.getWireStartP(), k.getCoords()):
                                i.setValue(k.getValue())
            i.setChecked(True)

    def prepareCheckers(checkers:List[Checker]) -> None:
        for i in checkers:
            i.setChecked(False)