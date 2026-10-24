import { create } from 'zustand';
export type ComponentId =
  | 'blades'
  | 'hub'
  | 'rotor'
  | 'shaft'
  | 'gearbox'
  | 'generator'
  | 'converter'
  | 'transformer'
  | 'yaw'
  | 'pitch'
  | 'nacelle'
  | 'tower';
interface State {
  modelId: string;
  view: 'exterior' | 'interior' | 'park';
  siteId: string | null;
  setSite: (id: string) => void;
  exploded: boolean;
  selected: ComponentId | null;
  tab: 'explore' | 'catalog';
  playing: boolean;
  resetCount: number;
  setModel: (id: string) => void;
  setView: (v: State['view']) => void;
  setSelected: (id: ComponentId | null) => void;
  setTab: (t: State['tab']) => void;
  toggleExploded: () => void;
  togglePlaying: () => void;
  resetCamera: () => void;
}
export const useSimulator = create<State>((set) => ({
  modelId: 'goldwind-gw1500-87',
  view: 'exterior',
  siteId: null,
  setSite: (siteId) => set({ siteId, view: 'park', selected: null, exploded: false }),
  exploded: false,
  selected: null,
  tab: 'explore',
  playing: true,
  resetCount: 0,
  setModel: (modelId) => set({ modelId, siteId: null, selected: null, exploded: false }),
  setView: (view) => set({ view, selected: null, exploded: false }),
  setSelected: (selected) => set({ selected }),
  setTab: (tab) => set({ tab }),
  toggleExploded: () => set((s) => ({ view: 'interior', exploded: !s.exploded })),
  togglePlaying: () => set((s) => ({ playing: !s.playing })),
  resetCamera: () => set((s) => ({ resetCount: s.resetCount + 1 })),
}));
