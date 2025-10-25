from __future__ import annotations
from enum import Enum
from typing import List

class Operator(Enum):
    
    PLUS = ('+', lambda x, y: x + y)
    MINUS = ('-', lambda x, y: x - y)
    MULT = ('*', lambda x, y: x * y)
    DIV = ('/', lambda x, y: x / y)

    def __str__(self) -> str:
        return str(self.value[0])

    def berechne(self, operand_1: float, operand_2: float) -> float:
        return self.value[1](operand_1, operand_2)
        
    def istStrichrechnung(self) -> bool:
        return not self.istPunktrechnung()
    
    def istPunktrechnung(self) -> bool:
        return self is Operator.MULT or self is Operator.DIV

    def bindetGleich(self, operator: Operator) -> bool:
        return not self.bindetSchwaecher(operator) and not self.bindetStaerker(operator)

    def bindetSchwaecher(self, operator: Operator) -> bool:
        return self.istStrichrechnung() and operator.istPunktrechnung()

    def bindetStaerker(self, operator: Operator) -> bool:
        return self.istPunktrechnung() and operator.istStrichrechnung()

    @staticmethod
    def werte_liste() -> List[str]:
        return [member.value[0] for member in Operator]

    @staticmethod
    def ist_operator_zeichen(zeichen: str) -> bool:
        return zeichen in Operator.werte_liste()