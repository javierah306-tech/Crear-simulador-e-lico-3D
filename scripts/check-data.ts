import Ajv from 'ajv';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import assert from 'node:assert/strict';
import type { TurbineModel } from '../src/data/types';
const ajv = new Ajv({ allErrors: true, strict: false });
const schema = JSON.parse(readFileSync('src/data/turbine.schema.json', 'utf8'));
const validate = ajv.compile(schema);
const ids = new Set<string>();
for (const file of readdirSync('src/data/models').filter((f) => f.endsWith('.json'))) {
  const m = JSON.parse(readFileSync('src/data/models/' + file, 'utf8')) as TurbineModel;
  assert(validate(m), `${file}: ${ajv.errorsText(validate.errors)}`);
  assert(!ids.has(m.id), 'ID duplicado');
  ids.add(m.id);
  const s = m.simulation;
  assert(s.cutInMS < s.fixedWindMS && s.fixedWindMS < s.cutOutMS, 'Viento fijo fuera del rango');
  assert(s.cutInMS < s.ratedWindMS && s.ratedWindMS < s.cutOutMS, 'Umbrales incoherentes');
  for (const key of ['glb', 'lod'] as const) {
    const path = 'public/' + m.asset[key];
    assert(existsSync(path), `Falta ${path}`);
    const buffer = readFileSync(path);
    assert.equal(buffer.toString('ascii', 0, 4), 'glTF');
    assert.equal(buffer.readUInt32LE(4), 2);
    const json = JSON.parse(buffer.toString('utf8', 20, 20 + buffer.readUInt32LE(12)));
    assert(json.extensionsRequired.includes('KHR_draco_mesh_compression'), 'Sin Draco');
    assert(json.animations?.length > 0, 'Sin animación glTF');
    const gear = json.nodes.some((n: { name: string }) => n.name === 'Gearbox');
    assert.equal(gear, m.specs.gearbox.value === true, `Multiplicadora incorrecta en ${m.id}`);
    assert(
      json.nodes.some((n: { name: string }) => n.name === 'RotorAssembly'),
      'Sin rotor seleccionable',
    );
  }
}
console.log(`OK: ${ids.size} JSON, geometrías, LOD, Draco, animaciones y arquitectura.`);
