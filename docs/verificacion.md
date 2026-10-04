# Verificación de la base funcional

Verificación local realizada el 4 de octubre de 2026.

- TypeScript y compilación de producción con Vite: correctos.
- ESLint: sin errores en código propio; se excluyen los decodificadores Draco de terceros.
- JSON Schema y assets: nueve registros validados, IDs únicos, viento fijo dentro del rango, umbrales coherentes y dieciocho GLB válidos.
- glTF: animación de rotor, extensión Draco obligatoria y multiplicadora presente solo cuando el catálogo la documenta. Dos niveles de geometría por modelo.
- Fórmulas: nueve pruebas, una por modelo; potencia cero bajo arranque y desde corte, nominal alcanzada, curva monótona dentro del rango, RPM acotadas, viento no finito rechazado.
- Navegador: Microsoft Edge con WebGL; exterior, interior, cambio de modelo, ficha, catálogo, selección por botones, raycasting, explosión y animación. Revisadas capturas de escritorio 1440 × 1050 y móvil 390 × 844. Sin desbordamiento horizontal ni reguladores de viento.

Los archivos GLB pesan aproximadamente 80–177 KB cada uno, antes del gzip del servidor. Las piezas usan colores de material y no necesitan texturas KTX2. El decodificador Draco se sirve localmente. La biblioteca 3D se carga como un módulo diferido; Vite advierte que ese módulo supera 500 KB sin comprimir. El aviso no impide compilar, pero el rendimiento y tiempo de arranque se deben medir en equipos móviles reales antes de la publicación final.

No se midieron FPS en un teléfono físico de gama media ni se comprobó Safari iOS. No se ha ejecutado el workflow en un repositorio remoto ni existe todavía una URL pública. Las capturas y registros intermedios están en `tmp/qa`, ignorado por Git.
