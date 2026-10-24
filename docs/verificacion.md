# Verificación de la versión 0.3.0

Revisión: 24 de octubre de 2026. Se conservan cinco modelos, uno por fabricante. Se retiraron cuatro variantes Vestas de JSON, GLB y fuentes Blender activas. Los documentos de entrada originales se conservaron.

## Comprobaciones de esta revisión

| Área           | Resultado                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------- |
| Selección      | Cinco modelos; Goldwind, Envision, Gamesa, Nordex y Vestas, sin duplicados                                        |
| Código         | TypeScript y ESLint correctos                                                                                     |
| Datos y assets | Cinco JSON y diez GLB; Draco, animaciones, LOD y componentes correctos                                            |
| Simulación     | Seis pruebas aprobadas, incluida coherencia nominal de Envision (1680 RPM, 118:1)                                 |
| Topología      | Vestas/Gamesa/Envision: una planetaria y dos paralelas; Nordex: dos planetarias y una paralela; Goldwind: directo |
| Navegador      | Cinco modelos y dos cámaras; selección, explosión, pausa, ficha y catálogo correctos                              |
| Formato móvil  | 390 × 844 sin desbordamiento horizontal; cámara adaptada                                                          |
| Condiciones    | Viento fijo de 8 m/s; sin reguladores                                                                             |
| Publicación    | Correcto: GitHub Actions finalizó y web HTTPS verificada                                                          |

La revisión local de producción usó el prefijo /Crear-simulador-e-lico-3D/. La revisión se repitió contra la URL pública y aprobó las cinco máquinas, animación, pausa, selección, explosión, ficha, catálogo y formato móvil sin errores de consola.

## Assets actuales

| Modelo                           | Interior / LOD (KiB) | Triángulos interior / LOD |
| -------------------------------- | -------------------: | ------------------------: |
| Envision EN110 · 2,1 MW          |            535 / 310 |            128408 / 49316 |
| Gamesa G114 · referencia 2,0 MW  |            537 / 311 |            127928 / 49120 |
| Goldwind GW87/1500               |            516 / 271 |             97704 / 34616 |
| Nordex N149 / Delta4000 · 4,8 MW |            519 / 303 |            120320 / 47156 |
| Vestas V110 · 2,0 MW             |            547 / 315 |            131592 / 49552 |

## Precisión y límites

Las fuentes primarias y sus páginas están en [investigación técnica](investigacion-tecnica.md) y cada JSON (`engineering.references`). Las reconstrucciones siguen la estructura documentada de cada familia; no hay planos OEM acotados completos ni certificación as-built por número de serie. El número de dientes, reparto por etapas, posiciones internas y piezas de acabado son ilustrativos.

La transmisión 118:1 y el nominal de 1680 RPM de Envision proceden de su tabla de diseño preliminar. La cinemática simplificada se ancla a ese punto mediante una TSR constante derivada, marcada como supuesto de control. Las otras relaciones 90:1 no se presentan como datos OEM.

Se comprobaron movimiento de la región mecánica y estabilidad al pausar, raycasting, selección por botones, explosión, ficha con referencias, catálogo de cinco filas y formato móvil. No hubo errores de consola en la revisión local de producción. Las capturas por modelo fueron inspeccionadas.

El módulo 3D es diferido, aproximadamente 319,68 kB gzip; aplicación 84,26 kB y CSS 7,26 kB gzip. Vite advierte que el módulo 3D supera 500 kB sin comprimir, pero el build finaliza correctamente. Los decodificadores Draco se sirven localmente.

La revisión de navegador usa Edge con WebGL por software. No se han certificado FPS en teléfonos físicos de gama media ni Safari iOS. Los resultados y capturas temporales están en tmp/qa, ignorado por Git.

## Publicación confirmada

[Aplicación HTTPS](https://javierah306-tech.github.io/Crear-simulador-e-lico-3D/) y [workflow aprobado](https://github.com/javierah306-tech/Crear-simulador-e-lico-3D/actions/runs/40129461568), commit de implementación `6020285`. Los diez GLB publicados coinciden por SHA-256 con los archivos locales finales. Los ocho GLB de las cuatro variantes retiradas responden HTTP 404. La compilación, lint, datos y seis pruebas de simulación se aprobaron en CI.
