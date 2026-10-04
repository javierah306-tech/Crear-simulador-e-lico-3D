import type { TurbineModel } from './types';
const files = import.meta.glob<TurbineModel>('./models/*.json', { eager: true, import: 'default' });
export const models = Object.values(files).sort((a, b) =>
  a.id === 'goldwind-gw1500-87'
    ? -1
    : b.id === 'goldwind-gw1500-87'
      ? 1
      : a.manufacturer.localeCompare(b.manufacturer) || a.model.localeCompare(b.model),
);
export const architecture = (model: TurbineModel) =>
  model.specs.gearbox.value === false
    ? 'Accionamiento directo'
    : model.specs.gearbox.value === true
      ? 'Con multiplicadora'
      : 'Arquitectura por confirmar';
