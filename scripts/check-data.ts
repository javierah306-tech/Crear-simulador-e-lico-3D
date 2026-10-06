import Ajv from 'ajv';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import assert from 'node:assert/strict';
import type { TurbineModel } from '../src/data/types';

interface GltfNode {
  name?: string;
  mesh?: number;
  extras?: Record<string, unknown>;
}
interface GltfPrimitive {
  mode?: number;
  indices?: number;
  attributes: Record<string, number>;
  extensions?: Record<string, unknown>;
}
interface GltfAsset {
  asset: { version: string };
  extensionsRequired?: string[];
  nodes: GltfNode[];
  meshes: { primitives: GltfPrimitive[] }[];
  accessors: { count: number }[];
  animations?: {
    channels: { target: { node: number; path: string }; sampler: number }[];
    samplers: { input: number; output: number }[];
  }[];
}
const componentIds = new Set([
  'blades',
  'hub',
  'rotor',
  'shaft',
  'gearbox',
  'generator',
  'converter',
  'transformer',
  'yaw',
  'pitch',
  'nacelle',
  'tower',
]);
const requiredGroups = [
  'RotorAssembly',
  'MainShaft',
  'Generator',
  'GeneratorRotor',
  'Converter',
  'Transformer',
  'Yaw',
  'Nacelle',
  'Tower',
];

function inspectAsset(path: string, model: TurbineModel) {
  assert(existsSync(path), `Falta ${path}`);
  const buffer = readFileSync(path);
  assert(buffer.length >= 20, `GLB incompleto: ${path}`);
  assert.equal(buffer.toString('ascii', 0, 4), 'glTF', `Cabecera incorrecta: ${path}`);
  assert.equal(buffer.readUInt32LE(4), 2, `Versión GLB incorrecta: ${path}`);
  assert.equal(buffer.readUInt32LE(8), buffer.length, `Longitud GLB incorrecta: ${path}`);
  assert.equal(buffer.readUInt32LE(16), 0x4e4f534a, `Falta chunk JSON: ${path}`);
  const jsonEnd = 20 + buffer.readUInt32LE(12);
  assert(jsonEnd <= buffer.length, `Chunk JSON truncado: ${path}`);
  const asset = JSON.parse(buffer.toString('utf8', 20, jsonEnd)) as GltfAsset;
  assert.equal(asset.asset.version, '2.0', `Versión glTF incorrecta: ${path}`);
  assert(asset.extensionsRequired?.includes('KHR_draco_mesh_compression'), `Sin Draco: ${path}`);
  assert(asset.nodes?.length > 0 && asset.meshes?.length > 0, `GLB sin geometría: ${path}`);
  const names = new Set(asset.nodes.map((node) => node.name));
  for (const group of requiredGroups) assert(names.has(group), `Falta ${group}: ${path}`);
  assert(
    asset.nodes.some((node) => node.name === 'Shell' || node.name?.startsWith('Shell_')),
    `Falta carcasa traslúcida: ${path}`,
  );
  assert.equal(
    names.has('Gearbox'),
    model.specs.gearbox.value === true,
    `Multiplicadora incorrecta en ${model.id}`,
  );
  // V110 family brochure, PDF p. 6: one planetary and two helical stages.
  // Ratios and tooth counts remain illustrative; check topology, not CAD dimensions.
  if (model.id === 'vestas-v110-20') {
    const planetaryStages = asset.nodes.filter((node) =>
      /^PlanetaryStage\d+$/.test(node.name ?? ''),
    );
    const helicalStages = new Set(
      asset.nodes.flatMap((node) => {
        const match = /^HelicalStage(\d+)_(Input|Output)$/.exec(node.name ?? '');
        return match ? [match[1]] : [];
      }),
    );
    assert.equal(planetaryStages.length, 1, `V110 debe tener una etapa planetaria: ${path}`);
    assert.deepEqual(
      [...helicalStages].sort(),
      ['1', '2'],
      `V110 requiere dos etapas helicoidales: ${path}`,
    );
    for (const stage of helicalStages) {
      assert(
        names.has(`HelicalStage${stage}_Input`) && names.has(`HelicalStage${stage}_Output`),
        `Etapa helicoidal V110 incompleta: ${path}`,
      );
    }
    const gearboxExtras = asset.nodes.find((node) => node.name === 'Gearbox')?.extras;
    assert.equal(
      gearboxExtras?.stageLayoutScope,
      'family',
      `V110 debe indicar alcance de familia: ${path}`,
    );
  }
  for (let i = 0; i < model.simulation.bladeCount; i++) {
    assert(names.has(`Pitch_${i}`), `Falta mecanismo de paso ${i}: ${path}`);
  }
  const components = new Set<string>();
  for (const node of asset.nodes) {
    const extras = node.extras;
    if (extras?.component !== undefined) {
      assert(
        typeof extras.component === 'string' && componentIds.has(extras.component),
        `Componente desconocido en ${node.name}: ${path}`,
      );
      components.add(extras.component);
    }
    if (extras?.motionRatio !== undefined) {
      assert(
        typeof extras.motionRatio === 'number' && Number.isFinite(extras.motionRatio),
        `Relación de movimiento inválida en ${node.name}: ${path}`,
      );
      assert(
        ['x', 'y', 'z'].includes(String(extras.motionAxis)),
        `Eje de movimiento inválido en ${node.name}: ${path}`,
      );
      assert(
        typeof extras.motionBaseRPM === 'number' &&
          extras.motionBaseRPM > 0 &&
          Number.isFinite(extras.motionBaseRPM),
        `RPM de referencia inválidas: ${path}`,
      );
    }
  }
  for (const component of componentIds) {
    if (component === 'gearbox' && model.specs.gearbox.value !== true) continue;
    assert(components.has(component), `Componente sin etiqueta ${component}: ${path}`);
  }
  assert.equal(
    components.has('gearbox'),
    model.specs.gearbox.value === true,
    `Etiqueta de multiplicadora no respaldada en ${model.id}`,
  );
  const rotorIndex = asset.nodes.findIndex((node) => node.name === 'RotorAssembly');
  const rotorAnimated = asset.animations?.some((animation) =>
    animation.channels.some((channel) => {
      if (channel.target.node !== rotorIndex || channel.target.path !== 'rotation') return false;
      const sampler = animation.samplers[channel.sampler];
      return (
        sampler &&
        asset.accessors[sampler.input]?.count > 1 &&
        asset.accessors[sampler.output]?.count > 1
      );
    }),
  );
  assert(rotorAnimated, `Sin animación de rotación del rotor: ${path}`);
  let triangles = 0;
  for (const mesh of asset.meshes) {
    for (const primitive of mesh.primitives) {
      assert(
        primitive.extensions?.KHR_draco_mesh_compression,
        `Geometría sin compresión Draco: ${path}`,
      );
      assert(
        primitive.mode === undefined || primitive.mode === 4,
        `Modo de geometría no triangular: ${path}`,
      );
      const accessorIndex = primitive.indices ?? primitive.attributes.POSITION;
      const count = asset.accessors[accessorIndex]?.count;
      assert(
        typeof count === 'number' && Number.isInteger(count) && count > 0,
        `Geometría vacía: ${path}`,
      );
      triangles += count / 3;
    }
  }
  return { bytes: buffer.length, triangles };
}

const ajv = new Ajv({ allErrors: true, strict: false });
const schema = JSON.parse(readFileSync('src/data/turbine.schema.json', 'utf8'));
const validate = ajv.compile(schema);
const ids = new Set<string>();
let assetsChecked = 0;
for (const file of readdirSync('src/data/models').filter((f) => f.endsWith('.json'))) {
  const model = JSON.parse(readFileSync('src/data/models/' + file, 'utf8')) as TurbineModel;
  assert(validate(model), `${file}: ${ajv.errorsText(validate.errors)}`);
  assert(!ids.has(model.id), `ID duplicado: ${model.id}`);
  ids.add(model.id);
  const scenario = model.simulation;
  assert(
    scenario.cutInMS < scenario.fixedWindMS && scenario.fixedWindMS < scenario.cutOutMS,
    `Viento fijo fuera del rango: ${model.id}`,
  );
  assert(
    scenario.cutInMS < scenario.ratedWindMS && scenario.ratedWindMS < scenario.cutOutMS,
    `Umbrales incoherentes: ${model.id}`,
  );
  const detailed = inspectAsset('public/' + model.asset.glb, model);
  const reduced =
    model.asset.lod === model.asset.glb
      ? detailed
      : inspectAsset('public/' + model.asset.lod, model);
  assetsChecked += model.asset.lod === model.asset.glb ? 1 : 2;
  assert(
    reduced.triangles <= detailed.triangles,
    `LOD con más triángulos que el interior: ${model.id}`,
  );
  console.log(
    `${model.id}: ${Math.ceil(detailed.bytes / 1024)} KiB / ` +
      `${Math.ceil(reduced.bytes / 1024)} KiB; ` +
      `${Math.round(detailed.triangles)} / ${Math.round(reduced.triangles)} triángulos (interior/exterior).`,
  );
}
console.log(
  `OK: ${ids.size} JSON, ${assetsChecked} GLB, componentes, LOD, Draco, animación y arquitectura.`,
);
