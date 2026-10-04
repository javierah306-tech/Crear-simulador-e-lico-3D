import type { Fact, TurbineModel, TurbineSpecs } from '../data/types';
export const specLabels: Record<keyof TurbineSpecs, string> = {
  ratedPowerMW: 'Potencia nominal',
  rotorDiameterM: 'Diámetro de rotor',
  hubHeightM: 'Altura de buje instalada',
  bladeCount: 'Número de palas',
  generator: 'Generador',
  gearbox: 'Multiplicadora',
  powerControl: 'Control de potencia',
  cutInMS: 'Viento de arranque',
  ratedWindMS: 'Viento nominal',
  cutOutMS: 'Viento de corte',
  converter: 'Convertidor',
};
export const specUnits: Partial<Record<keyof TurbineSpecs, string>> = {
  ratedPowerMW: 'MW',
  rotorDiameterM: 'm',
  hubHeightM: 'm',
  cutInMS: 'm/s',
  ratedWindMS: 'm/s',
  cutOutMS: 'm/s',
};
export function formatFact(f: Fact<unknown>, unit = '') {
  return f.value === null
    ? 'No documentado'
    : typeof f.value === 'boolean'
      ? f.value
        ? 'Sí'
        : 'No'
      : `${typeof f.value === 'number' ? f.value.toLocaleString('es-CL') : f.value}${unit ? ' ' + unit : ''}`;
}
export function TechnicalSheet({ model }: { model: TurbineModel }) {
  return (
    <div className="technical-sheet">
      <div className="sheet-heading">
        <span className="eyebrow">DATOS Y TRAZABILIDAD</span>
        <h3>Ficha técnica</h3>
      </div>
      <p className="small muted">
        Los datos de familia orientan la explicación y requieren confirmación para cada parque.
      </p>
      <dl>
        {Object.entries(specLabels).map(([key, label]) => {
          const k = key as keyof TurbineSpecs;
          const f = model.specs[k];
          return (
            <div className="spec-row" key={key}>
              <dt>{label}</dt>
              <dd>
                {formatFact(f, specUnits[k])}
                <span className={'scope ' + f.scope}>
                  {f.scope === 'installed'
                    ? 'Parque'
                    : f.scope === 'family'
                      ? 'Familia'
                      : 'Sin dato'}
                </span>
                <small>{f.source || f.note}</small>
                {f.value !== null && <small>{f.note}</small>}
              </dd>
            </div>
          );
        })}
      </dl>
      <div className="source-note">
        <strong>Fabricante / proveedor</strong>
        <p>
          {model.manufacturer}. {model.supplier.note}
        </p>
      </div>
      <h4>Parques documentados</h4>
      {model.parks.map((p) => (
        <div className="park-note" key={p.name}>
          <strong>
            {p.name} <span className="scope installed">{p.evidence}</span>
          </strong>
          <p>
            {p.references.join(' · ')} · {p.note || 'Identificación documentada en el informe.'}
          </p>
          <p>Altura instalada: {formatFact(p.hubHeightM, 'm')}</p>
          {p.hubHeightM.value !== null && <p>{p.hubHeightM.note}</p>}
          {p.installationProvider && <p>Instalación: {p.installationProvider}</p>}
        </div>
      ))}
      <details>
        <summary>Notas y límites de la ficha</summary>
        <ul>
          {model.notes.map((n) => (
            <li key={n}>{n}</li>
          ))}
        </ul>
      </details>
      <details>
        <summary>Supuestos de la simulación</summary>
        <ul>
          {model.simulation.assumptions.map((n) => (
            <li key={n}>{n}</li>
          ))}
        </ul>
        <p>
          Viento nominal usado: {model.simulation.ratedWindMS} m/s. Diámetro para cálculo de RPM:{' '}
          {model.simulation.rotorDiameterM} m. Potencia del escenario:{' '}
          {model.simulation.ratedPowerMW} MW. Estos valores no completan los campos documentales
          ausentes.
        </p>
      </details>
      <p className="small muted">
        Fuente base: informe Smartwind, versión 1.0, corte documental 3 de octubre de 2026. El
        catálogo no certifica el inventario vigente por unidad.
      </p>
    </div>
  );
}
