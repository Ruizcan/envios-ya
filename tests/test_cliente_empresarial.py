"""Parte 8 - Solicitud de cambio CR-01 (cliente empresarial). Escritas ANTES de implementar.

CR-01: nuevo tipo de cliente "empresarial" con 12 % de descuento. Si el peso es
mayor que L2 (10 kg), el recargo de zona no se cobra.
Supuesto documentado: la exención del recargo de zona aplica solo al cliente
empresarial (la solicitud la describe como parte del nuevo tipo de cliente).
"""
import pytest

from envios import calc

CASOS_CR = [
    # id,     peso,  zona,       cliente,       dia, cupon,     esperado
    ("CE-01", 5,     "urbana",   "empresarial", 1, None,      7900),
    ("CE-02", 5,     "rural",    "empresarial", 1, None,      8700),
    ("CE-03", 10,    "nacional", "empresarial", 1, None,      11900),
    ("CE-04", 10.01, "nacional", "empresarial", 1, None,      7900),
    ("CE-05", 15,    "rural",    "empresarial", 6, None,      13200),
    ("CE-06", 15,    "rural",    "empresarial", 6, "ENVIO10", 11900),
    ("CE-07", 15,    "rural",    "vip",         1, None,      11400),
    ("CE-08", 2,     "urbana",   "empresarial", 1, "ENVIO10", 5000),
]


@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon, esperado",
    [pytest.param(*c[1:], id=c[0]) for c in CASOS_CR],
)
def test_cliente_empresarial(peso, zona, cliente, dia, cupon, esperado):
    assert calc(peso, zona, cliente, dia, cupon) == esperado


def test_empresarial_con_zona_invalida_sigue_siendo_error():
    with pytest.raises(ValueError):
        calc(15, "insular", "empresarial", 1)
