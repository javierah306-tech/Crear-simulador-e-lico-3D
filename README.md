# Smartwind · Explorador eólico del Biobío

Simulador educativo 3D en español de nueve modelos o variantes presentes en la documentación del Biobío. La nueva versión renueva los interiores mecánicos, los materiales y la interfaz con una paleta de arena, verde y cobre. Funciona sin registro, servidor de datos ni claves de acceso.

El visitante puede alternar entre dos acercamientos principales: exterior a la altura de la góndola e interior traslúcido. La cámara orbital, la selección de piezas, la vista de explosión y el flujo de energía permiten explorar la máquina en operación normal. El viento permanece fijo en **8 m/s**; no hay reguladores de condiciones.

## Ejecutar

Requiere Node.js 24 y pnpm 11.19.0.

```sh
pnpm install --frozen-lockfile
pnpm dev
```

Abrir la dirección local que imprime Vite. La carpeta de trabajo es `C:\Users\javie\OneDrive\Desktop\Lab Neiron\modelos 3D eolicos`.

```sh
pnpm lint
pnpm check:data
pnpm test
pnpm build
pnpm preview
```

## Qué incluye

- React, TypeScript, Vite, Three.js con React Three Fiber/drei, Zustand, GSAP y Tailwind CSS.
- Nueve fuentes Blender editables y dieciocho GLB con Draco: geometría detallada para el interior y LOD reducido para el exterior.
- Palas perfiladas, buje, apoyos, tren mecánico, generador, equipos eléctricos y estructura de la góndola, con partes animadas identificables.
- Dos cámaras principales, interior traslúcido, vista de explosión, selección por ratón o botones, ficha técnica y catálogo comparativo.
- Datos y supuestos separados en JSON, pruebas de las fórmulas y validación del contrato de los assets.
- CI automática que valida, compila y despliega GitHub Pages al subir a `main`; validación de pull requests y configuración alternativa para Netlify.

## Documentación

- [Tabla de modelos y proveedores](docs/modelos-extraidos.md), además de CSV con campos y procedencia.
- [Arquitectura, ecuaciones, extensión y plan](docs/arquitectura-y-plan.md).
- [Cambios de la nueva versión visual](docs/mejora-visual.md).
- [Verificación y límites de la entrega](docs/verificacion.md).
- [Esquema JSON](src/data/turbine.schema.json) y [contratos TypeScript](src/data/types.ts).
- [Fuentes documentales](docs/fuentes.md).

## Datos y alcance técnico

La fuente primaria es `02_PARQUES_COMPONENTES_BIOBIO.pdf`, contrastada con el corpus local de fabricantes en `modelos chilenos/`. Corte documental: 3 de octubre de 2026. Los JSON distinguen datos instalados, referencias de familia y campos ausentes. La ficha muestra **No documentado** cuando no existe evidencia. No se afirma un inventario vigente por unidad.

`simulation` contiene los valores ilustrativos usados para calcular potencia, RPM y paso. Las Peñas conserva la discrepancia de potencia. Las geometrías, el detalle de engranajes, las relaciones de movimiento y la ubicación de los equipos son reconstrucciones didácticas originales; las imágenes recibidas inspiran el acabado y no acreditan una configuración instalada. Los modelos con transmisión sin documentar muestran una cadena funcional genérica y conservan esa incertidumbre en la ficha. Una ausencia de multiplicadora en esas geometrías no demuestra accionamiento directo.

Los PDF/HTML completos y las imágenes de inspiración no se redistribuyen como assets. El código y los modelos originales usan licencia MIT.

## Modelado y extensión

```sh
# Windows: detecta Blender 5.2 en su ruta habitual.
pnpm models
# También se puede definir BLENDER_PATH con el ejecutable de Blender.
```

`scripts/create_models.py` construye los assets originales, guarda fuentes `.blend` y exporta GLB con compresión Draco, etiquetas de componente y animación de rotor. Los assets están incluidos: Blender no es necesario para ejecutar ni compilar el visor.

Para agregar una eólica basta un JSON que cumpla el esquema y un GLB compatible. El selector descubre los JSON automáticamente. `asset.lod` puede apuntar al mismo archivo si todavía no existe una versión reducida. Consulta el contrato en [arquitectura](docs/arquitectura-y-plan.md).

`scripts/build_catalog.py` reproduce la extracción curada y `scripts/generate_deliverables.py` genera tablas y esquema. No deben ejecutarse para sustituir datos desconocidos por valores inferidos del nombre de un modelo.

## Repositorio y publicación

La nueva versión está subida a [Crear-simulador-e-lico-3D](https://github.com/javierah306-tech/Crear-simulador-e-lico-3D), rama `main`. La aplicación está publicada en GitHub Pages con HTTPS y acceso libre. El workflow de publicación terminó correctamente.

Abrir la aplicación: [Smartwind · Explorador eólico](https://javierah306-tech.github.io/Crear-simulador-e-lico-3D/). La web pública se verificó con los nueve modelos en escritorio y móvil; los dieciocho GLB publicados coinciden con los archivos locales. Resultados y límites en [verificación](docs/verificacion.md).

Cada subida a `main` ejecuta **Publicar en GitHub Pages**: valida código, datos y simulación, compila el sitio y lo despliega. También puede ejecutarse manualmente desde **Actions**. Las pull requests ejecutan validación sin despliegue. No se requiere registro para visitar la aplicación.
