import pytest
from src.tokenizer import tokenize, Token, TokenTyp

def test_einfache_zahl():
    tokens = tokenize("42")
    assert len(tokens) == 1
    assert tokens[0] == Token(TokenTyp.ZAHL, "42", 0)

def test_dezimalzahl():
    tokens = tokenize("3.14")
    assert len(tokens) == 1
    assert tokens[0] == Token(TokenTyp.ZAHL, "3.14", 0)

def test_ungueltige_dezimalzahl():
    with pytest.raises(ValueError):
        tokenize("3.14.15")

def test_einfache_addition():
    tokens = tokenize("2 + 3")
    assert len(tokens) == 3
    assert tokens[0] == Token(TokenTyp.ZAHL, "2", 0)
    assert tokens[1] == Token(TokenTyp.OPERATOR, "+", 2)
    assert tokens[2] == Token(TokenTyp.ZAHL, "3", 4)

def test_ohne_leerzeichen():
    tokens = tokenize("2+3")
    assert len(tokens) == 3
    assert tokens[0] == Token(TokenTyp.ZAHL, "2", 0)
    assert tokens[1] == Token(TokenTyp.OPERATOR, "+", 1)
    assert tokens[2] == Token(TokenTyp.ZAHL, "3", 2)

def test_mit_klammern():
    tokens = tokenize("(2 + 3) * 4")
    assert len(tokens) == 7
    assert tokens[0] == Token(TokenTyp.KLAMMER_AUF, "(", 0)
    assert tokens[1] == Token(TokenTyp.ZAHL, "2", 1)
    assert tokens[2] == Token(TokenTyp.OPERATOR, "+", 3)
    assert tokens[3] == Token(TokenTyp.ZAHL, "3", 5)
    assert tokens[4] == Token(TokenTyp.KLAMMER_ZU, ")", 6)
    assert tokens[5] == Token(TokenTyp.OPERATOR, "*", 8)
    assert tokens[6] == Token(TokenTyp.ZAHL, "4", 10)

def test_ungueltige_zeichen():
    with pytest.raises(ValueError):
        tokenize("2 + a")

def test_komplexer_ausdruck():
    tokens = tokenize("1 + 2 * 3 - 4 / 5")
    assert len(tokens) == 9
    assert [t.typ for t in tokens] == [
        TokenTyp.ZAHL,
        TokenTyp.OPERATOR,
        TokenTyp.ZAHL,
        TokenTyp.OPERATOR,
        TokenTyp.ZAHL,
        TokenTyp.OPERATOR,
        TokenTyp.ZAHL,
        TokenTyp.OPERATOR,
        TokenTyp.ZAHL
    ]

def test_negative_zahl():
    tokens = tokenize("-42")
    assert len(tokens) == 1
    assert tokens[0] == Token(TokenTyp.ZAHL, "-42", 0)

def test_negative_dezimalzahl():
    tokens = tokenize("-3.14")
    assert len(tokens) == 1
    assert tokens[0] == Token(TokenTyp.ZAHL, "-3.14", 0)

def test_ausdruck_mit_negativer_zahl():
    tokens = tokenize("2 * -3")
    assert len(tokens) == 3
    assert tokens[0] == Token(TokenTyp.ZAHL, "2", 0)
    assert tokens[1] == Token(TokenTyp.OPERATOR, "*", 2)
    assert tokens[2] == Token(TokenTyp.ZAHL, "-3", 4)

def test_subtraktion():
    tokens = tokenize("5 - 3")
    assert len(tokens) == 3
    assert tokens[0] == Token(TokenTyp.ZAHL, "5", 0)
    assert tokens[1] == Token(TokenTyp.OPERATOR, "-", 2)
    assert tokens[2] == Token(TokenTyp.ZAHL, "3", 4)

def test_negative_klammer():
    tokens = tokenize("-(2 + 3)")
    assert len(tokens) == 6
    assert tokens[0] == Token(TokenTyp.UNAER, "-", 0)
    assert tokens[1] == Token(TokenTyp.KLAMMER_AUF, "(", 1)
    assert tokens[2] == Token(TokenTyp.ZAHL, "2", 2)
    assert tokens[3] == Token(TokenTyp.OPERATOR, "+", 4)
    assert tokens[4] == Token(TokenTyp.ZAHL, "3", 6)
    assert tokens[5] == Token(TokenTyp.KLAMMER_ZU, ")", 7)

def test_negative_klammer_in_ausdruck():
    tokens = tokenize("4 * -(1 + 2)")
    assert len(tokens) == 8
    assert tokens[0] == Token(TokenTyp.ZAHL, "4", 0)
    assert tokens[1] == Token(TokenTyp.OPERATOR, "*", 2)
    assert tokens[2] == Token(TokenTyp.UNAER, "-", 4)
    assert tokens[3] == Token(TokenTyp.KLAMMER_AUF, "(", 5)
    assert tokens[4] == Token(TokenTyp.ZAHL, "1", 6)
    assert tokens[5] == Token(TokenTyp.OPERATOR, "+", 8)
    assert tokens[6] == Token(TokenTyp.ZAHL, "2", 10)
    assert tokens[7] == Token(TokenTyp.KLAMMER_ZU, ")", 11)

def test_mehrere_operatoren():
    tokens = tokenize("3 + -4 * -5")
    assert len(tokens) == 5
    assert tokens[0] == Token(TokenTyp.ZAHL, "3", 0)
    assert tokens[1] == Token(TokenTyp.OPERATOR, "+", 2)
    assert tokens[2] == Token(TokenTyp.ZAHL, "-4", 4)
    assert tokens[3] == Token(TokenTyp.OPERATOR, "*", 7)
    assert tokens[4] == Token(TokenTyp.ZAHL, "-5", 9)