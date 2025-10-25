from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from operatoren import Operator

@dataclass()
class BaumKnoten(ABC):

    @abstractmethod
    def berechne_wert(self) -> float: pass

    @abstractmethod
    def einfacher_text(self) -> str: pass

    @abstractmethod
    def empfange_besucher(self, besucher: BaumKnoten_Visitor) -> None: pass


@dataclass()
class ZahlKnoten(BaumKnoten):
    
    wert: float = 0.0

    def __str__(self) -> str:
        return str(self.wert)
    
    def berechne_wert(self) -> float:
        return self.wert

    def einfacher_text(self) -> str:
        return str(self)

    def empfange_besucher(self, besucher: BaumKnoten_Visitor) -> None:
        besucher.besuche_wert_knoten(self)


@dataclass()
class OperatorKnoten(BaumKnoten):

    __operator: Operator
    __linker_knoten: BaumKnoten
    __rechter_knoten: BaumKnoten

    def __init__(self, operator: Operator) -> None:
        self.__operator = operator
        if self.__operator.ist_punktrechnung():
            self.__linker_knoten = ZahlKnoten(1.0)
            self.__rechter_knoten = ZahlKnoten(1.0)
        else:
            self.__linker_knoten = ZahlKnoten(0.0)
            self.__rechter_knoten = ZahlKnoten(0.0)

    @property
    def operator(self) -> Operator:
        return self.__operator
    
    @property
    def linker_knoten(self) -> BaumKnoten:
        return self.__linker_knoten
    
    @linker_knoten.setter
    def linker_knoten(self, knoten: BaumKnoten) -> None:
        self.__linker_knoten = knoten

    @property
    def rechter_knoten(self) -> BaumKnoten:
        return self.__rechter_knoten
    
    @rechter_knoten.setter
    def rechter_knoten(self, knoten: BaumKnoten) -> None:
        self.__rechter_knoten = knoten

    def __str__(self) -> str:
        return "(" + str(self.__linker_knoten) + " " + str(self.__operator) + " " + str(self.__rechter_knoten) + ")"

    def berechne_wert(self) -> float:
        return self.__operator.berechne(self.__linker_knoten.berechne_wert(), self.__rechter_knoten.berechne_wert())
    
    def einfacher_text(self) -> str:
        return str(self.__operator)

    def empfange_besucher(self, besucher: BaumKnoten_Visitor) -> None:
        besucher.besuche_operator_knoten(self)


@dataclass()
class VorzeichenKnoten(BaumKnoten):    

    __innerer_knoten: BaumKnoten

    def __init__(self, innerer_knoten: BaumKnoten = ZahlKnoten(0.0)):
        self.__innerer_knoten = innerer_knoten

    @property
    def innerer_knoten(self) -> BaumKnoten:
        return self.__innerer_knoten

    def __str__(self) -> str:
        return "-" + str(self.__innerer_knoten)
        
    def einfacher_text(self) -> str:
        return "~"

    def berechne_wert(self) -> float:
        return -1 * self.__innerer_knoten.berechne_wert()

    def empfange_besucher(self, besucher: BaumKnoten_Visitor) -> None:
        besucher.besuche_vorzeichen_knoten(self)


class BaumKnoten_Visitor(ABC):

    @abstractmethod
    def besuche_operator_knoten(self, knoten: OperatorKnoten) -> None: pass

    @abstractmethod
    def besuche_vorzeichen_knoten(self, knoten: VorzeichenKnoten) -> None: pass

    @abstractmethod
    def besuche_wert_knoten(self, knoten: ZahlKnoten) -> None: pass