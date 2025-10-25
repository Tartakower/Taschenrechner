from operatoren import Operator

def test_string() -> None:
    assert '+' == str(Operator.PLUS)
    assert '-' == str(Operator.MINUS)
    assert '*' == str(Operator.MULT)
    assert '/' == str(Operator.DIV)

def test_berechne() -> None:
    assert 5.0 == Operator.PLUS.berechne(2.0, 3.0)
    assert -1.0 == Operator.MINUS.berechne(2.0, 3.0)
    assert 6.0 == Operator.MULT.berechne(2.0, 3.0)
    assert 1.5 == Operator.DIV.berechne(3.0, 2.0)