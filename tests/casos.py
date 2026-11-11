"""Casos de prueba de caja negra (Parte 3) con resultados esperados calculados a mano.

Parámetros del estudiante Audi Javier Ruiz Cantillo (código 0182210085):
A=2 B=1 C=0 D=0 E=8 F=5 -> PMAX=40, L1=3 (incluido), L2=10, RR=10 %, RN=50 %,
V=20 %, S=$2.000 (antes de descuentos), cliente y cupón se aplican ambos
(primero cliente), cupón inexistente = error.

Formato: (id, requisito, peso, zona, cliente, dia, cupon, esperado, tecnica)
esperado = int con el costo, o ERROR si debe lanzar ValueError.
"""
ERROR = "ERROR"

CASOS = [
    # --- Valores límite de peso (R1, R3) ---
    ("CP-01", "R1",    0,     "urbana",   "normal",    1, None,      ERROR, "VL peso = 0"),
    ("CP-02", "R1,R3", 0.01,  "urbana",   "normal",    1, None,      6000,  "VL peso justo sobre 0"),
    ("CP-03", "R3",    3,     "urbana",   "normal",    1, None,      6000,  "VL peso = L1 (incluido, D par)"),
    ("CP-04", "R3",    3.01,  "urbana",   "normal",    1, None,      9000,  "VL peso justo sobre L1"),
    ("CP-05", "R3",    10,    "urbana",   "normal",    1, None,      9000,  "VL peso = L2"),
    ("CP-06", "R3,R8", 10.01, "urbana",   "normal",    1, None,      9000,  "VL peso justo sobre L2"),
    ("CP-07", "R1,R3", 40,    "urbana",   "normal",    1, None,      33000, "VL peso = PMAX"),
    ("CP-08", "R1",    40.01, "urbana",   "normal",    1, None,      ERROR, "VL peso justo sobre PMAX"),
    ("CP-09", "R1",    45,    "urbana",   "normal",    1, None,      ERROR, "PE peso > PMAX"),
    ("CP-10", "R1",    -5,    "urbana",   "normal",    1, None,      ERROR, "PE peso negativo"),
    # --- Zona (R2, R4) ---
    ("CP-11", "R3,R4", 15,    "rural",    "normal",    2, None,      14300, "PE zona rural / tramo 3"),
    ("CP-12", "R4",    5,     "nacional", "normal",    3, None,      13500, "PE zona nacional"),
    ("CP-13", "R2",    5,     "maritima", "normal",    1, None,      ERROR, "PE zona inválida"),
    # --- Día (R2, R5) ---
    ("CP-14", "R2",    5,     "urbana",   "normal",    0, None,      ERROR, "VL día = 0"),
    ("CP-15", "R2",    5,     "urbana",   "normal",    8, None,      ERROR, "VL día = 8"),
    ("CP-16", "R5",    2,     "urbana",   "normal",    6, None,      8000,  "VL día = 6 (sábado)"),
    ("CP-17", "R5",    2,     "urbana",   "normal",    7, None,      8000,  "VL día = 7 (domingo)"),
    ("CP-18", "R5",    2,     "urbana",   "normal",    5, None,      6000,  "VL día = 5 (viernes)"),
    # --- Cliente y cupón (R6, R7) ---
    ("CP-19", "R6,R8", 5,     "urbana",   "frecuente", 1, None,      8600,  "PE cliente frecuente (empate $50)"),
    ("CP-20", "R6",    5,     "urbana",   "vip",       1, None,      7200,  "PE cliente vip"),
    ("CP-21", "R6",    5,     "urbana",   "normal",    1, "ENVIO10", 8100,  "PE cupón válido"),
    ("CP-22", "R7",    5,     "urbana",   "normal",    1, "GRATIS",  ERROR, "PE cupón inexistente"),
    # --- Mínimo y redondeo (R8) ---
    ("CP-23", "R8",    2,     "urbana",   "vip",       1, "ENVIO10", 5000,  "VL costo mínimo"),
    ("CP-24", "R8",    11.2,  "urbana",   "normal",    1, None,      10000, "Redondeo hacia arriba"),
    ("CP-25", "R8",    10.5,  "rural",    "normal",    1, None,      10300, "Redondeo hacia abajo"),
    # --- Tabla de decisión cliente x cupón x fin de semana (peso 5, urbana) ---
    ("CP-26", "R5,R6", 5, "urbana", "normal",    1, None,      9000,  "TD-01"),
    ("CP-27", "R5,R6", 5, "urbana", "normal",    6, None,      11000, "TD-02"),
    ("CP-28", "R5,R6", 5, "urbana", "normal",    1, "ENVIO10", 8100,  "TD-03"),
    ("CP-29", "R5,R6", 5, "urbana", "normal",    6, "ENVIO10", 9900,  "TD-04"),
    ("CP-30", "R5,R6", 5, "urbana", "frecuente", 1, None,      8600,  "TD-05"),
    ("CP-31", "R5,R6", 5, "urbana", "frecuente", 6, None,      10500, "TD-06"),
    ("CP-32", "R5,R6", 5, "urbana", "frecuente", 1, "ENVIO10", 7700,  "TD-07"),
    ("CP-33", "R5,R6", 5, "urbana", "frecuente", 6, "ENVIO10", 9400,  "TD-08"),
    ("CP-34", "R5,R6", 5, "urbana", "vip",       1, None,      7200,  "TD-09"),
    ("CP-35", "R5,R6", 5, "urbana", "vip",       6, None,      8800,  "TD-10"),
    ("CP-36", "R5,R6", 5, "urbana", "vip",       1, "ENVIO10", 6500,  "TD-11"),
    ("CP-37", "R5,R6", 5, "urbana", "vip",       6, "ENVIO10", 7900,  "TD-12"),
    ("CP-38", "R7",    5, "urbana", "vip",       6, "XYZ",     ERROR, "TD-13"),
    # --- Combinados (todas las reglas) ---
    ("CP-39", "R3-R8", 3,  "rural",    "vip",       6, "ENVIO10", 6200,  "Combinado"),
    ("CP-40", "R3-R8", 12, "nacional", "frecuente", 7, "ENVIO10", 15300, "Combinado"),
    ("CP-41", "R3-R6,R8", 8, "rural",  "frecuente", 6, None,      11300, "Combinado"),
]
