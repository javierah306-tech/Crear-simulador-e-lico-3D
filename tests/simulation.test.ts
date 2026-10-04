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
