
from baum_knoten import OperatorKnoten, ZahlKnoten, VorzeichenKnoten
from operatoren import Operator

def test_zahl_knoten_wert():
    knoten = ZahlKnoten(42.0)
    assert knoten.berechne_wert() == 42.0
    assert str(knoten) == "42.0"

def test_operator_addition():
    knoten = OperatorKnoten(Operator.PLUS)
    knoten.linker_knoten = ZahlKnoten(5.0)
    knoten.rechter_knoten = ZahlKnoten(3.0)
    assert knoten.berechne_wert() == 8.0
    assert str(knoten) == "(5.0 + 3.0)"

def test_operator_multiplikation():
    knoten = OperatorKnoten(Operator.MULT)
    knoten.linker_knoten = ZahlKnoten(4.0)
    knoten.rechter_knoten = ZahlKnoten(2.0)
    assert knoten.berechne_wert() == 8.0
    assert str(knoten) == "(4.0 * 2.0)"

def test_verschachtelte_berechnung():
    additionsknoten = OperatorKnoten(Operator.PLUS)
    additionsknoten.linker_knoten = ZahlKnoten(1.0)
    additionsknoten.rechter_knoten = ZahlKnoten(2.0)
    
    multiplikationsknoten = OperatorKnoten(Operator.MULT)
    multiplikationsknoten.linker_knoten = additionsknoten
    multiplikationsknoten.rechter_knoten = ZahlKnoten(3.0)
    
    assert multiplikationsknoten.berechne_wert() == 9.0
    assert str(multiplikationsknoten) == "((1.0 + 2.0) * 3.0)"

def test_vorzeichen_knoten():
    innerer = ZahlKnoten(5.0)
    knoten = VorzeichenKnoten(innerer)
    assert knoten.berechne_wert() == -5.0
    assert str(knoten) == "-5.0"
    assert knoten.einfacher_text() == "~"

    knoten = VorzeichenKnoten()
    assert knoten.berechne_wert() == -0.0
    assert str(knoten) == "-0.0"


def test_vorzeichen_mit_operator():
    additionsknoten = OperatorKnoten(Operator.PLUS)
    additionsknoten.linker_knoten = ZahlKnoten(3.0)
    additionsknoten.rechter_knoten = ZahlKnoten(2.0)
    
    vorzeichenknoten = VorzeichenKnoten(additionsknoten)
    assert vorzeichenknoten.berechne_wert() == -5.0
    assert str(vorzeichenknoten) == "-(3.0 + 2.0)"