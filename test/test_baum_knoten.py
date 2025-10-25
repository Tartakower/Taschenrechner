import pytest
from src.baum_knoten import Operatorknoten, Zahlknoten, Vorzeichenknoten, Rechenbaum
from src.operatoren import Operator

def test_zahl_knoten_wert():
    knoten = Zahlknoten(42.0)
    assert knoten.berechne_wert() == 42.0
    assert str(knoten) == "42.0"

def test_operator_addition():
    knoten = Operatorknoten(Operator.PLUS)
    knoten.linker_knoten = Zahlknoten(5.0)
    knoten.rechter_knoten = Zahlknoten(3.0)
    assert knoten.berechne_wert() == 8.0
    assert str(knoten) == "(5.0 + 3.0)"

def test_operator_multiplikation():
    knoten = Operatorknoten(Operator.MULT)
    knoten.linker_knoten = Zahlknoten(4.0)
    knoten.rechter_knoten = Zahlknoten(2.0)
    assert knoten.berechne_wert() == 8.0
    assert str(knoten) == "(4.0 * 2.0)"

def test_verschachtelte_berechnung():
    additionsknoten = Operatorknoten(Operator.PLUS)
    additionsknoten.linker_knoten = Zahlknoten(1.0)
    additionsknoten.rechter_knoten = Zahlknoten(2.0)
    
    multiplikationsknoten = Operatorknoten(Operator.MULT)
    multiplikationsknoten.linker_knoten = additionsknoten
    multiplikationsknoten.rechter_knoten = Zahlknoten(3.0)
    
    assert multiplikationsknoten.berechne_wert() == 9.0
    assert str(multiplikationsknoten) == "((1.0 + 2.0) * 3.0)"

def test_vorzeichen_knoten():
    innerer = Zahlknoten(5.0)
    knoten = Vorzeichenknoten(innerer)
    assert knoten.berechne_wert() == -5.0
    assert str(knoten) == "-5.0"
    assert knoten.einfacher_text() == "~"

    knoten = Vorzeichenknoten()
    assert knoten.berechne_wert() == -0.0
    assert str(knoten) == "-0.0"


def test_vorzeichen_mit_operator():
    additionsknoten = Operatorknoten(Operator.PLUS)
    additionsknoten.linker_knoten = Zahlknoten(3.0)
    additionsknoten.rechter_knoten = Zahlknoten(2.0)
    
    vorzeichenknoten = Vorzeichenknoten(additionsknoten)
    assert vorzeichenknoten.berechne_wert() == -5.0
    assert str(vorzeichenknoten) == "-(3.0 + 2.0)"


def test_rechenbaum_standard():
    baum = Rechenbaum()
    assert baum.berechne_wert() == 0.0
    assert str(baum) == "0.0"

def test_rechenbaum_set_wurzel():
    baum = Rechenbaum()
    neuer_knoten = Zahlknoten(42.0)
    baum.wurzel = neuer_knoten
    assert baum.berechne_wert() == 42.0
    assert str(baum) == "42.0"

def test_rechenbaum_komplexer_ausdruck():
    baum = Rechenbaum()
    
    # Baue (3 + 4) * 2
    plus_knoten = Operatorknoten(Operator.PLUS)
    plus_knoten.linker_knoten = Zahlknoten(3.0)
    plus_knoten.rechter_knoten = Zahlknoten(4.0)
    
    mal_knoten = Operatorknoten(Operator.MULT)
    mal_knoten.linker_knoten = plus_knoten
    mal_knoten.rechter_knoten = Zahlknoten(2.0)
    
    baum.wurzel = mal_knoten
    assert baum.berechne_wert() == 14.0
    assert str(baum) == "((3.0 + 4.0) * 2.0)"
    assert baum.einfacher_text() == "*"

def test_rechenbaum_ohne_wurzel():
    baum = Rechenbaum()
    assert baum.berechne_wert() == 0.0