from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class TokenTyp(Enum):
    ZAHL = auto()
    OPERATOR = auto()
    UNAER = auto()
    KLAMMER_AUF = auto()
    KLAMMER_ZU = auto()

@dataclass(frozen=True)
class Token:
    typ: TokenTyp
    wert: str
    position: int
    
    def __str__(self) -> str:
        return f"{self.typ.name}({self.wert})"

def tokenize(formel: str) -> List[Token]:
    tokens: List[Token] = []
    aktueller_index = 0
    
    # Entferne Leerzeichen am Anfang und Ende
    formel = formel.strip()
    
    while aktueller_index < len(formel):
        aktuelles_zeichen = formel[aktueller_index]
        
        # Überspringe Leerzeichen zwischen Tokens
        if aktuelles_zeichen.isspace():
            aktueller_index += 1
            continue
            
        # Zahlen verarbeiten (ganze Zahlen und Dezimalzahlen, auch negative)
        if (aktuelles_zeichen.isdigit() or aktuelles_zeichen == '.' or 
            (aktuelles_zeichen == '-' and aktueller_index + 1 < len(formel) and 
             (formel[aktueller_index + 1].isdigit() or formel[aktueller_index + 1] == '.'))):
            
            start_position = aktueller_index
            
            # Wenn es ein Minuszeichen ist, starte mit dem nächsten Zeichen
            if aktuelles_zeichen == '-':
                aktueller_index += 1
            
            while (aktueller_index < len(formel) and 
                   (formel[aktueller_index].isdigit() or formel[aktueller_index] == '.')):
                aktueller_index += 1
            
            zahl = formel[start_position:aktueller_index]
            # Prüfe ob die Zahl gültig ist (nur ein Dezimalpunkt)
            if zahl.count('.') > 1:
                raise ValueError(f"Ungültige Zahl bei Position {start_position}: {zahl}")
            tokens.append(Token(TokenTyp.ZAHL, zahl, start_position))
            continue
            
        # Operatoren und Klammern verarbeiten
        if aktuelles_zeichen in ['+', '-', '*', '/', '(', ')']:
            if aktuelles_zeichen == '(':
                token_typ = TokenTyp.KLAMMER_AUF
            elif aktuelles_zeichen == ')':
                token_typ = TokenTyp.KLAMMER_ZU
            elif aktuelles_zeichen == '-':
                # Entscheide ob es ein unärer oder binärer Operator ist
                naechstes_ist_klammer = (
                    aktueller_index + 1 < len(formel) and
                    formel[aktueller_index + 1] == '('
                )
                token_typ = TokenTyp.UNAER if naechstes_ist_klammer else TokenTyp.OPERATOR
            else:
                token_typ = TokenTyp.OPERATOR
            
            tokens.append(Token(token_typ, aktuelles_zeichen, aktueller_index))
            aktueller_index += 1
            continue
            
        # Ungültiges Zeichen gefunden
        raise ValueError(f"Ungültiges Zeichen bei Position {aktueller_index}: {aktuelles_zeichen}")
    
    return tokens