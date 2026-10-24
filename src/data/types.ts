export type EvidenceScope = 'installed' | 'family' | 'missing';
export interface Fact<T> {
  value: T | null;
  source: string | null;
  scope: EvidenceScope;
  note: string;
}
export interface TurbineSpecs {
  ratedPowerMW: Fact<number>;
  rotorDiameterM: Fact<number>;
  hubHeightM: Fact<number>;
  bladeCount: Fact<number>;
  generator: Fact<string>;
  gearbox: Fact<boolean>;
  powerControl: Fact<string>;
  cutInMS: Fact<number>;
  ratedWindMS: Fact<number>;
  cutOutMS: Fact<number>;
  converter: Fact<string>;
}
export interface Park {
  name: string;
  references: string[];
  evidence: string;
  note: string;
  hubHeightM: Fact<number>;
  installationProvider: string | null;
}
export interface SimulationSpec {
  fixedWindMS: number;
  ratedPowerMW: number;
  cutInMS: number;
  ratedWindMS: number;
  cutOutMS: number;
  tipSpeedRatio: number;
  maxRotorRPM: number;
  pitchBaseDeg: number;
  pitchGainDegPerMS: number;
  gearRatio: number;
  bladeCount: number;
  rotorDiameterM: number;
  hubHeightM: number;
  assumptions: string[];
}
export interface EngineeringReference {
  id: string;
  title: string;
  publisher: string;
  url: string;
  pages: string;
}
export interface EngineeringSpec {
  reviewDate: string;
  geometryScope: string;
  identity: string;
  layoutCode: 'direct' | 'one-planetary-two-parallel' | 'two-planetary-one-parallel';
  layout: string;
  pitchDrive: Fact<string>;
  gearRatio: Fact<number>;
  generatorVoltageV: Fact<number>;
  generatorSpeedRPM: Fact<number>;
  transformer: Fact<string>;
  references: EngineeringReference[];
}
export interface LandscapeSite {
  id: string;
  parkName: string;
  municipality: string;
  region: string;
  preset:
    'valley-crops' | 'alluvial-valley' | 'coastal-forestry' | 'rural-mosaic' | 'interior-hills';
  biome: string;
  description: string;
  seed: number;
  sitingNote: string;
  sources: { title: string; url: string; publisher: string }[];
}
export interface TurbineModel {
  id: string;
  manufacturer: string;
  model: string;
  supplier: Fact<string>;
  parks: Park[];
  specs: TurbineSpecs;
  notes: string[];
  simulation: SimulationSpec;
  engineering: EngineeringSpec;
  landscapes: LandscapeSite[];
  asset: { glb: string; lod: string; schematic: boolean };
}
