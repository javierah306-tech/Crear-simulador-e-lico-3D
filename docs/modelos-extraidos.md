# Modelos y proveedores del Biobío

Fuente base: 02_PARQUES_COMPONENTES_BIOBIO.pdf, Smartwind v1.0, corte documental 03-10-2026. Corpus complementario: Goldwind 1,5 MW, Vestas 2 MW, Vestas 4 MW, Vestas V112 LCA 2011 y HTML local Nordex N149. Se conserva el nivel de evidencia del informe; las referencias Bxx son las de ese informe, no consultas nuevas.

El catálogo registra nueve modelos o variantes y trece entradas de parque (Raki y Huajache separados). No es un censo actualizado ni una certificación por número de serie. Se usa el Biobío actual.

## Fabricantes, suministro y parques

| Fabricante / modelo              | Potencia unitaria documentada | Parque(s)                    | Evidencia                                                         | Proveedor de instalación mencionado               |
| -------------------------------- | ----------------------------- | ---------------------------- | ----------------------------------------------------------------- | ------------------------------------------------- |
| Envision E110 · 2,1 MW           | 2.1 [parque]                  | La Esperanza                 | La Esperanza: B B03,B16                                           | La Esperanza: Tecnorenova                         |
| Gamesa G114 · variante pendiente | No documentado                | Las Peñas                    | Las Peñas: B B17,B18                                              | Las Peñas: CJR Renewables                         |
| Goldwind GW1500-87               | 1.5 [parque]                  | Cuel                         | Cuel: A B01                                                       | No documentado                                    |
| Nordex N149 / Delta4000 · 4,8 MW | 4.8 [parque]                  | Alena, Los Olmos, Mesamavida | Alena: B B03,B06; Los Olmos: A/B B07,B08; Mesamavida: A/B B09,B10 | Los Olmos: Greenwork; Mesamavida: Tecnorenova     |
| Vestas V110 · 2,0 MW             | 2 [parque]                    | Los Buenos Aires             | Los Buenos Aires: A B14,B20                                       | No documentado                                    |
| Vestas V112 · 3,0 MW             | 3 [parque]                    | Raki, Huajache               | Raki: A B15; Huajache: A B15                                      | No documentado                                    |
| Vestas V136 CP3.6 · PO1 · 50 Hz  | 3.6 [parque]                  | Negrete                      | Negrete: A B02,B05                                                | Negrete: Tecnorenova (referencia discrepante B23) |
| Vestas V150 Mk3B · 4,2 MW        | 4.2 [parque]                  | Lomas de Duqueco             | Lomas de Duqueco: A B02,B04                                       | No documentado                                    |
| Vestas V150 · 4,3 MW             | 4.3 [parque]                  | Campo Lindo, San Matías      | Campo Lindo: A B11; San Matías: A B12,B13                         | No documentado                                    |

Fabricante, operador e instalador son roles distintos. «Proveedor» se entrega como fabricante identificado; el corpus no demuestra un contratista de suministro independiente para todos los parques. Tecnorenova/Greenwork/CJR son referencias de instalación, no fabricantes.

## Datos técnicos extraídos

Cada valor incluye su alcance. Ausencia de un dato no se reemplaza por la cifra de otra variante. Alturas de torre se conservan por parque.

### Geometría y arquitectura

| Modelo                    | Rotor (m)       | Buje instalado (m) | Palas          | Generador                                                   | Multiplicadora | Control         |
| ------------------------- | --------------- | ------------------ | -------------- | ----------------------------------------------------------- | -------------- | --------------- |
| E110 · 2,1 MW             | No documentado  | No documentado     | No documentado | No documentado                                              | No documentado | No documentado  |
| G114 · variante pendiente | No documentado  | No documentado     | No documentado | No documentado                                              | No documentado | No documentado  |
| GW1500-87                 | 87 [familia]    | No documentado     | 3 [familia]    | PMSG · síncrono de imanes permanentes [familia]             | No [familia]   | pitch [familia] |
| N149 / Delta4000 · 4,8 MW | 149.1 [familia] | No documentado     | No documentado | DFIG · asíncrono doblemente alimentado [familia]            | Sí [familia]   | pitch [familia] |
| V110 · 2,0 MW             | 110 [familia]   | No documentado     | 3 [familia]    | DFIG · doblemente alimentado con anillos rozantes [familia] | Sí [familia]   | pitch [familia] |
| V112 · 3,0 MW             | No documentado  | No documentado     | No documentado | No documentado                                              | Sí [familia]   | No documentado  |
| V136 CP3.6 · PO1 · 50 Hz  | No documentado  | No documentado     | No documentado | Inducción · subtipo no indicado [parque]                    | No documentado | No documentado  |
| V150 Mk3B · 4,2 MW        | 150 [familia]   | No documentado     | 3 [familia]    | Inducción · subtipo no indicado [parque]                    | Sí [familia]   | pitch [familia] |
| V150 · 4,3 MW             | 150 [familia]   | No documentado     | 3 [familia]    | No documentado                                              | Sí [familia]   | pitch [familia] |

### Umbrales de operación y conversión

| Modelo                    | Arranque (m/s) | Nominal (m/s)  | Corte (m/s)    | Convertidor                      |
| ------------------------- | -------------- | -------------- | -------------- | -------------------------------- |
| E110 · 2,1 MW             | No documentado | No documentado | No documentado | No documentado                   |
| G114 · variante pendiente | No documentado | No documentado | No documentado | No documentado                   |
| GW1500-87                 | 3 [familia]    | 9.9 [familia]  | 22 [familia]   | Escala completa (IGBT) [familia] |
| N149 / Delta4000 · 4,8 MW | 3 [familia]    | No documentado | 20 [familia]   | No documentado                   |
| V110 · 2,0 MW             | 3 [familia]    | No documentado | 21 [familia]   | No documentado                   |
| V112 · 3,0 MW             | No documentado | No documentado | No documentado | No documentado                   |
| V136 CP3.6 · PO1 · 50 Hz  | No documentado | No documentado | No documentado | Escala completa [parque]         |
| V150 Mk3B · 4,2 MW        | No documentado | No documentado | No documentado | Escala completa [familia]        |
| V150 · 4,3 MW             | No documentado | No documentado | No documentado | Escala completa [familia]        |

### Alturas y discrepancias

San Matías: 140 m de torre reportados en el informe p. 5 [B13]. Se conserva en `parks[].hubHeightM` con la nota de confirmar la definición de altura de buje; no se transfiere a Campo Lindo. Las otras alturas instaladas no constan. Opciones de altura de familia V110: 75/80/95/110/120/125 m; Nordex hasta 164 m; V150 ofrece varias torres en el folleto. No se escoge una como instalada.

V136 CP3.6 no hereda diámetro, pitch ni multiplicadora del V136-4.2. V112/E110/G114 no reciben diámetro por interpretación del nombre. El catálogo conserva los datos explícitos y hace visibles los vacíos.

Las Peñas: constructor informa cuatro G114, 2 MW por unidad y 8,4 MW de proyecto; no se fija 2,1 MW ni 2,5 MW. Negrete: diez CP3.6 de 3,6 MW según CEN/operador frente a once de 3,45 MW según instalador; se conserva el alcance ensayado. San Matías: «N163 V150» se concilia con B13 como Vestas V150, manteniendo la inconsistencia. N149 de Los Olmos/Mesamavida: plataforma Delta4000 confirmada, modelo específico con evidencia de montaje. Alena: pedido y registro histórico, sin certificación de inventario 2026.

Umbrales V150-4.2/4.5 del folleto comercial: 3 m/s de arranque, 24,5 m/s de corte. No se asignan a Mk3B/4,3 MW instaladas. V136-4.2: 3/25 m/s, no transferidos a CP3.6. Nordex: 20 m/s base y opción hasta 26 m/s, no certificada por parque. Goldwind: 22 m/s de corte en promedio de diez minutos, nominal estática 9,9 m/s.

## Trazabilidad por campo

### Envision E110 · 2,1 MW

- P nominal (MW): 2.1 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Generador: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Multiplicadora: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Control: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Arranque (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Convertidor: No documentado. Sin fuente específica. No consta en los documentos disponibles.

- Sin ficha OEM verificable de esta variante en el corpus. Geometría exterior genérica y cadena de conversión abstracta; no se inventa arquitectura.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- rotorDiameterM=110: supuesto para animación; dato documental ausente.
- cutInMS=3: supuesto para animación; dato documental ausente.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- cutOutMS=20: supuesto para animación; dato documental ausente.
- bladeCount=3: supuesto para animación; dato documental ausente.

### Gamesa G114 · variante pendiente

- P nominal (MW): No documentado. Sin fuente específica. Discrepancia: 2 MW por unidad frente a 8,4 MW para cuatro unidades. No se fija variante.
- Rotor (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Generador: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Multiplicadora: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Control: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Arranque (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Convertidor: No documentado. Sin fuente específica. No consta en los documentos disponibles.

- La variante G114/2000 aparece en el informe, pero no resuelve la discrepancia de potencia del parque.
- Potencia de 2 MW usada SOLO como supuesto del escenario, no como ficha instalada.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- rotorDiameterM=110: supuesto para animación; dato documental ausente.
- cutInMS=3: supuesto para animación; dato documental ausente.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- cutOutMS=20: supuesto para animación; dato documental ausente.
- bladeCount=3: supuesto para animación; dato documental ausente.
- ratedPowerMW=2: capacidad ilustrativa sin variante confirmada.

### Goldwind GW1500-87

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

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.

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
- Relación de transmisión ilustrativa 90:1, no documentada.

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

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- Relación de transmisión ilustrativa 90:1, no documentada.

### Vestas V112 · 3,0 MW

- P nominal (MW): 3 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Generador: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Multiplicadora: Sí [familia]. Informe p. 8; Vestas LCA 2011 p. PDF 72 [B27]. Referencia de familia; no certifica la revisión instalada.
- Control: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Arranque (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Convertidor: No documentado. Sin fuente específica. No consta en los documentos disponibles.

- LCA histórica confirma componentes, sin certificar generador ni etapas de transmisión de Raki/Huajache. No se deduce diámetro del nombre del modelo.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- rotorDiameterM=110: supuesto para animación; dato documental ausente.
- cutInMS=3: supuesto para animación; dato documental ausente.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- cutOutMS=20: supuesto para animación; dato documental ausente.
- bladeCount=3: supuesto para animación; dato documental ausente.
- Relación de transmisión ilustrativa 90:1, no documentada.

### Vestas V136 CP3.6 · PO1 · 50 Hz

- P nominal (MW): 3.6 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Generador: Inducción · subtipo no indicado [parque]. Informe p. 7 [B05]. Inducción con convertidor de escala completa; no se infiere DFIG.
- Multiplicadora: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Control: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Arranque (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Convertidor: Escala completa [parque]. Informe p. 7 [B05]. Configuración ensayada de Negrete.

- No se transfieren diámetro, umbrales, transmisión ni opciones del folleto V136-4.2 a CP3.6. El interior muestra únicamente la cadena funcional conocida.

Supuestos empleados en el escenario:

- Viento fijo de 8 m/s, uniforme, alineado con el rotor.
- Curva cúbica simplificada sin pérdidas; no es una curva medida ni certificada.
- RPM estimadas con relación de velocidad de punta λ=7, límite de 16 RPM.
- Pitch didáctico: 1,5° bajo viento nominal, +2° por m/s sobre nominal.
- Proporciones y ubicación de componentes esquemáticas, sin planos por número de serie.
- Altura visual normalizada; las posiciones del convertidor y transformador son didácticas.
- rotorDiameterM=110: supuesto para animación; dato documental ausente.
- cutInMS=3: supuesto para animación; dato documental ausente.
- ratedWindMS=12: supuesto para animación; dato documental ausente.
- cutOutMS=20: supuesto para animación; dato documental ausente.
- bladeCount=3: supuesto para animación; dato documental ausente.

### Vestas V150 Mk3B · 4,2 MW

- P nominal (MW): 4.2 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): 150 [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: 3 [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Generador: Inducción · subtipo no indicado [parque]. Informe p. 7 [B04]. Generador de inducción y convertidor completo documentados para Mk3B. No se etiqueta DFIG.
- Multiplicadora: Sí [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Control: pitch [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Arranque (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Convertidor: Escala completa [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.

- El folleto V150-4.2/4.5 no documenta una variante 4,3 MW ni confirma umbrales de las unidades chilenas.

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
- Relación de transmisión ilustrativa 90:1, no documentada.

### Vestas V150 · 4,3 MW

- P nominal (MW): 4.3 [parque]. Informe p. 4. Potencia unitaria descrita en el catálogo; no equivale a potencia neta de conexión.
- Rotor (m): 150 [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Buje instalado (m): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Palas: 3 [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Generador: No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Multiplicadora: Sí [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Control: pitch [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.
- Arranque (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Nominal (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Corte (m/s): No documentado. Sin fuente específica. No consta en los documentos disponibles.
- Convertidor: Escala completa [familia]. Informe p. 7; Vestas 4 MW p. 9 [B25]. Referencia de familia; no certifica la revisión instalada.

- El folleto V150-4.2/4.5 no documenta una variante 4,3 MW ni confirma umbrales de las unidades chilenas.
- El generador de inducción del Mk3B de 4,2 MW no se transfiere a las variantes de 4,3 MW: su tipo queda sin documentar.

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
- Relación de transmisión ilustrativa 90:1, no documentada.
