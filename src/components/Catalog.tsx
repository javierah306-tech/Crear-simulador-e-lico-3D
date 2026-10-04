import { models, architecture } from '../data/catalog';
import { formatFact } from './TechnicalSheet';
import { useSimulator } from '../store/useSimulator';
export function Catalog() {
  const { setModel, setTab } = useSimulator();
  return (
    <section className="catalog-page">
      <span className="eyebrow">DOCUMENTACIÓN DEL BIOBÍO</span>
      <h1>Un territorio, distintas tecnologías.</h1>
      <p>
        Compara los modelos identificados en el informe. «Familia» indica una referencia comercial,
        pendiente de confirmar para las unidades del parque.
      </p>
      <div className="catalog-table">
        <table>
          <caption>Modelos y fabricantes extraídos del corpus documental</caption>
          <thead>
            <tr>
              <th>Fabricante / modelo</th>
              <th>Parques</th>
              <th>Potencia</th>
              <th>Rotor</th>
              <th>Generador</th>
              <th>Transmisión</th>
              <th>Explorar</th>
            </tr>
          </thead>
          <tbody>
            {models.map((m) => (
              <tr key={m.id}>
                <th scope="row">
                  <small>{m.manufacturer}</small>
                  {m.model}
                </th>
                <td>{m.parks.map((p) => p.name).join(', ')}</td>
                <td>{formatFact(m.specs.ratedPowerMW, 'MW')}</td>
                <td>
                  {formatFact(m.specs.rotorDiameterM, 'm')}
                  <small>{m.specs.rotorDiameterM.scope === 'family' ? 'Familia' : ''}</small>
                </td>
                <td>
                  {formatFact(m.specs.generator)}
                  <small>{m.specs.generator.scope === 'family' ? 'Familia' : ''}</small>
                </td>
                <td>
                  {architecture(m)}
                  <small>{m.specs.gearbox.scope === 'family' ? 'Familia' : ''}</small>
                </td>
                <td>
                  <button
                    className="text-button"
                    onClick={() => {
                      setModel(m.id);
                      setTab('explore');
                    }}
                  >
                    Ver modelo
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="catalog-footnotes">
        <p>
          <strong>Las Peñas:</strong> cuatro G114; 2 MW por unidad y 8,4 MW de proyecto no permiten
          fijar una variante.
        </p>
        <p>
          <strong>San Matías:</strong> el informe contrasta «N163 V150» con un anexo que identifica
          Vestas V150 de 4,3 MW. Torre reportada: 140 m.
        </p>
        <p>
          <strong>Inventario pendiente:</strong> Lebu, Eólica Lebu II, Lebu Sur, El Arrebol, El
          Nogal y El Maitén requieren identificación técnica. No se asignan modelos por analogía.
        </p>
      </div>
    </section>
  );
}
