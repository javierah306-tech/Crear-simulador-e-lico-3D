# Modelos y proveedores del Biobío

Fuente base: 02_PARQUES_COMPONENTES_BIOBIO.pdf, Smartwind v1.0, corte documental 03-10-2026. Corpus activo: Goldwind 1,5 MW, Vestas 2 MW, Nordex N149, Coener/Coordinador, Flender/Winergy y documentación OEM Gamesa. Se conserva el nivel de evidencia del informe; las referencias Bxx son las de ese informe, complementadas por referencias técnicas enlazadas en cada JSON.

El catálogo seleccionado registra cinco modelos, uno por fabricante; revisión complementaria de fuentes primarias el 24-10-2026. No es un censo actualizado ni una certificación por número de serie. Se usa el Biobío actual.

## Fabricantes, suministro y parques

| Fabricante / modelo              | Potencia unitaria documentada | Parque(s)                    | Evidencia                                                         | Proveedor de instalación mencionado           |
| -------------------------------- | ----------------------------- | ---------------------------- | ----------------------------------------------------------------- | --------------------------------------------- |
| Envision EN110 · 2,1 MW          | 2.1 [parque]                  | La Esperanza                 | La Esperanza: B B03,B16                                           | La Esperanza: Tecnorenova                     |
| Gamesa G114 · referencia 2,0 MW  | 2 [familia]                   | Las Peñas                    | Las Peñas: B B17,B18                                              | Las Peñas: CJR Renewables                     |
| Goldwind GW87/1500               | 1.5 [parque]                  | Cuel                         | Cuel: A B01                                                       | No documentado                                |
| Nordex N149 / Delta4000 · 4,8 MW | 4.8 [parque]                  | Alena, Los Olmos, Mesamavida | Alena: B B03,B06; Los Olmos: A/B B07,B08; Mesamavida: A/B B09,B10 | Los Olmos: Greenwork; Mesamavida: Tecnorenova |
| Vestas V110 · 2,0 MW             | 2 [parque]                    | Los Buenos Aires             | Los Buenos Aires: A B14,B20                                       | No documentado                                |

Fabricante, operador e instalador son roles distintos. «Proveedor» se entrega como fabricante identificado; el corpus no demuestra un contratista de suministro independiente para todos los parques. Tecnorenova/Greenwork/CJR son referencias de instalación, no fabricantes.

## Datos técnicos extraídos

Cada valor incluye su alcance. Ausencia de un dato no se reemplaza por la cifra de otra variante. Alturas de torre se conservan por parque.

### Geometría y arquitectura

| Modelo                    | Rotor (m)       | Buje instalado (m) | Palas          | Generador                                                              | Multiplicadora | Control         |
| ------------------------- | --------------- | ------------------ | -------------- | ---------------------------------------------------------------------- | -------------- | --------------- |
| EN110 · 2,1 MW            | 110 [familia]   | 100 [familia]      | 3 [familia]    | DFIG · inducción doblemente alimentada, refrigerada por aire [familia] | Sí [familia]   | pitch [familia] |
| G114 · referencia 2,0 MW  | 114 [familia]   | No documentado     | 3 [familia]    | DFIG · inducción doblemente alimentada [familia]                       | Sí [familia]   | pitch [familia] |
| GW87/1500                 | 87 [familia]    | No documentado     | 3 [familia]    | PMSG · síncrono de imanes permanentes [familia]                        | No [familia]   | pitch [familia] |
| N149 / Delta4000 · 4,8 MW | 149.1 [familia] | No documentado     | No documentado | DFIG · asíncrono doblemente alimentado [familia]                       | Sí [familia]   | pitch [familia] |
| V110 · 2,0 MW             | 110 [familia]   | No documentado     | 3 [familia]    | DFIG · doblemente alimentado con anillos rozantes [familia]            | Sí [familia]   | pitch [familia] |

### Umbrales de operación y conversión

| Modelo                    | Arranque (m/s) | Nominal (m/s)  | Corte (m/s)    | Convertidor                      |
| ------------------------- | -------------- | -------------- | -------------- | -------------------------------- |
| EN110 · 2,1 MW            | 3 [familia]    | 9.5 [familia]  | 20 [familia]   | IGBT PWM [familia]               |
| G114 · referencia 2,0 MW  | No documentado | No documentado | No documentado | No documentado                   |
| GW87/1500                 | 3 [familia]    | 9.9 [familia]  | 22 [familia]   | Escala completa (IGBT) [familia] |
| N149 / Delta4000 · 4,8 MW | 3 [familia]    | No documentado | 20 [familia]   | No documentado                   |
| V110 · 2,0 MW             | 3 [familia]    | No documentado | 21 [familia]   | No documentado                   |

### Alcance de las cinco fichas

Envision: el informe del parque incluye una tabla de diseño preliminar; el comunicado OEM anuncia buje de 100 m, no una medición as-built. Gamesa: la referencia G114-2.0 no resuelve la discrepancia de Las Peñas. Vestas: las alturas comerciales no se asignan a Los Buenos Aires. Nordex y Goldwind: se distinguen parámetros de familia de la configuración instalada.

La documentación complementaria y los esquemas consultados se enlazan en investigacion-tecnica.md y engineering.references. No se deducen especificaciones del nombre de los modelos.

## Trazabilidad por campo

### Envision EN110 · 2,1 MW

- P nominal (MW): 2.1 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): 110 [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Buje instalado (m): 100 [familia]. Envision, comunicado del pedido La Esperanza, 10-09-2015. Altura contratada anunciada por el fabricante; no es una medición de campo.
- Palas: 3 [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Generador: DFIG · inducción doblemente alimentada, refrigerada por aire [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Multiplicadora: Sí [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Control: pitch [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Arranque (m/s): 3 [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Nominal (m/s): 9.5 [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Corte (m/s): 20 [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.
- Convertidor: IGBT PWM [familia]. Coener / Coordinador Eléctrico, La Esperanza, Rev. 1 (2019), p. PDF 8, tabla 3 de diseño preliminar. Especificación de diseño preliminar incluida en el informe del parque; no sustituye planos as-built.

- La documentación de La Esperanza confirma arquitectura DFIG con multiplicadora, diámetro, tres palas y umbrales de diseño preliminar.
- El esquema Winergy PEAB es una referencia de familia; no confirma el proveedor de cada máquina instalada.
- La tabla de diseño indica inclinación de eje de 6° y cono de 2,6°. No se aplica una inclinación visual independiente del tren común sin planos acotados.
- El informe cita 0,6 kV/23 kV y tabla eléctrica de 690 V. Se mantienen ambos antecedentes sin conciliarlos artificialmente.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- Dimensiones internas, número de dientes y distribución exacta de armarios son aproximaciones visuales sin planos acotados.
- Relación total de diseño 118:1; reparto por etapas y número de dientes ilustrativos.
- Diámetros de rotor y altura visual mantienen una escala común; alturas no documentadas continúan como supuestos de 100 m.
- TSR constante 8.6317 derivada del punto de diseño 1680 RPM / 118:1 a 9,5 m/s y rotor 110 m. Es una aproximación del control, no su curva OEM.

### Gamesa G114 · referencia 2,0 MW

- P nominal (MW): 2 [familia]. Gamesa G114-2.0 MW, folleto OEM marzo 2012, pp. PDF 1–2, archivo NY DPS. Referencia de familia G114-2.0 MW; no resuelve la variante ni potencia instalada de Las Peñas.
- Rotor (m): 114 [familia]. Gamesa G114-2.0 MW, folleto OEM marzo 2012, pp. PDF 1–2, archivo NY DPS. Referencia de familia G114-2.0 MW; no resuelve la variante ni potencia instalada de Las Peñas.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: 3 [familia]. Gamesa G114-2.0 MW, folleto OEM marzo 2012, pp. PDF 1–2, archivo NY DPS. Referencia de familia G114-2.0 MW; no resuelve la variante ni potencia instalada de Las Peñas.
- Generador: DFIG · inducción doblemente alimentada [familia]. Gamesa G114-2.0 MW, folleto OEM marzo 2012, pp. PDF 1–2, archivo NY DPS. Referencia de familia G114-2.0 MW; no resuelve la variante ni potencia instalada de Las Peñas.
- Multiplicadora: Sí [familia]. Gamesa G114-2.0 MW, folleto OEM marzo 2012, pp. PDF 1–2, archivo NY DPS. Referencia de familia G114-2.0 MW; no resuelve la variante ni potencia instalada de Las Peñas.
- Control: pitch [familia]. Gamesa G114-2.0 MW, folleto OEM marzo 2012, pp. PDF 1–2, archivo NY DPS. Referencia de familia G114-2.0 MW; no resuelve la variante ni potencia instalada de Las Peñas.
- Arranque (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Convertidor: No documentado. Sin fuente específica. No consta en los documentos disponibles.

- Geometría de referencia: G114-2.0 MW. El informe original identifica G114/2000, pero 8,4 MW para cuatro unidades no permite certificar esa variante instalada en Las Peñas.
- Tres etapas documentadas: una planetaria y dos paralelas; relaciones individuales y relación total 90:1 son ilustrativas.
- Las torres comerciales 93/120/140 m no acreditan altura instalada. No se transfieren datos de la G114-2.1 MW.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- cutInMS=3: supuesto para animación; dato documental ausente.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- cutOutMS=20: supuesto para animación; dato documental ausente.
- Dimensiones internas, número de dientes y distribución exacta de armarios son aproximaciones visuales sin planos acotados.
- Relación total 90:1 elegida para visualizar el movimiento; no es una relación OEM confirmada.
- Diámetros de rotor y altura visual mantienen una escala común; alturas no documentadas continúan como supuestos de 100 m.

### Goldwind GW87/1500

- P nominal (MW): 1.5 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): 87 [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: 3 [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Generador: PMSG · síncrono de imanes permanentes [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Multiplicadora: No [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Control: pitch [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Arranque (m/s): 3 [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Nominal (m/s): 9.9 [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Corte (m/s): 22 [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.
- Convertidor: Escala completa (IGBT) [familia]. Goldwind 1.5 MW, tabla de datos p. PDF 6 [B19]. Referencia de familia; no certifica la revisión instalada.

- GW1500-87 es la denominación del parque; GW 87/1500 es la nomenclatura del folleto.
- La altura instalada de Cuel no consta en el corpus.
- El corte OEM identifica estator, rotor PM, buje, bancada y grúa auxiliar. El paso emplea correa y la refrigeración del generador es pasiva.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- Dimensiones internas, número de dientes y distribución exacta de armarios son aproximaciones visuales sin planos acotados.
- Relación total de diseño 1:1; reparto por etapas y número de dientes ilustrativos.
- Diámetros de rotor y altura visual mantienen una escala común; alturas no documentadas continúan como supuestos de 100 m.

### Nordex N149 / Delta4000 · 4,8 MW

- P nominal (MW): 4.8 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): 149.1 [familia]. Nordex N149/4.X, HTML local [B24]. Referencia de familia; no certifica la revisión instalada.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Generador: DFIG · asíncrono doblemente alimentado [familia]. Nordex N149/4.X, HTML local [B24]. Referencia de familia; no certifica la revisión instalada.
- Multiplicadora: Sí [familia]. Nordex N149/4.X, HTML local [B24]. Referencia de familia; no certifica la revisión instalada.
- Control: pitch [familia]. Nordex N149/4.X, HTML local [B24]. Referencia de familia; no certifica la revisión instalada.
- Arranque (m/s): 3 [familia]. Nordex N149/4.X, HTML local [B24]. Referencia de familia; no certifica la revisión instalada.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): 20 [familia]. Nordex N149/4.X, HTML local [B24]. Base de familia 20 m/s; opciones específicas hasta 26 m/s. Umbral de cada parque sin confirmar.
- Convertidor: No documentado. Sin fuente específica. No consta en los documentos disponibles.

- N149 confirmado por suministro/montaje; Delta4000 es la plataforma confirmada en Los Olmos y Mesamavida.
- Multiplicadora de dos etapas planetarias y una cilíndrica; relación de transmisión no documentada.
- Alturas comerciales hasta 164 m no identifican la torre instalada.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- bladeCount=3: supuesto para animación; dato documental ausente.
- Dimensiones internas, número de dientes y distribución exacta de armarios son aproximaciones visuales sin planos acotados.
- Relación total 90:1 elegida para visualizar el movimiento; no es una relación OEM confirmada.
- Diámetros de rotor y altura visual mantienen una escala común; alturas no documentadas continúan como supuestos de 100 m.

### Vestas V110 · 2,0 MW

- P nominal (MW): 2 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): 110 [familia]. Vestas 2 MW, ficha V110 p. PDF 6 [B26]. Referencia de familia; no certifica la revisión instalada.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: 3 [familia]. Vestas 2 MW, ficha V110 p. PDF 6 [B26]. Referencia de familia; no certifica la revisión instalada.
- Generador: DFIG · doblemente alimentado con anillos rozantes [familia]. Vestas 2 MW, ficha V110 p. PDF 6 [B26]. Referencia de familia; no certifica la revisión instalada.
- Multiplicadora: Sí [familia]. Vestas 2 MW, ficha V110 p. PDF 6 [B26]. Referencia de familia; no certifica la revisión instalada.
- Control: pitch [familia]. Vestas 2 MW, ficha V110 p. PDF 6 [B26]. Referencia de familia; no certifica la revisión instalada.
- Arranque (m/s): 3 [familia]. Vestas 2 MW, ficha V110 p. PDF 6 [B26]. Referencia de familia; no certifica la revisión instalada.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): 21 [familia]. Vestas 2 MW, ficha V110 p. PDF 6 [B26]. Referencia de familia; no certifica la revisión instalada.
- Convertidor: No documentado. Sin fuente específica. No consta en los documentos disponibles.

- Opciones comerciales de altura: 75, 80, 95, 110, 120 y 125 m; no prueban la altura instalada.
- Los ~90 m del relato de un incidente no se usan como altura de buje.
- Envolvente de familia documentada: longitud de góndola 10,4 m, anchura 3,5 m; altura de transporte 4 m y 5,4 m instalada con CoolerTop. La reconstrucción interna no es un plano acotado.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- Dimensiones internas, número de dientes y distribución exacta de armarios son aproximaciones visuales sin planos acotados.
- Relación total 90:1 elegida para visualizar el movimiento; no es una relación OEM confirmada.
- Diámetros de rotor y altura visual mantienen una escala común; alturas no documentadas continúan como supuestos de 100 m.
