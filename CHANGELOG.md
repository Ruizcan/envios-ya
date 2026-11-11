# Changelog
Todos los cambios importantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto sigue [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [1.0.1] - 2026-11-11
### Fixed
- DEF-01: el peso máximo era 50 kg fijo; ahora es PMAX = 40 kg (R1).
- DEF-02: una zona inválida no lanzaba error; ahora lanza `ValueError("zona inválida")` (R2).
- DEF-03: un día fuera de 1–7 no lanzaba error; ahora lanza `ValueError("día inválido")` (R2).
- DEF-04: el sábado no cobraba el recargo de fin de semana (`d > 6` → `d >= 6`) (R5).
- DEF-05: un cupón inexistente se ignoraba; ahora lanza `ValueError("cupón inválido")` (R7).
- DEF-06: el redondeo truncaba (`int(t/100)*100`); ahora redondea al $100 más cercano, $50 hacia arriba (R8).
- DEF-07: el mensaje de error decía "peso invalido" en lugar de "peso inválido" (R1).
### Added
- Suite de pruebas pytest: 41 casos de caja negra, 15 caminos de caja blanca y la prueba del mensaje de error.

## [1.0.0] - 2026-11-11
### Added
- Código heredado de EnvíaYa con `CONFIG` diligenciado según el código estudiantil 0182210085.

[Unreleased]: ../../compare/v1.0.1...HEAD
[1.0.1]: ../../compare/v1.0.0...v1.0.1
[1.0.0]: ../../releases/tag/v1.0.0
