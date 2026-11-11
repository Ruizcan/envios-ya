"""envios.py - Cálculo del costo de un envío de EnvíaYa (versión 2.0.0).

Especificación personalizada: Audi Javier Ruiz Cantillo, código 0182210085
(A=2 B=1 C=0 D=0 E=8 F=5).
"""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

# ----------------------------------------------------------------------------
# Constantes del negocio (antes eran números mágicos o el diccionario CONFIG)
# ----------------------------------------------------------------------------
PESO_MAXIMO_KG = Decimal("40")          # R1: PMAX = 30 + 5*A
LIMITE_TRAMO_1_KG = Decimal("3")        # R3: L1 = 2 + (B mod 3); D par -> incluido
LIMITE_TRAMO_2_KG = Decimal("10")       # R3: L2 = 10 + C
TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
TARIFA_POR_KG_EXTRA = Decimal("800")

RECARGO_RURAL = Decimal("0.10")         # R4: RR = 10 + 5*(E mod 4) %
RECARGO_NACIONAL = Decimal("0.50")      # R4: RN = 40 + 5*(F mod 3) %

DIA_MINIMO, DIA_MAXIMO = 1, 7           # R2
DIAS_FIN_DE_SEMANA = (6, 7)             # R5: sábado y domingo
RECARGO_FIN_DE_SEMANA = Decimal("2000")  # R5: S = 2000 + 500*(C mod 4), antes de descuentos

DESCUENTOS_CLIENTE = {                  # R6: V = 10 + 5*(A mod 3) %
    "normal": Decimal("0"),
    "frecuente": Decimal("0.05"),
    "vip": Decimal("0.20"),
}
CUPONES = {"ENVIO10": Decimal("0.10")}  # R6/R7

COSTO_MINIMO = Decimal("5000")          # R8
MULTIPLO_REDONDEO = Decimal("100")      # R8


# ----------------------------------------------------------------------------
# Patrón Estrategia: recargo por zona (R4)
# ----------------------------------------------------------------------------
class EstrategiaZona(ABC):
    """Interfaz común: cada zona sabe cómo aplicar su recargo a la tarifa."""

    @abstractmethod
    def aplicar_recargo(self, tarifa: Decimal) -> Decimal:
        ...


class ZonaUrbana(EstrategiaZona):
    def aplicar_recargo(self, tarifa: Decimal) -> Decimal:
        return tarifa


class ZonaRural(EstrategiaZona):
    def aplicar_recargo(self, tarifa: Decimal) -> Decimal:
        return tarifa * (1 + RECARGO_RURAL)


class ZonaNacional(EstrategiaZona):
    def aplicar_recargo(self, tarifa: Decimal) -> Decimal:
        return tarifa * (1 + RECARGO_NACIONAL)


ESTRATEGIAS_ZONA = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


# ----------------------------------------------------------------------------
# Funciones extraídas
# ----------------------------------------------------------------------------
def validar_peso(peso: Decimal) -> None:
    if not (0 < peso <= PESO_MAXIMO_KG):
        raise ValueError("peso inválido")


def validar_dia(dia: int) -> None:
    if not (DIA_MINIMO <= dia <= DIA_MAXIMO):
        raise ValueError("día inválido")


def obtener_estrategia_zona(zona: str) -> EstrategiaZona:
    if zona not in ESTRATEGIAS_ZONA:
        raise ValueError("zona inválida")
    return ESTRATEGIAS_ZONA[zona]


def obtener_descuento_cupon(cupon) -> Decimal:
    if cupon is None:
        return Decimal("0")
    if cupon not in CUPONES:  # F impar: un cupón que no existe es error
        raise ValueError("cupón inválido")
    return CUPONES[cupon]


def calcular_tarifa_base(peso: Decimal) -> Decimal:
    if peso <= LIMITE_TRAMO_1_KG:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2_KG:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2_KG) * TARIFA_POR_KG_EXTRA


def es_fin_de_semana(dia: int) -> bool:
    return dia in DIAS_FIN_DE_SEMANA


def aplicar_descuento(costo: Decimal, porcentaje: Decimal) -> Decimal:
    return costo * (1 - porcentaje)


def redondear_a_cien(costo: Decimal) -> int:
    centenas = (costo / MULTIPLO_REDONDEO).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(centenas * MULTIPLO_REDONDEO)


# ----------------------------------------------------------------------------
# Función pública
# ----------------------------------------------------------------------------
def calcular_costo(peso, zona, cliente, dia, cupon=None) -> int:
    """Devuelve el costo del envío en pesos, según R1-R8."""
    peso = Decimal(str(peso))
    validar_peso(peso)
    estrategia_zona = obtener_estrategia_zona(zona)
    validar_dia(dia)
    descuento_cupon = obtener_descuento_cupon(cupon)

    costo = estrategia_zona.aplicar_recargo(calcular_tarifa_base(peso))
    if es_fin_de_semana(dia):                     # E par: antes de los descuentos
        costo += RECARGO_FIN_DE_SEMANA
    # B impar: se aplican ambos, primero el del cliente y luego el cupón
    costo = aplicar_descuento(costo, DESCUENTOS_CLIENTE.get(cliente, Decimal("0")))
    costo = aplicar_descuento(costo, descuento_cupon)
    return redondear_a_cien(max(costo, COSTO_MINIMO))


# Alias para no romper a quien ya llamaba calc(p, z, c, d, cup)
calc = calcular_costo
