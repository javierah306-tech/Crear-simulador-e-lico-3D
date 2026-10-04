# Arquitectura y plan de entrega

El producto abre directamente el visor. El boceto se interpreta como un selector lateral, una escena central a altura de góndola, acceso a un interior traslúcido y un botón para avanzar al siguiente modelo. Se usan dos posiciones principales de cámara; el usuario también puede orbitar y acercar libremente. La indicación expresa de no ofrecer reguladores prevalece sobre el requisito posterior de un deslizador de viento: el escenario usa 8 m/s fijos y no ofrece edición de las condiciones.

## Estructura

```text
src/
  App.tsx                         interfaz y navegación
  styles.css                      tema responsivo, integrado con Tailwind 4
  data/
    models/*.json                 fuente única de datos de cada aerogenerador
    turbine.schema.json           JSON Schema con alcance y procedencia
    types.ts                      contratos TypeScript
    catalog.ts                    descubrimiento automático de JSON
    components.ts                 funciones de las piezas en español
  store/useSimulator.ts           selector, cámara, selección y animación (Zustand)
  simulation/normalOperation.ts   escenario normal y estimaciones
  components/
    TurbineScene.tsx              Canvas R3F, GLB, raycasting, cámara y flujos
    TechnicalSheet.tsx            ficha y supuestos por campo
    Catalog.tsx                   comparación documental
public/
  models/*.glb                    modelos y variantes de menor detalle
  draco/                          decodificador local, sin CDN externo
  favicon.svg
assets/blender/*.blend            fuentes originales editables
scripts/
  create_models.py                modelado y exportación Blender a GLB/Draco
  export-models.mjs               lanzador Blender
  build_catalog.py               reproducción de la extracción curada
  generate_deliverables.py        tablas y esquema
  check-data.ts                   verificación de JSON y estructura GLB
tests/simulation.test.ts          invariantes de curva y umbrales
.github/workflows/pages.yml       CI y publicación HTTPS en GitHub Pages
docs/                            extracción, arquitectura, fuentes y plan
```

El visor se carga con `React.lazy`. Cada GLB solo se solicita al seleccionar el modelo: LOD reducido en exterior y geometría detallada en interior. La cámara usa OrbitControls de drei; GSAP interpola acercamientos y posiciones de la vista de explosión. La animación de rotor viene del glTF exportado por Blender y ajusta su velocidad a las RPM estimadas. Generador y engranajes tienen movimiento cinemático adicional.

Las piezas tienen `extras.component` en glTF. El raycasting identifica ese atributo en la pieza o sus padres. Existe una lista equivalente de botones para selección por teclado. La ficha usa un diálogo nativo modal con foco contenido, cierre por Escape y devolución de foco al disparador. El Canvas tiene mensaje alternativo cuando WebGL no está disponible.

## Datos y extensión

Cada dato técnico es `{ value, source, scope, note }`. `scope` puede ser `installed`, `family` o `missing`. Los datos ausentes tienen `value: null`; un valor de familia no se convierte silenciosamente en dato de un parque. El objeto `simulation` almacena valores ilustrativos separados, incluyendo supuestos explícitos. `parks[]` conserva discrepancias, evidencias y alturas particulares.

Para agregar un modelo se incorpora un JSON que cumpla el esquema y un GLB con la misma convención de componentes. No se modifica el selector. Si solo hay un GLB, `asset.lod` puede apuntar al mismo archivo que `asset.glb`; la validación lo permite. Para producción se recomienda un LOD real; los nueve modelos entregados tienen ambos niveles. No se requieren cambios de componentes React por modelo.

### Contrato del GLB

- Coordenadas glTF Y hacia arriba; eje mecánico X; góndola centrada cerca del origen.
- Grupos `RotorAssembly`, `MainShaft`, `Generator`, `GeneratorRotor`, `Converter`, `Transformer`, `Yaw`, `Nacelle`, `Tower`; `Gearbox` solo si está documentada.
- Mesh `Shell` para transparencia. Cada pieza conserva `extras.component` con su identificador.
- Pitch: grupos `Pitch_0` a `Pitch_2`; engranajes: `GearWheel_0` a `GearWheel_2` si aplican.
- Clip de rotación a 12 RPM nominales de reproducción; el runtime usa `timeScale = RPM / 12`.
- No se usa una geometría como evidencia de un componente instalado. Los assets actuales son modelos educativos normalizados, no reconstrucciones CAD OEM.

## Modelo didáctico

Para viento `v` dentro del rango y `v_nom > v_in`:

```text
P(v) = P_nom × clamp((v³ − v_in³) / (v_nom³ − v_in³), 0, 1)
RPM(v) = min(RPM_max, 60 × λ × min(v, v_nom) / (π × D))
pitch(v) = pitch_base + ganancia × max(0, v − v_nom)
```

En la interfaz `v = 8 m/s` es constante. La fórmula incluye límites para validar los cálculos, pero no hay escenarios de fallas, extremos o transitorios. La curva no incorpora pérdidas, variación de densidad, control propietario ni medidas reales. Para Goldwind se usan umbrales de familia 3/9,9/22 m/s; para los datos ausentes se usa nominal ilustrativa 12 m/s. La relación de transmisión de 90:1 en máquinas con multiplicadora es un supuesto visual, no una especificación del fabricante.

En DFIG la electricidad del estator pasa al transformador y la rama del rotor atraviesa el convertidor. Los demás modelos muestran una ruta funcional de escala completa o una ruta abstracta cuando la arquitectura no está documentada. Las partículas ilustran la dirección, no paquetes físicos de energía ni valores de potencia distribuidos.

## Plan por etapas

| Etapa                        | Resultado y criterio de salida                                                                              | Estado en esta base                                                        |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| 1. Prototipo con Goldwind    | GLB sin multiplicadora, vista exterior/interior, rotor animado, ficha y cámara orbital                      | Implementado y probado en navegador                                        |
| 2. Catálogo completo         | Nueve modelos/variantes, selector por JSON, separación de arquitectura, vacíos y discrepancias visibles     | Implementado con geometrías didácticas                                     |
| 3. Fidelidad técnica         | Planos o manuales autorizados por variante, alturas instaladas, curvas OEM, mapa por número de serie        | Pendiente de documentación; no inventar para cerrar vacíos                 |
| 4. Optimización y validación | Draco, LOD, carga diferida; medir en Android de gama media y Safari iOS; reducir draw calls si es necesario | Compresión, LOD y carga diferida implementados; benchmark físico pendiente |
| 5. Publicación               | Repositorio remoto, workflow exitoso, URL HTTPS pública sin registro                                        | Configuración lista; falta cuenta/repositorio de hosting                   |

### Publicar

1. Crear un repositorio de GitHub y subir el proyecto a la rama `main`, incluidos los GLB, decodificadores y el lockfile. No subir `node_modules`, `dist`, extracciones temporales ni documentos OEM completos.
2. En **Settings → Pages**, seleccionar **GitHub Actions**. El workflow comprueba lint, esquema/GLB, fórmulas y build antes de publicar. Configura la ruta base a `/<nombre-repositorio>/`.
3. Verificar la URL publicada por el job `deploy`: carga de Draco, cambios de modelo, dos vistas, navegación móvil y ausencia de registro. Para un repositorio de sitio de usuario (`usuario.github.io`), cambiar `VITE_BASE_PATH` a `/`.

Netlify: importar el repositorio; `netlify.toml` configura `pnpm build` y `dist`. Cloudflare Pages: usar el mismo comando y directorio, Node 24 y base `/`. La publicación requiere una cuenta de hosting para el propietario, pero el visitante no necesita cuenta. PWA y WebGPU son mejoras opcionales no implementadas.

## Límites prácticos

No hay backend, autenticación ni uso de APIs de pago. Los assets originales y el código usan licencia MIT; los documentos de fabricantes conservan sus propios derechos y no se redistribuyen en el sitio. El rendimiento móvil tiene objetivo de fluidez pero no una certificación de FPS. El modo interior usa un esquema de subsistemas; para las máquinas sin ficha específica no se presenta como gemelo de la configuración instalada.
