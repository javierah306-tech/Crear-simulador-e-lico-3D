import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { normalOperation } from '../src/simulation/normalOperation.ts';
import type { TurbineModel } from '../src/data/types';
for (const file of readdirSync('src/data/models')) {
  const model = JSON.parse(readFileSync('src/data/models/' + file, 'utf8')) as TurbineModel;
  test(`${model.id}: límites y curva de potencia`, () => {
    const s = model.simulation;
    assert.equal(normalOperation(s, s.cutInMS - 0.1).powerMW, 0);
    assert.equal(normalOperation(s, s.cutInMS).powerMW, 0);
    assert.equal(normalOperation(s, s.ratedWindMS).powerMW, s.ratedPowerMW);
    assert.equal(normalOperation(s, s.cutOutMS).powerMW, 0);
    let last = 0;
    for (let wind = s.cutInMS; wind < s.cutOutMS; wind += 0.2) {
      const value = normalOperation(s, wind);
      assert(value.powerMW >= last);
      assert(value.powerMW <= s.ratedPowerMW);
      assert(value.rotorRPM <= s.maxRotorRPM);
      assert(value.pitchDeg >= 0);
      last = value.powerMW;
    }
    assert(normalOperation(s).operating);
    assert.throws(() => normalOperation(s, NaN));
  });
}

// Coener/Coordinador La Esperanza, table 3: rated generator1680 rpm,
// ratio118 and rated wind9.5 m/s. The simplified control is anchored there.
test('Envision: el punto nominal respeta los datos de diseño documentados', () => {
  const model = JSON.parse(
    readFileSync('src/data/models/envision-e110-21.json', 'utf8'),
  ) as TurbineModel;
  const result = normalOperation(model.simulation, model.simulation.ratedWindMS);
  assert(Math.abs(result.rotorRPM * model.simulation.gearRatio - 1680) < 1e-8);
  assert.equal(model.simulation.gearRatio, 118);
});
