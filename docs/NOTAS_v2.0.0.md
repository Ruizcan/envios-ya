# EnvíaYa v2.0.0 · Notas de la versión

**Fecha:** 11 de noviembre de 2026

## Resumen
Versión de mantenimiento mayor: incluye las 7 correcciones de la v1.0.1 y una refactorización
completa de `calc`. Las 56 pruebas de regresión pasan y el camino de `flag` queda omitido
porque ese argumento ya no existe.

## ⚠️ Cambio incompatible
- Se eliminó el parámetro `flag`. Una llamada como `calc(5, "urbana", "normal", 1, flag=True)`
  ahora lanza `TypeError`. **Cómo migrar:** quita `flag=True` e imprime el resultado desde quien llama.

## Mejoras internas
- Patrón Estrategia para las zonas: agregar una zona nueva ya no exige tocar `calcular_costo`.
- Complejidad ciclomática máxima por función: de 15 a 3.
- Aritmética con `Decimal`: se acaban los errores de punto flotante en el redondeo.

## Correcciones incluidas (desde la v1.0.1)
DEF-01 a DEF-07: ver el CHANGELOG.
