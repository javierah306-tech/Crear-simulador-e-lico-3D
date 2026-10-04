# Smartwind · Explorador eólico del Biobío

Base funcional en español: React 19, TypeScript, Vite, Three.js/React Three Fiber, drei, Zustand, GSAP y Tailwind CSS. Incluye nueve modelos o variantes de la documentación regional, dieciocho GLB con Draco y nueve fuentes Blender.

Dos acercamientos principales, cámara orbital, interior traslúcido, rotor animado, flujo de energía, selección de componentes, vista de explosión, ficha documental y comparación de modelos. Sin registro ni control de viento: escenario normal fijo de 8 m/s.

## Ejecutar

Requiere Node.js 24 y pnpm 11.19.0.

```sh
pnpm install --frozen-lockfile
pnpm dev
```

Abrir la dirección local que imprime Vite. El sitio es estático y no necesita servidor de datos ni claves.

```sh
pnpm lint
pnpm check:data
pnpm test
pnpm build
pnpm preview
```

## Entregables

- [Tabla de modelos y proveedores](docs/modelos-extraidos.md), además de CSV con todos los campos y procedencia.
- [Arquitectura, ecuaciones, plan por etapas y publicación](docs/arquitectura-y-plan.md).
- [Esquema JSON](src/data/turbine.schema.json), [contratos TypeScript](src/data/types.ts) y un JSON por modelo en `src/data/models`.
- Visor funcional en `src/components/TurbineScene.tsx`, UI en `src/App.tsx`.
- Assets GLB comprimidos y fuentes originales en `assets/blender`.
- CI/CD listo para GitHub Pages; configuración adicional para Netlify.

## Fuentes y precauciones de interpretación

La extracción proviene de `02_PARQUES_COMPONENTES_BIOBIO.pdf` y del corpus local de fabricantes encontrado en la carpeta `modelos 3D eolicos/modelos chilenos`. Corte documental: 3 de octubre de 2026. No se afirma un inventario vigente por unidad. Los JSON distinguen dato instalado, referencia de familia y dato ausente. `simulation` contiene valores ilustrativos separados de la ficha. Las Peñas conserva la discrepancia de potencia; la configuración exacta de varias máquinas sigue pendiente. Las geometrías son esquemáticas, normalizadas y originales, no CAD de fabricantes.

Los PDF/HTML completos no se distribuyen con el sitio; las referencias por campo permanecen en los JSON y la documentación. Consulta `docs/fuentes.md` para las rutas de lectura y la huella de los documentos usados.

## Modelado

```sh
# Windows: detecta Blender 5.2 en su ruta habitual.
pnpm models
# O definir BLENDER_PATH con el ejecutable de Blender antes de ejecutar.
```

`scripts/create_models.py` genera los modelos educativos y exporta glTF con extras por componente y un clip de rotor a 12 RPM. Los assets ya están incluidos; Blender no es necesario para usar ni compilar el visor. `scripts/build_catalog.py` reproduce la curación documental; cambiar un JSON directamente es suficiente para la extensión y no requiere ejecutar ese generador. `scripts/generate_deliverables.py` actualiza tablas y esquema.

## Estado de publicación

El proyecto está preparado para una URL pública HTTPS en GitHub Pages, Netlify o Cloudflare Pages. No está publicado todavía: falta configurar una cuenta/repositorio remoto. Las pruebas de navegador realizadas en este entorno y los límites de rendimiento se registran en `docs/verificacion.md`.
