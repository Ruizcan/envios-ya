"""Parte 4/5 - Un caso por cada camino independiente del grafo de flujo de calc (V(G) = 15)."""
import inspect

import pytest

from envios import calc

CAMINOS = [
    # id,   peso, zona,      cliente,     dia, cupon,     esperado
    ("C01", 5,  "urbana",   "normal",    1, None,      9000),
    ("C02", 0,  "urbana",   "normal",    1, None,      ValueError),
    ("C03", 60, "urbana",   "normal",    1, None,      ValueError),
    ("C04", 2,  "urbana",   "normal",    1, None,      6000),
    ("C05", 15, "urbana",   "normal",    1, None,      13000),
    ("C06", 5,  "rural",    "normal",    1, None,      9900),
    ("C07", 5,  "nacional", "normal",    1, None,      13500),
    ("C08", 5,  "x",        "normal",    1, None,      ValueError),
    ("C09", 5,  "urbana",   "normal",    7, None,      11000),
    ("C10", 5,  "urbana",   "frecuente", 1, None,      8600),
    ("C11", 5,  "urbana",   "vip",       1, None,      7200),
    ("C12", 5,  "urbana",   "normal",    1, "X",       ValueError),
    ("C13", 5,  "urbana",   "normal",    1, "ENVIO10", 8100),
    ("C14", 2,  "urbana",   "vip",       1, "ENVIO10", 5000),
]


@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon, esperado",
    [pytest.param(*c[1:], id=c[0]) for c in CAMINOS],
)
def test_camino(peso, zona, cliente, dia, cupon, esperado):
    if esperado is ValueError:
        with pytest.raises(ValueError):
            calc(peso, zona, cliente, dia, cupon)
    else:
        assert calc(peso, zona, cliente, dia, cupon) == esperado


def test_camino_C15_flag(capsys):
    """Camino 15: flag=True imprime el costo. En la versión 2.0.0 se eliminó flag."""
    if "flag" not in inspect.signature(calc).parameters:
        pytest.skip("Camino eliminado en la refactorización: se quitó el argumento flag")
    assert calc(5, "urbana", "normal", 1, flag=True) == 9000
    assert "costo:" in capsys.readouterr().out
