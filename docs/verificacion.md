# Verificación de la nueva versión

Actualización del 5 de octubre de 2026. Esta página registra evidencias de la nueva versión; los resultados de la base del 4 de octubre no se trasladan automáticamente a los assets o a la interfaz renovados.

## Comprobaciones de la entrega

| Área          | Comprobación                                               | Estado de la nueva versión                 |
| ------------- | ---------------------------------------------------------- | ------------------------------------------ |
| Compilación   | TypeScript y build de Vite                                 | Correcto                                   |
| Código        | ESLint                                                     | Correcto: revisión completa sin errores    |
| Datos         | JSON Schema, IDs únicos, umbrales y viento fijo            | Correcto: nueve registros                  |
| Assets        | GLB v2, Draco, clip de rotor, componentes y arquitectura   | Correcto: dieciocho GLB                    |
| LOD           | Variante reducida y detallada de cada modelo               | Correcto: todos los LOD reducen triángulos |
| Simulación    | Invariantes de potencia, RPM y umbrales                    | Correcto: nueve pruebas aprobadas          |
| Navegador     | Microsoft Edge con WebGL; nueve modelos exterior/interior  | Correcto: revisión completa                |
| Interacción   | Raycasting, botones, explosión, pausa, ficha y catálogo    | Correcto                                   |
| Responsive    | Escritorio y móvil 390 × 844 sin desbordamiento horizontal | Correcto: cámara adaptada a retrato        |
| Condiciones   | Ausencia de reguladores de viento                          | Correcto: sin controles de rango           |
| GitHub        | Subida al repositorio indicado, rama main                  | Correcto: verificado remotamente           |
| Sitio público | GitHub Pages configurado con Actions y HTTPS               | Configurado; despliegue inicial en curso   |

La nueva versión está subida y verificada en [Crear-simulador-e-lico-3D](https://github.com/javierah306-tech/Crear-simulador-e-lico-3D), rama `main`. Primer commit remoto de esta versión: `66de6667634c4a620d31eb422f2b2bd4e52bb0c6`. GitHub Pages está configurado con Actions y HTTPS obligatorio. El despliegue inicial está en curso; todavía no se declara verificada la [URL pública](https://javierah306-tech.github.io/Crear-simulador-e-lico-3D/).

## Compilación y simulación

La compilación de producción y ESLint finalizaron correctamente. Las nueve pruebas de simulación comprueban potencia cero fuera del rango, llegada a nominal, crecimiento de potencia antes de la nominal, RPM acotadas y rechazo de un viento no finito. La interfaz continúa usando el escenario fijo de 8 m/s.

El build separa la aplicación y el visor 3D. Sus tamaños gzip son aproximadamente 82,72 kB para la aplicación, 319,66 kB para el módulo 3D diferido y 7,17 kB para CSS. El módulo 3D supera el umbral orientativo de 500 kB sin comprimir que advierte Vite; el visor se solicita como un módulo separado al montar la escena. El aviso no impide el build.

## Navegador e interacción

La revisión completa en Microsoft Edge con WebGL recorrió los nueve modelos, en exterior e interior, sin errores de consola. Comparó el Canvas antes y después para comprobar movimiento, seleccionó piezas mediante raycasting y botones, abrió y cerró la ficha con sus supuestos, activó la vista de explosión y verificó las nueve filas del catálogo.

Las capturas de escritorio y de móvil a 390 × 844 permiten revisar encuadre y jerarquía visual. En retrato se ajustó la distancia inicial para conservar la máquina dentro del visor. La página no presenta desbordamiento horizontal y no contiene entradas de rango para alterar condiciones. Se revisó el contraste de las métricas sobre la paleta clara.

La animación auxiliar comparte el reloj del mixer glTF para mantener sincronizados los mecanismos. Al pausar, el Canvas trabaja por demanda; la cámara y las interacciones continúan disponibles sin dibujar constantemente un rotor detenido. El flujo de energía ilustra la dirección funcional y no representa telemetría.

La revisión de producción usó la ruta base `/Crear-simulador-e-lico-3D/`, cargó los nueve modelos y contrastó la región central de los mecanismos: cambió durante la animación y permaneció idéntica al pausar. Los assets V110 definitivos coinciden por SHA con las copias de `dist`. No se registraron errores de consola. Esta prueba local con la ruta del repositorio verifica el build; la revisión de la URL pública se registra por separado al terminar el despliegue.

## Assets exportados

El validador revisa cabecera y longitud GLB, chunk JSON, compresión Draco por primitiva, grupos y etiquetas de componentes, mecanismos de paso, un canal real de rotación para `RotorAssembly`, metadatos de movimiento finitos y coherencia de multiplicadora con la ficha. Comprueba que el LOD no tenga más triángulos que el interior. Para V110 verifica además una etapa planetaria y dos helicoidales, etiquetadas con alcance de familia, de acuerdo con la tabla primaria de `vestas_2mw.pdf` p. PDF 6.

| Modelo                           | Interior / exterior (KiB) | Triángulos interior / exterior |
| -------------------------------- | ------------------------: | -----------------------------: |
| Goldwind GW1500-87               |                 347 / 201 |                66 720 / 27 368 |
| Nordex N149 · 4,8 MW             |                 334 / 236 |                80 188 / 37 680 |
| Vestas V110 · 2,0 MW             |                 418 / 268 |                88 620 / 40 408 |
| Vestas V112 · 3,0 MW             |                 334 / 236 |                80 188 / 37 680 |
| Vestas V150 Mk3B · 4,2 MW        |                 334 / 236 |                80 188 / 37 680 |
| Vestas V150 · 4,3 MW             |                 334 / 236 |                80 188 / 37 680 |
| Vestas V136 CP3.6                |                 220 / 139 |                61 624 / 23 756 |
| Envision E110 · 2,1 MW           |                 220 / 139 |                61 624 / 23 756 |
| Gamesa G114 · variante pendiente |                 220 / 139 |                61 624 / 23 756 |

Tamaños redondeados hacia arriba; 1 KiB = 1024 bytes. Son archivos GLB antes de la compresión HTTP. El detalle adicional incluye las uniones, apoyos, carcasas, bastidores y equipos; las arquitecturas incompletas conservan su carácter genérico.

## Alcance y límites

La geometría nueva es original e ilustrativa. No representa un CAD autorizado ni un gemelo por número de serie. La ficha sigue indicando los datos ausentes; las arquitecturas sin documentar no se declaran como accionamiento directo por no dibujar una multiplicadora.

El exterior utiliza el LOD reducido; el interior carga la variante detallada al solicitarla. Draco se sirve localmente. Los materiales evitan la descarga de texturas externas. El módulo 3D se carga de forma diferida. Su descarga inicial y las llamadas de dibujo de los interiores se deben medir en dispositivos físicos para fijar un presupuesto de rendimiento.

No se han medido FPS en un teléfono físico de gama media ni validado Safari iOS. Las pruebas de navegador con renderizado por software permiten revisar carga, interacción y animación, pero no certifican el rendimiento en una GPU móvil. Los registros y capturas intermedios se guardan en `tmp/qa`, ignorado por Git.
