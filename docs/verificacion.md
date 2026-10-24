# Verificación de la versión 0.4.0

Revisión: 24 de octubre de 2026. Cinco modelos activos, con identidad geométrica propia y siete paisajes de parques del Biobío. Los resultados siguientes corresponden a los assets finales de esta revisión.

## Comprobaciones

| Área        | Resultado                                                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Catálogo    | Cinco modelos, uno por fabricante; cinco fuentes Blender y diez GLB                                                                        |
| Código      | TypeScript y ESLint aprobados                                                                                                              |
| Datos       | JSON Schema aprobado; parques con procedencia, sin sitios duplicados y con cobertura de todos los parques de cada modelo                   |
| Mecánica    | Transmisiones documentadas, Draco, animación y LOD correctos; Gamesa con dos apoyos principales y Nordex con uno, contrastados con fuentes |
| Simulación  | Seis pruebas aprobadas, incluida coherencia nominal Envision de 1.680 RPM y 118:1                                                          |
| Navegador   | Cinco modelos en exterior, interior y parque; siete ubicaciones, incluido selector de tres parques Nordex                                  |
| Interacción | Movimiento, estabilidad en pausa, raycasting, selección por botones, explosión, ficha y catálogo aprobados                                 |
| Móvil       | 390 × 844 sin desbordamiento horizontal; controles de cámara y ficha disponibles                                                           |
| Condiciones | Viento fijo de 8 m/s; sin reguladores de condiciones                                                                                       |
| Publicación | Pendiente de actualización de GitHub Pages para esta revisión                                                                              |

La revisión local de producción usó el prefijo `/Crear-simulador-e-lico-3D/`, Edge y WebGL por software. No hubo errores de consola. Se inspeccionaron las capturas de los cinco modelos y los paisajes; los resultados temporales están en `tmp/qa`, ignorado por Git. Los GLB se solicitan con versión de recurso para evitar reutilizar geometrías antiguas en caché.

## Assets finales

| Modelo                           | Interior / LOD (KiB) | Triángulos interior / LOD |
| -------------------------------- | -------------------: | ------------------------: |
| Envision EN110 · 2,1 MW          |            462 / 268 |            106878 / 39650 |
| Gamesa G114 · referencia 2,0 MW  |            420 / 259 |             94238 / 37670 |
| Goldwind GW87/1500               |            500 / 257 |             95342 / 32918 |
| Nordex N149 / Delta4000 · 4,8 MW |            436 / 264 |             98308 / 37060 |
| Vestas V110 · 2,0 MW             |            426 / 259 |             97194 / 37406 |

Los modelos exterior/parque usan el LOD reducido y el interior carga su GLB detallado. El módulo 3D es diferido: aproximadamente 325 kB gzip; interfaz 87 kB y CSS 7,64 kB gzip. Vite advierte que el módulo 3D supera 500 kB sin comprimir; la compilación finaliza correctamente. Draco se sirve localmente y la vegetación usa instancias.

## Precisión y límites

Las diferencias de forma, apoyos, transmisión y refrigeración se describen con sus fuentes en [investigación técnica](investigacion-tecnica.md). Las reconstrucciones se basan en referencias de familia y fotografías; no se dispone de planos OEM acotados completos ni acreditación as-built por número de serie. El número de dientes, cotas internas y ubicación de auxiliares no documentados se interpretan. La cola roja Nordex sigue una fotografía oficial de N149 y no certifica la pintura de cada unidad chilena.

Los siete paisajes interpretan el contexto rural y bioma de las comunas documentadas. No usan levantamiento topográfico, parcelas exactas ni coordenadas individuales. Las fuentes y el alcance son consultables dentro de cada escena.

Se conserva la discrepancia de variante/potencia de Las Peñas. La transmisión Envision 118:1 y nominal 1.680 RPM vienen de una tabla de diseño preliminar; la ley de control usada para estimar RPM es un supuesto explícito. Las demás relaciones 90:1 permanecen ilustrativas.

No se han certificado FPS en teléfonos físicos de gama media ni Safari iOS. La prueba de escritorio con WebGL por software confirma funcionalidad, no garantiza rendimiento de todos los dispositivos.
