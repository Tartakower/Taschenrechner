from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from operatoren import Operator

@dataclass()
class Baumknoten(ABC):

    @abstractmethod
    def berechne_wert(self) -> float: pass

    @abstractmethod
    def einfacher_text(self) -> str: pass

    @abstractmethod
    def empfange_besucher(self, besucher: Baumknoten_Visitor) -> None: pass


@dataclass()
class Zahlknoten(Baumknoten):
    
    _wert: float = 0.0

    @property
    def wert(self) -> float:
        return self._wert

    def __str__(self) -> str:
        return str(self._wert)
    
    def berechne_wert(self) -> float:
        return self._wert

    def einfacher_text(self) -> str:
        return str(self)

    def empfange_besucher(self, besucher: Baumknoten_Visitor) -> None:
        besucher.besuche_zahlknoten(self)


@dataclass()
class Operatorknoten(Baumknoten):

    _operator: Operator
    _linker_knoten: Baumknoten
    _rechter_knoten: Baumknoten

    def __init__(self, operator: Operator) -> None:
        self._operator = operator
        if self._operator.ist_punktrechnung():
            self._linker_knoten = Zahlknoten(1.0)
            self._rechter_knoten = Zahlknoten(1.0)
        else:
            self._linker_knoten = Zahlknoten(0.0)
            self._rechter_knoten = Zahlknoten(0.0)

    @property
    def operator(self) -> Operator:
        return self._operator
    
    @property
    def linker_knoten(self) -> Baumknoten:
        return self._linker_knoten
    
    @linker_knoten.setter
    def linker_knoten(self, knoten: Baumknoten) -> None:
        self._linker_knoten = knoten

    @property
    def rechter_knoten(self) -> Baumknoten:
        return self._rechter_knoten
    
    @rechter_knoten.setter
    def rechter_knoten(self, knoten: Baumknoten) -> None:
        self._rechter_knoten = knoten

    def __str__(self) -> str:
        return "(" + str(self._linker_knoten) + " " + str(self._operator) + " " + str(self._rechter_knoten) + ")"

    def berechne_wert(self) -> float:
        return self._operator.berechne(self._linker_knoten.berechne_wert(), self._rechter_knoten.berechne_wert())
    
    def einfacher_text(self) -> str:
        return str(self._operator)

    def empfange_besucher(self, besucher: Baumknoten_Visitor) -> None:
        besucher.besuche_operatorknoten(self)


@dataclass()
class Vorzeichenknoten(Baumknoten):    

    _innerer_knoten: Baumknoten

    def __init__(self, innerer_knoten: Baumknoten = Zahlknoten(0.0)):
        self._innerer_knoten = innerer_knoten

    @property
    def innerer_knoten(self) -> Baumknoten:
        return self._innerer_knoten

    def __str__(self) -> str:
        return "-" + str(self._innerer_knoten)
        
    def einfacher_text(self) -> str:
        return "~"

    def berechne_wert(self) -> float:
        return -1 * self._innerer_knoten.berechne_wert()

    def empfange_besucher(self, besucher: Baumknoten_Visitor) -> None:
        besucher.besuche_vorzeichenknoten(self)


@dataclass()
class Rechenbaum(Baumknoten):
    
    _wurzel: Baumknoten

    def __init__(self, wurzel: Baumknoten = Zahlknoten(0.0)):
        self._wurzel = wurzel
    
    @property
    def wurzel(self) -> Baumknoten:
        return self._wurzel
    
    @wurzel.setter
    def wurzel(self, neuer_knoten: Baumknoten) -> None:
        self._wurzel = neuer_knoten
    
    def berechne_wert(self) -> float:
        return self._wurzel.berechne_wert()
    
    def einfacher_text(self) -> str:
        return self._wurzel.einfacher_text()
    
    def __str__(self) -> str:
        return str(self._wurzel)
    
    def empfange_besucher(self, besucher: Baumknoten_Visitor) -> None:
        besucher.besuche_rechenbaum(self)


class Baumknoten_Visitor(ABC):

    @abstractmethod
    def besuche_operatorknoten(self, knoten: Operatorknoten) -> None: pass
    
    @abstractmethod
    def besuche_rechenbaum(self, knoten: Rechenbaum) -> None: pass

    @abstractmethod
    def besuche_vorzeichenknoten(self, knoten: Vorzeichenknoten) -> None: pass

    @abstractmethod
    def besuche_zahlknoten(self, knoten: Zahlknoten) -> None: pass