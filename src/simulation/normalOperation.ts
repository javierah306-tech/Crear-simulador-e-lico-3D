import type { SimulationSpec } from '../data/types';
/** Educational steady-state surrogate; outputs are estimates, never telemetry. */
export function normalOperation(s: SimulationSpec, wind = s.fixedWindMS) {
  if (!Number.isFinite(wind)) throw new Error('El viento debe ser finito');
  const operating = wind >= s.cutInMS && wind < s.cutOutMS;
  const fraction = Math.max(
    0,
    Math.min(1, (wind ** 3 - s.cutInMS ** 3) / (s.ratedWindMS ** 3 - s.cutInMS ** 3)),
  );
  const powerMW = operating ? s.ratedPowerMW * fraction : 0;
  // Below rated, tip-speed ratio determines speed; above rated, hold rated RPM.
  const rotorRPM = operating
    ? Math.min(
        s.maxRotorRPM,
        (60 * s.tipSpeedRatio * Math.min(wind, s.ratedWindMS)) / (Math.PI * s.rotorDiameterM),
      )
    : 0;
  const pitchDeg = operating
    ? s.pitchBaseDeg + Math.max(0, wind - s.ratedWindMS) * s.pitchGainDegPerMS
    : 0;
  return { powerMW, rotorRPM, pitchDeg, operating, wind };
}
