# Nueva versión visual y mecánica

La mejora abarca los nueve modelos. Las cuatro imágenes proporcionadas se usan como inspiración de acabado: rodamientos y uniones visibles, generador anular para accionamiento directo, tren con multiplicadora cuando está documentado, bastidor, cableado y equipos auxiliares. No se copian como texturas ni se incorporan a la publicación.

## Dirección visual

La interfaz usa tonos cálidos de arena y cobre junto con verdes ecológicos. La escena conserva materiales diferenciados para carcasas claras, acero, bobinados y equipos eléctricos. Las transiciones entre exterior e interior y hacia la vista de explosión ayudan a seguir las piezas en lugar de cambiar de posición de manera abrupta.

El acabado transmite una aplicación de mayor calidad mediante jerarquía clara, espacio para la escena, información legible y acceso continuo a las funciones educativas. El indicador de operación normal y las métricas calculadas pertenecen a la simulación; no representan telemetría de un parque real.

## Mecánica y animación

- El buje incorpora uniones, anillos de apoyo y mecanismos de paso ilustrativos.
- Los apoyos del eje, las uniones del tren mecánico y los componentes del generador se distinguen con geometría y materiales propios.
- Goldwind representa un generador anular sin multiplicadora, siguiendo la arquitectura documentada de su familia.
- Los modelos con multiplicadora documentada incluyen una transmisión ilustrativa con engranajes y elementos móviles. El V110 distingue una etapa planetaria y dos helicoidales, según la referencia de familia en `vestas_2mw.pdf`, página PDF 6. En Nordex N149 la referencia de familia describe dos etapas planetarias y una cilíndrica. Las disposiciones de las variantes restantes continúan siendo ilustrativas.
- Para las arquitecturas incompletas se conserva una cadena funcional genérica sin afirmar una multiplicadora ni un tipo de generador ausente de la ficha.
- Los GLB incluyen metadatos de movimiento para enlazar la animación de los mecanismos con las RPM estimadas del rotor.
- Las piezas estáticas compatibles se agrupan por componente y material para limitar llamadas de dibujo; exterior e interior tienen niveles de detalle diferentes.

Las cantidades de dientes, disposición de apoyos, bobinados, accesorios y proporciones no son datos OEM. Los movimientos auxiliares se coordinan por relaciones ilustrativas respecto al rotor, sin presentar una relación de transmisión como dato real cuando no está documentada. El escenario mantiene viento fijo, alineación y paso estable bajo operación normal.

## Información protegida

La mejora visual no altera `src/data/models/*.json`, el resumen de fabricantes ni las fuentes primarias. Se mantiene la separación entre **instalado**, **familia**, **no documentado** y **supuesto de simulación**. Las nuevas piezas no completan automáticamente una ficha técnica.

## Revisión de la entrega

La lista de verificaciones, resultados y limitaciones está en [verificacion.md](verificacion.md). La fluidez en un navegador de escritorio no certifica el rendimiento de todos los teléfonos; la validación en dispositivos físicos se mantiene como etapa de optimización.
