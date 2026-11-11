"""Parte 3/5 - Casos de caja negra automatizados (matriz CP-01 ... CP-41)."""
import pytest

from envios import calc
from casos import CASOS, ERROR


@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon, esperado",
    [pytest.param(*c[2:8], id=c[0]) for c in CASOS],
)
def test_caja_negra(peso, zona, cliente, dia, cupon, esperado):
    if esperado == ERROR:
        with pytest.raises(ValueError):
            calc(peso, zona, cliente, dia, cupon)
    else:
        assert calc(peso, zona, cliente, dia, cupon) == esperado


def test_mensaje_peso_invalido():
    """R1: el mensaje del error debe ser exactamente 'peso inválido'."""
    with pytest.raises(ValueError, match="^peso inválido$"):
        calc(0, "urbana", "normal", 1)
