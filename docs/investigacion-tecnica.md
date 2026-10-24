# Investigación y reconstrucción técnica de cinco modelos

Revisión: 24 de octubre de 2026. Se conservan exactamente Goldwind GW87/1500, Envision EN110-2.1, Gamesa G114 (referencia de familia 2,0 MW), Nordex N149/4.X y Vestas V110-2.0 MW. Las otras cuatro variantes se retiraron del catálogo, JSON, GLB y fuentes Blender activas. Los documentos de entrada originales se conservan.

## Qué se ha encontrado y cómo se utiliza

| Modelo   | Base contrastada                                                                      | Aplicación en la reconstrucción                                                                                 | Límite                                                                                   |
| -------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Goldwind | Corte OEM 1.5 MW PMDD y especificaciones                                              | Generador anular PMSG directo, paso por correa, refrigeración pasiva, grúa auxiliar                             | Sin cotas internas por número de serie                                                   |
| Envision | Coener/Coordinador, tabla 3 p. PDF 8; esquema Winergy p. 11; comunicado Envision      | DFIG, transmisión 118:1, tres etapas, paso eléctrico AC, tres palas, 110 m; referencia contratada de buje 100 m | Tabla de diseño preliminar y esquema de familia, no as-built de cada unidad              |
| Gamesa   | Folleto original G114-2.0 y presentación OEM de plataforma archivados por reguladores | DFIG, 114 m, una etapa planetaria y dos paralelas; paso hidráulico                                              | La referencia 2,0 MW no resuelve la discrepancia de Las Peñas (cuatro unidades / 8,4 MW) |
| Nordex   | N149/4.X, página oficial                                                              | Dos etapas planetarias y una cilíndrica; DFIG refrigerado líquido/aire                                          | Relación total, dientes y cotas internas sin documentar                                  |
| Vestas   | Folleto OEM 2 MW, p. PDF 6 y página V110                                              | Una etapa planetaria y dos helicoidales, cilindros de paso, DFIG con anillos rozantes, envolvente y CoolerTop   | Cotas internas y configuración de torre instalada pendientes                             |

## Fuentes primarias enlazadas

### Envision

- [Informe técnico La Esperanza, Rev. 1](https://www.coordinador.cl/wp-content/uploads/2019/11/19-008-544-PE-La-Esperanza-Informe-detenci%C3%B3n-y-partida-04Nov19-Rev1.pdf). Coener / Coordinador Eléctrico Nacional; 6–8.
- [Up-tower repair solutions: PEAB 4456,8 para E110 2,1 MW](https://www.flender.com/media-download/media-direct/201905-Winergy-uptower-repair-solutions.pdf). Flender / Winergy; 11.
- [Pedido de cinco EN110-2.1 MW a 100 m](https://www.prnewswire.com/news-releases/envision-confirma-orden-por-105mw-de-petroquim-para-su-primer-parque-eolico-en-chile-526335301.html). Envision; Comunicado 2015.

### Gamesa

- [G114-2.0 MW: folleto original del fabricante](https://documents.dps.ny.gov/public/common/viewdoc.aspx?docrefid=%7Bf41cd6af-1b53-42e6-b748-fd1e2b2bcb72%7D). Gamesa, copia pública en NY DPS; 1–2.
- [Presentación Gamesa 2.0 MW: transmisión, DFIM y paso hidráulico](https://www.correze.gouv.fr/index.php/content/download/19153/130715/file/29-1%20-%20Reponse%20demande%20complement_CORREZE1%20Complet.pdf). Gamesa, expediente Prefectura Corrèze; Láminas de plataforma y G114.

### Goldwind

- [Goldwind 1.5 MW PMDD: corte funcional y especificaciones](https://www.goldwindamericas.com/sites/default/files/1.5%20MW%20PMDD%20Turbine%20-%20English.pdf). Goldwind; 3–6.

### Nordex

- [N149/4.X: etapas de transmisión y generador](https://www.nordex-online.com/es/product/n149-4-0-4-5/?noredirect=es-ES). Nordex; Datos técnicos web.

### Vestas

- [V110-2.0 MW y folleto 2 MW conservado en el corpus](https://www.vestas.com/en/energy-solutions/onshore-wind-turbines/2-mw-platform/V110-2-0-mw). Vestas; Ficha V110: PDF 6.

## Precisión y vacíos que se conservan

Se revisaron dibujos funcionales, un corte de transmisión y especificaciones OEM; no se localizaron planos acotados completos para las cinco máquinas. Los GLB son reconstrucciones documentadas, con datos de familia distinguidos de datos de parque. No son archivos CAD de fabricación ni gemelos certificados.

La relación 118:1 de Envision está en su tabla de diseño. Para las otras multiplicadoras se conserva 90:1 como supuesto explícito; no se selecciona una de las relaciones comerciales Gamesa sin acreditar variante y frecuencia. El número de dientes y el reparto por etapas son ilustrativos incluso cuando la relación total está documentada.

El diámetro de los rotores se representa con un factor visual común; las alturas no documentadas usan el supuesto de 100 m. Los componentes internos se han normalizado para su lectura didáctica; no deben medirse como planos de montaje.

Se conserva la discrepancia del informe Envision: texto 0,6 kV/23 kV y tabla de 690 V. El nominal del aerogenerador es 2,1 MW; los 2.200 kW de la tabla corresponden al sistema eléctrico, no sustituyen la potencia nominal.

## Acabados originales

Bordes biselados, juntas y tornillería de paneles, trampillas y asas, placas educativas, rotulación vectorial, ventilación, juntas de elastómero y materiales de pintura, acero y cobre. Los DFIG incorporan bobinado y anillos rozantes con escobillas estacionarias. Estas piezas cosméticas no completan datos técnicos ausentes. Las ilustraciones y los PDF OEM no se redistribuyen como texturas o assets.

La animación de Envision se ancla al punto de diseño: 1.680 RPM de generador, relación 118:1 y viento nominal 9,5 m/s. La TSR resultante se usa constante hasta nominal como aproximación explícita; no se reproduce un controlador propietario.
