# Identidad visual y mecánica · versión 0.4.0

Los cinco modelos tienen geometrías originales diferenciadas. El selector mantiene exactamente un Goldwind, un Envision, un Gamesa, un Nordex y un Vestas.

- Goldwind conserva el volumen del PMSG anular, sin multiplicadora.
- Envision incorpora envolvente rectangular, franjas del parque La Esperanza y generador con aletas de refrigeración por aire.
- Gamesa incorpora cápsula redondeada, dos apoyos principales y bastidor delantero de fundición.
- Nordex incorpora envolvente ancha, cola roja de referencia, radiadores traseros, dos planetarias y suspensión de tres puntos con un apoyo principal.
- Vestas incorpora nariz y envolvente propias, CoolerTop y disposición compacta del módulo delantero.

Los modelos incluyen cubiertas de buje, apertura traslúcida de carcasas, pedestales del generador, anillos, escobillas estacionarias, freno, cableado y acabados de acero, pintura y cobre. Las formas procedentes de fuentes se distinguen de piezas y cotas interpretadas en [investigación técnica](investigacion-tecnica.md).

Se conservan los dos acercamientos principales, exterior e interior. Una tercera vista **Parque** muestra torre completa, camino y paisaje. Todos los modelos tienen contexto territorial; Nordex ofrece tres parques. Los campos, masas arboladas y lomas se generan con una semilla por sitio, usando instancias de vegetación y geometría moderada. Son paisajes representativos, no reconstrucciones topográficas georreferenciadas.

El escenario mantiene 8 m/s fijos, operación normal y una paleta cálida de verano. La cámara, explosión y animación siguen siendo fluidas mediante GSAP, glTF y un reloj compartido. La pausa detiene mecanismos, flujo y turbinas vecinas. Las transiciones respetan la preferencia de reducir movimiento.

Los JSON ahora almacenan identidad técnica y procedencia del paisaje. Los datos ausentes continúan como `null`; no se completan a partir de piezas dibujadas. Las fotografías recibidas y las fuentes externas se consultan como referencia, sin incorporarlas como texturas. Resultados de las comprobaciones en [verificación](verificacion.md).
