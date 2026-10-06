import { Component, lazy, Suspense, useEffect, useState, useRef, type ReactNode } from 'react';
import {
  Wind,
  MapPin,
  ChevronRight,
  RotateCcw,
  Layers3,
  Maximize2,
  Box,
  X,
  Play,
  Pause,
  Info,
  Zap,
  Gauge,
  Compass,
  Menu,
  Leaf,
  ArrowRight,
  Radio,
} from 'lucide-react';
import { models, architecture } from './data/catalog';
import { components } from './data/components';
import { useSimulator, type ComponentId } from './store/useSimulator';
import { normalOperation } from './simulation/normalOperation';
import { TechnicalSheet, formatFact } from './components/TechnicalSheet';
import { Catalog } from './components/Catalog';
import type { TurbineModel } from './data/types';
const TurbineScene = lazy(() => import('./components/TurbineScene'));

class ViewerBoundary extends Component<{ children: ReactNode }, { error: boolean }> {
  state = { error: false };
  static getDerivedStateFromError() {
    return { error: true };
  }
  render() {
    return this.state.error ? (
      <div className="canvas-message">
        <Info />
        <h3>No se pudo cargar la vista 3D</h3>
        <p>Recarga la página para reintentar. Puedes seguir explorando los datos y componentes.</p>
      </div>
    ) : (
      this.props.children
    );
  }
}

function ModelGlyph({ direct }: { direct: boolean }) {
  return (
    <svg viewBox="0 0 42 42" fill="none" aria-hidden="true">
      <path d="M21 23v13M16 36h10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path
        d="m21 20-1.2-14c-.1-1.2 1.8-1.2 1.9 0L23 18.6M19.5 21.4 7.4 27.1c-1.1.5-2-1.1-1-1.8L18.8 18.7M22.5 20.6l10.3 9.2c.9.8-.4 2.1-1.3 1.4L20.4 23"
        fill="currentColor"
        fillOpacity=".14"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinejoin="round"
      />
      <circle
        cx="21"
        cy="21"
        r={direct ? 3.9 : 2.8}
        fill="currentColor"
        fillOpacity=".12"
        stroke="currentColor"
        strokeWidth="1.3"
      />
      <circle cx="21" cy="21" r=".8" fill="currentColor" />
    </svg>
  );
}
function componentIds(model: TurbineModel): ComponentId[] {
  const basic: ComponentId[] = ['blades', 'hub', 'rotor', 'shaft'];
  if (model.specs.gearbox.value === true) basic.push('gearbox');
  basic.push('generator', 'converter', 'transformer', 'yaw');
  if (model.specs.powerControl.value === 'pitch') basic.push('pitch');
  basic.push('nacelle', 'tower');
  return basic;
}
function ComponentPanel({ id, model }: { id: ComponentId; model: TurbineModel }) {
  const part = components[id];
  const { setSelected } = useSimulator();
  const tech =
    id === 'generator'
      ? model.specs.generator
      : id === 'gearbox'
        ? model.specs.gearbox
        : id === 'converter'
          ? model.specs.converter
          : id === 'pitch'
            ? model.specs.powerControl
            : null;
  return (
    <div className="part-panel" role="region" aria-label={'Información de ' + part.name}>
      <div className="part-top">
        <span className="eyebrow">ANATOMÍA / DETALLE</span>
        <button
          aria-label="Cerrar componente"
          className="icon-button"
          onClick={() => setSelected(null)}
        >
          <X size={18} />
        </button>
      </div>
      <h3>
        <span style={{ background: part.color }} />
        {part.name}
      </h3>
      <p>{part.description}</p>
      {tech && (
        <div className="part-tech">
          <strong>{formatFact(tech)}</strong>
          <small>{tech.source || 'Configuración técnica no documentada.'}</small>
        </div>
      )}
      <p className="small muted">
        Detalle mecánico ilustrativo.{' '}
        {model.specs.gearbox.value === null
          ? 'La arquitectura instalada está pendiente de confirmar.'
          : 'Forma, escala y ubicación didácticas; no son planos de fabricación.'}
      </p>
    </div>
  );
}
function SheetModal({ model, close }: { model: TurbineModel; close: () => void }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current;
    dialog?.showModal();
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      dialog?.close();
      document.body.style.overflow = previous;
    };
  }, []);
  return (
    <dialog
      ref={ref}
      className="sheet-dialog native-dialog"
      aria-label={'Ficha técnica de ' + model.model}
      onCancel={close}
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          const r = e.currentTarget.getBoundingClientRect();
          if (
            e.clientX < r.left ||
            e.clientX > r.right ||
            e.clientY < r.top ||
            e.clientY > r.bottom
          )
            close();
        }
      }}
    >
      <div className="dialog-title">
        <div>
          <span className="eyebrow">{model.manufacturer}</span>
          <h2>{model.model}</h2>
        </div>
        <button autoFocus className="icon-button" aria-label="Cerrar ficha técnica" onClick={close}>
          <X />
        </button>
      </div>
      <TechnicalSheet model={model} />
    </dialog>
  );
}
function App() {
  const state = useSimulator();
  const model = models.find((m) => m.id === state.modelId) || models[0];
  const [sheet, setSheet] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const data = normalOperation(model.simulation);
  const ids = componentIds(model);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setSheet(false);
        state.setSelected(null);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [state]);
  const next = () =>
    state.setModel(models[(models.findIndex((m) => m.id === model.id) + 1) % models.length].id);
  return (
    <div className="app-shell">
      <header className="topbar">
        <a href="#main" className="skip-link">
          Saltar al contenido
        </a>
        <button
          className="brand"
          onClick={() => state.setTab('explore')}
          aria-label="Smartwind, explorador"
        >
          <span className="brand-symbol">
            <Leaf size={23} strokeWidth={1.7} />
          </span>
          <span>
            smartwind<span className="brand-sub">ENERGÍA QUE SE EXPLORA</span>
          </span>
        </button>
        <nav aria-label="Navegación principal">
          <button
            className={state.tab === 'explore' ? 'active' : ''}
            onClick={() => state.setTab('explore')}
          >
            Explorador 3D
          </button>
          <button
            className={state.tab === 'catalog' ? 'active' : ''}
            onClick={() => state.setTab('catalog')}
          >
            Catálogo técnico
          </button>
        </nav>
        <div className="region">
          <span className="region-dot" />
          <span>Biobío, Chile</span>
          <span className="open-access">ACCESO LIBRE</span>
        </div>
      </header>
      <main id="main">
        {state.tab === 'catalog' ? (
          <Catalog />
        ) : (
          <div className="explorer-layout">
            <aside
              className={'sidebar ' + (mobileMenu ? 'mobile-open' : '')}
              aria-label="Selector de aerogeneradores"
            >
              <div className="sidebar-heading">
                <span className="eyebrow">COLECCIÓN BIOBÍO</span>
                <h2>
                  Aerogeneradores <span>{models.length.toString().padStart(2, '0')}</span>
                </h2>
              </div>
              <p className="sidebar-caption">Nueve maneras de transformar el viento.</p>
              <div className="model-list">
                {models.map((m, i) => (
                  <button
                    key={m.id}
                    className={'model-card ' + (m.id === model.id ? 'selected' : '')}
                    onClick={() => {
                      state.setModel(m.id);
                      setMobileMenu(false);
                    }}
                    aria-pressed={m.id === model.id}
                  >
                    <span className="model-symbol">
                      <ModelGlyph direct={m.specs.gearbox.value === false} />
                      <span className="model-number">{(i + 1).toString().padStart(2, '0')}</span>
                    </span>
                    <span className="model-copy">
                      <span className="maker">{m.manufacturer}</span>
                      <strong>{m.model}</strong>
                      <span className="model-meta">
                        {m.specs.ratedPowerMW.value !== null
                          ? `${m.specs.ratedPowerMW.value.toLocaleString('es-CL')} MW`
                          : 'Potencia por confirmar'}{' '}
                        <span>·</span>{' '}
                        {m.specs.gearbox.value === false
                          ? 'Directo'
                          : m.specs.gearbox.value === true
                            ? 'Multiplicadora'
                            : 'Por confirmar'}
                      </span>
                    </span>
                    <ChevronRight size={16} />
                  </button>
                ))}
              </div>
              <div className="sidebar-footer">
                <Leaf size={20} strokeWidth={1.5} />
                <p>
                  Entender la energía es parte del cambio.
                  <span>Una experiencia educativa abierta.</span>
                </p>
              </div>
            </aside>
            <section className="viewer-workspace" aria-label="Simulador 3D">
              <div className="viewer-heading">
                <div>
                  <span className="eyebrow viewer-eyebrow">
                    EL VIENTO, POR DENTRO <span> / </span> EXPLORADOR 3D
                  </span>
                  <h1>
                    {model.manufacturer} <span>{model.model.split(' · ')[0]}</span>
                  </h1>
                  <p>
                    <MapPin size={14} />
                    {model.parks.map((p) => p.name).join(' · ')}
                    <span className="location-divider" /> {architecture(model)}
                  </p>
                </div>
                <button className="outline-button sheet-button" onClick={() => setSheet(true)}>
                  <Info size={16} strokeWidth={1.6} />
                  Ficha técnica
                </button>
                <button
                  className="icon-button mobile-selector"
                  aria-label={mobileMenu ? 'Ocultar modelos' : 'Mostrar modelos'}
                  aria-expanded={mobileMenu}
                  onClick={() => setMobileMenu(!mobileMenu)}
                >
                  <Menu />
                </button>
              </div>
              <div className="viewport">
                <div className="viewport-top">
                  <div className="view-switch" role="group" aria-label="Acercamientos de cámara">
                    <button
                      className={state.view === 'exterior' ? 'active' : ''}
                      onClick={() => state.setView('exterior')}
                    >
                      <Maximize2 size={16} />
                      Vista exterior
                    </button>
                    <button
                      className={state.view === 'interior' ? 'active' : ''}
                      onClick={() => state.setView('interior')}
                    >
                      <Box size={16} />
                      Vista interior
                    </button>
                  </div>
                  <span className={'operation-label ' + (state.playing ? 'is-live' : 'is-paused')}>
                    <span className="live-dot" />
                    <span className="operation-copy">
                      <strong>{state.playing ? 'EN VIVO' : 'EN PAUSA'}</strong>
                      <small>Operación normal</small>
                    </span>
                    <Radio size={17} strokeWidth={1.5} aria-hidden="true" />
                  </span>
                </div>
                <ViewerBoundary key={model.id}>
                  <Suspense fallback={<div className="canvas-message">Preparando visor 3D…</div>}>
                    <TurbineScene model={model} />
                  </Suspense>
                </ViewerBoundary>
                <div className="studio-label" aria-hidden="true">
                  <span className="studio-line" />
                  <span>{state.exploded ? 'VISTA DESPIEZADA' : 'ESTUDIO DE COMPONENTES'}</span>
                </div>
                <div className="scene-caption">
                  <span className="eyebrow">
                    {state.view === 'exterior'
                      ? '01 / VISTA DE GÓNDOLA Y ROTOR'
                      : '02 / INTERIOR TRASLÚCIDO'}
                  </span>
                  <span>
                    {state.view === 'exterior'
                      ? 'El viento se convierte en movimiento.'
                      : 'La ingeniería detrás de la energía.'}
                  </span>
                </div>
                <div className="camera-tools">
                  <button
                    className={'icon-button ' + (state.exploded ? 'active' : '')}
                    onClick={state.toggleExploded}
                    aria-label={state.exploded ? 'Reunir componentes' : 'Separar componentes'}
                    aria-pressed={state.exploded}
                    title="Vista de explosión"
                  >
                    <Layers3 size={19} />
                  </button>
                  <button
                    className="icon-button"
                    onClick={state.resetCamera}
                    aria-label="Restablecer cámara"
                    title="Restablecer cámara"
                  >
                    <RotateCcw size={19} />
                  </button>
                  <button
                    className="icon-button"
                    onClick={state.togglePlaying}
                    aria-label={state.playing ? 'Pausar animación' : 'Reanudar animación'}
                    title={state.playing ? 'Pausar animación' : 'Reanudar animación'}
                  >
                    {state.playing ? <Pause size={19} /> : <Play size={19} />}
                  </button>
                </div>
                <span className="orbit-hint">
                  Arrastra para orbitar · Pellizca o usa la rueda para acercar
                </span>
                {state.selected && <ComponentPanel id={state.selected} model={model} />}
                <button className="next-model" onClick={next}>
                  Siguiente modelo
                  <ChevronRight size={18} />
                </button>
              </div>
              <div className="readouts" aria-label="Estimaciones bajo un viento fijo">
                <div className="readouts-heading">
                  <span className="eyebrow">ESCENARIO NORMAL</span>
                  <span>Estimaciones didácticas · viento fijo</span>
                </div>
                <div>
                  <span className="metric-label">
                    <Wind size={16} />
                    Viento del escenario
                  </span>
                  <strong>
                    {data.wind.toLocaleString('es-CL')}
                    <small>m/s</small>
                  </strong>
                  <span className="metric-note">
                    <span className="tiny-dot" /> Condición fija
                  </span>
                </div>
                <div className="power-readout">
                  <span className="metric-label">
                    <Zap size={16} />
                    Potencia estimada
                  </span>
                  <strong>
                    {data.powerMW.toLocaleString('es-CL', { maximumFractionDigits: 2 })}
                    <small>MW</small>
                  </strong>
                  <span className="metric-note">Curva simplificada</span>
                </div>
                <div>
                  <span className="metric-label">
                    <Gauge size={16} />
                    Giro del rotor
                  </span>
                  <strong>
                    {data.rotorRPM.toLocaleString('es-CL', { maximumFractionDigits: 1 })}
                    <small>RPM</small>
                  </strong>
                  <span className="metric-note">Estimación cinemática</span>
                </div>
                <div>
                  <span className="metric-label">
                    <Compass size={16} />
                    Paso de pala
                  </span>
                  <strong>
                    {data.pitchDeg.toLocaleString('es-CL', { maximumFractionDigits: 1 })}
                    <small>°</small>
                  </strong>
                  <span className="metric-note">
                    {model.specs.powerControl.value === 'pitch'
                      ? 'Ángulo didáctico'
                      : 'Supuesto de animación'}
                  </span>
                </div>
              </div>
              <div className="energy-story" aria-label="Transformación de la energía">
                <span className="eyebrow">DE LA BRISA A LA RED</span>
                <div className="energy-steps">
                  <span>
                    <Wind size={16} /> Viento
                  </span>
                  <ArrowRight size={13} />
                  <span>Rotor</span>
                  <ArrowRight size={13} />
                  <span>Generador</span>
                  <ArrowRight size={13} />
                  <span>
                    <Zap size={15} /> Red
                  </span>
                </div>
                <span className="story-note">
                  {model.specs.gearbox.value === false
                    ? 'Accionamiento directo'
                    : model.specs.gearbox.value === true
                      ? 'Tren con multiplicadora'
                      : 'Arquitectura por confirmar'}
                </span>
              </div>
              <div className="components-section">
                <div className="components-heading">
                  <h2>Cada pieza tiene una historia.</h2>
                  <p>Toca una pieza o elige un componente para descubrir su función.</p>
                </div>
                <div className="component-list">
                  {ids.map((id) => (
                    <button
                      key={id}
                      className={state.selected === id ? 'active' : ''}
                      aria-pressed={state.selected === id}
                      onClick={() => {
                        state.setSelected(id);
                        if (
                          [
                            'shaft',
                            'gearbox',
                            'generator',
                            'converter',
                            'transformer',
                            'yaw',
                            'pitch',
                          ].includes(id)
                        )
                          state.setView('interior');
                        state.setSelected(id);
                      }}
                    >
                      <span style={{ background: components[id].color }} />
                      {components[id].name}
                    </button>
                  ))}
                </div>
              </div>
              <footer className="workspace-footer">
                <span>Geometría ilustrativa · Datos del informe y referencias de familia</span>
                <button className="text-button" onClick={() => setSheet(true)}>
                  Consultar fuentes y supuestos
                </button>
              </footer>
            </section>
          </div>
        )}
      </main>
      {sheet && <SheetModal model={model} close={() => setSheet(false)} />}
    </div>
  );
}
export default App;
