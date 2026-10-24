import { useMemo, useRef, useLayoutEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sky } from '@react-three/drei';
import * as THREE from 'three';
import type { LandscapeSite, TurbineModel } from '../data/types';
import { useSimulator } from '../store/useSimulator';
import { normalOperation } from '../simulation/normalOperation';

export const WORLD_SCALE = 30.8 / 87;
export function selectedLandscape(model: TurbineModel, siteId: string | null) {
  return model.landscapes.find((site) => site.id === siteId) ?? model.landscapes[0];
}
function random(seed: number) {
  let value = seed >>> 0;
  return () => {
    value = (Math.imul(value, 1664525) + 1013904223) >>> 0;
    return value / 4294967296;
  };
}
function settings(site: LandscapeSite) {
  const coastal = site.preset === 'coastal-forestry';
  const hills = site.preset === 'interior-hills';
  return {
    relief: coastal ? 8 : hills ? 6 : site.preset === 'rural-mosaic' ? 2.2 : 0.8,
    treeCount: coastal ? 620 : hills ? 520 : site.preset === 'alluvial-valley' ? 320 : 240,
    grass: coastal ? '#79995e' : hills ? '#8f9d62' : '#a7b777',
    patches: coastal
      ? ['#708b52', '#a6ad72', '#8d9d5e', '#acb889']
      : ['#b2b379', '#bca66d', '#92a763', '#c4b47d', '#7e9659'],
    sky: coastal ? '#dce6e5' : '#dce9ed',
  };
}
export function terrainHeight(x: number, z: number, site: LandscapeSite) {
  const { relief } = settings(site);
  const phase = site.seed * 0.12;
  const wave = (a: number, b: number) =>
    Math.sin(a * 0.022 + phase) * Math.cos(b * 0.018 - phase) +
    0.35 * Math.sin(a * 0.047 + b * 0.029);
  const flatten = THREE.MathUtils.smoothstep(Math.hypot(x, z), 7, 25);
  return (wave(x, z) - wave(0, 0)) * relief * flatten;
}
function Terrain({ site }: { site: LandscapeSite }) {
  const geometry = useMemo(() => {
    const g = new THREE.PlaneGeometry(760, 760, 120, 120);
    g.rotateX(-Math.PI / 2);
    const position = g.attributes.position;
    const colors = new Float32Array(position.count * 3);
    const palette = settings(site).patches.map((color) => new THREE.Color(color));
    const grass = new THREE.Color(settings(site).grass);
    for (let i = 0; i < position.count; i++) {
      const x = position.getX(i),
        z = position.getZ(i);
      position.setY(i, terrainHeight(x, z, site));
      const a = Math.floor((x + 380 + site.seed * 2) / 39),
        b = Math.floor((z + 380) / 48);
      const hash = Math.abs(Math.imul(a + 21, 73856093) ^ Math.imul(b + site.seed, 19349663));
      const color = palette[hash % palette.length].clone();
      const edge = Math.min((x + 1000) % 39, (z + 1000) % 48);
      if (edge < 2 || Math.hypot(x, z) < 12) color.lerp(grass, 0.65);
      color.multiplyScalar(0.96 + 0.04 * Math.sin(x * 0.6 + z * 0.4));
      color.toArray(colors, i * 3);
    }
    g.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    g.computeVertexNormals();
    return g;
  }, [site]);
  return (
    <mesh geometry={geometry} receiveShadow raycast={() => {}}>
      <meshStandardMaterial vertexColors roughness={1} />
    </mesh>
  );
}
// Match the rendered terrain triangles so the road does not cut through hills.
function surfaceHeight(x: number, z: number, site: LandscapeSite) {
  const step = 760 / 120;
  const ix = Math.floor((x + 380) / step),
    iz = Math.floor((z + 380) / step);
  const x0 = ix * step - 380,
    z0 = iz * step - 380;
  const u = (x - x0) / step,
    v = (z - z0) / step;
  const a = terrainHeight(x0, z0, site),
    b = terrainHeight(x0, z0 + step, site);
  const c = terrainHeight(x0 + step, z0 + step, site),
    d = terrainHeight(x0 + step, z0, site);
  return u + v <= 1 ? a + u * (d - a) + v * (b - a) : c + (1 - u) * (b - c) + (1 - v) * (d - c);
}
function AccessRoad({ site }: { site: LandscapeSite }) {
  const geometry = useMemo(() => {
    const points = [
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(-18, 0, 18),
      new THREE.Vector3(-42, 0, 40),
      new THREE.Vector3(-80, 0, 110),
      new THREE.Vector3(-175, 0, 200),
      new THREE.Vector3(-270, 0, 330),
    ];
    if (site.seed % 2)
      points.forEach((p) => {
        p.x *= -1;
      });
    const curve = new THREE.CatmullRomCurve3(points);
    const vertices: number[] = [],
      indices: number[] = [];
    const segments = 220;
    for (let i = 0; i <= segments; i++) {
      const center = curve.getPoint(i / segments),
        tangent = curve.getTangent(i / segments);
      const n = new THREE.Vector3(-tangent.z, 0, tangent.x).normalize().multiplyScalar(1.65);
      for (const sign of [-1, 1]) {
        const x = center.x + n.x * sign,
          z = center.z + n.z * sign;
        vertices.push(x, surfaceHeight(x, z, site) + 0.12, z);
      }
      if (i < segments) {
        const a = i * 2;
        indices.push(a, a + 2, a + 1, a + 1, a + 2, a + 3);
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    g.setIndex(indices);
    g.computeVertexNormals();
    return g;
  }, [site]);
  return (
    <mesh geometry={geometry} raycast={() => {}}>
      <meshStandardMaterial color="#ad9e80" roughness={1} side={THREE.DoubleSide} />
    </mesh>
  );
}
function Vegetation({ site }: { site: LandscapeSite }) {
  const trunks = useRef<THREE.InstancedMesh>(null),
    crowns = useRef<THREE.InstancedMesh>(null),
    tips = useRef<THREE.InstancedMesh>(null);
  const trees = useMemo(() => {
    const rng = random(site.seed),
      result: {
        x: number;
        z: number;
        height: number;
        radius: number;
        pine: boolean;
        tint: number;
      }[] = [];
    const count = settings(site).treeCount;
    for (let i = 0; i < count; i++) {
      let x = (rng() - 0.5) * 620,
        z = (rng() - 0.5) * 620;
      if (site.preset === 'coastal-forestry' || site.preset === 'interior-hills') {
        const cluster = i % 5;
        const cx = [-125, 155, -205, 195, 35][cluster],
          cz = [-90, -145, 145, 150, -240][cluster];
        x = cx + (rng() - 0.5) * 95;
        z = cz + (rng() - 0.5) * 100;
      } else {
        // Hedgerows and shelterbelts, rather than a uniform invented forest.
        if (i % 2) x = Math.round(x / 62) * 62 + (rng() - 0.5) * 7;
        else z = Math.round(z / 68) * 68 + (rng() - 0.5) * 7;
      }
      if (Math.hypot(x, z) < 20) continue;
      const height = 2.3 + rng() * 3.4;
      result.push({
        x,
        z,
        height,
        radius: 0.8 + rng() * 0.9,
        pine: rng() < (site.preset === 'coastal-forestry' ? 0.7 : 0.25),
        tint: rng(),
      });
    }
    return result;
  }, [site]);
  useLayoutEffect(() => {
    if (!trunks.current || !crowns.current || !tips.current) return;
    const dummy = new THREE.Object3D();
    trees.forEach((tree, index) => {
      const base = terrainHeight(tree.x, tree.z, site);
      dummy.position.set(tree.x, base + tree.height * 0.25, tree.z);
      dummy.scale.set(0.12, tree.height * 0.5, 0.12);
      dummy.updateMatrix();
      trunks.current!.setMatrixAt(index, dummy.matrix);
      dummy.position.y = base + tree.height * 0.66;
      dummy.scale.set(tree.radius, tree.height * 0.42, tree.radius * 0.85);
      dummy.updateMatrix();
      crowns.current!.setMatrixAt(index, dummy.matrix);
      dummy.position.y = base + tree.height * 0.91;
      dummy.scale.set(
        tree.pine ? tree.radius * 0.84 : tree.radius * 0.65,
        tree.pine ? tree.height * 0.45 : tree.height * 0.2,
        tree.radius * 0.72,
      );
      dummy.updateMatrix();
      tips.current!.setMatrixAt(index, dummy.matrix);
      const color = new THREE.Color().setHSL(
        0.22 + tree.tint * 0.08,
        0.28,
        0.22 + tree.tint * 0.09,
      );
      crowns.current!.setColorAt(index, color);
      tips.current!.setColorAt(index, color.clone().multiplyScalar(1.1));
    });
    for (const ref of [trunks, crowns, tips]) {
      ref.current!.instanceMatrix.needsUpdate = true;
      ref.current!.computeBoundingSphere();
    }
    if (crowns.current.instanceColor) crowns.current.instanceColor.needsUpdate = true;
    if (tips.current.instanceColor) tips.current.instanceColor.needsUpdate = true;
  }, [trees, site]);
  return (
    <group raycast={() => {}}>
      <instancedMesh ref={trunks} args={[undefined, undefined, trees.length]}>
        <cylinderGeometry args={[0.7, 1, 1, 5]} />
        <meshStandardMaterial color="#78664a" roughness={1} />
      </instancedMesh>
      <instancedMesh ref={crowns} args={[undefined, undefined, trees.length]}>
        <icosahedronGeometry args={[1, 1]} />
        <meshStandardMaterial color="white" roughness={1} />
      </instancedMesh>
      <instancedMesh ref={tips} args={[undefined, undefined, trees.length]}>
        <coneGeometry args={[1, 1, 7]} />
        <meshStandardMaterial color="white" roughness={1} />
      </instancedMesh>
    </group>
  );
}
function NeighbourTurbines({
  model,
  site,
  ground,
}: {
  model: TurbineModel;
  site: LandscapeSite;
  ground: number;
}) {
  const rotors = useRef<(THREE.Group | null)[]>([]);
  const playing = useSimulator((state) => state.playing);
  const h = -ground,
    r = (model.simulation.rotorDiameterM * WORLD_SCALE) / 2;
  const positions =
    model.manufacturer === 'Gamesa'
      ? [
          [-145, -175],
          [160, -185],
          [215, 100],
        ]
      : [
          [-145, -175],
          [160, -185],
          [240, -50],
          [-210, 110],
        ];
  const rpm = normalOperation(model.simulation).rotorRPM;
  useFrame((_, dt) => {
    if (playing)
      rotors.current.forEach((rotor) => {
        if (rotor) rotor.rotation.x -= (Math.min(dt, 0.1) * rpm * Math.PI) / 30;
      });
  });
  return (
    <group raycast={() => {}}>
      {positions.map(([x, z], index) => (
        <group key={index} position={[x, terrainHeight(x, z, site), z]}>
          <mesh position={[0, h / 2, 0]}>
            <cylinderGeometry args={[0.55, 0.95, h, 10]} />
            <meshStandardMaterial color="#e5e7dd" roughness={0.55} />
          </mesh>
          <group position={[1, h, 0]}>
            <mesh rotation={model.manufacturer === 'Gamesa' ? [0, 0, Math.PI / 2] : [0, 0, 0]}>
              {model.manufacturer === 'Goldwind' ? (
                <sphereGeometry args={[2, 12, 8]} />
              ) : model.manufacturer === 'Gamesa' ? (
                <capsuleGeometry args={[1.4, 5.1, 4, 10]} />
              ) : (
                <boxGeometry args={[model.manufacturer === 'Nordex' ? 9 : 7.5, 2.8, 2.8]} />
              )}
              <meshStandardMaterial color="#e5e7dd" roughness={0.5} />
            </mesh>
            {model.manufacturer === 'Nordex' && (
              <mesh position={[3.8, 0, 0]}>
                <boxGeometry args={[1.4, 2.85, 2.85]} />
                <meshStandardMaterial color="#b33c2a" />
              </mesh>
            )}
            {model.manufacturer === 'Vestas' && (
              <mesh position={[2.5, 1.8, 0]}>
                <boxGeometry args={[1.9, 1.1, 2]} />
                <meshStandardMaterial color="#e5e7dd" />
              </mesh>
            )}
          </group>
          <group
            ref={(el) => {
              rotors.current[index] = el;
            }}
            position={[-3, h, 0]}
          >
            <mesh rotation={[0, 0, Math.PI / 2]}>
              <coneGeometry args={[0.65, 1.5, 12]} />
              <meshStandardMaterial color="#f5f2e7" />
            </mesh>
            {[0, 1, 2].map((i) => (
              <group key={i} rotation={[(i * Math.PI * 2) / 3, 0, 0]}>
                <mesh position={[0, r / 2, 0]} rotation={[0, Math.PI / 2, 0.025]}>
                  <boxGeometry args={[0.19, r, 0.7]} />
                  <meshStandardMaterial color="#efeee2" roughness={0.55} />
                </mesh>
              </group>
            ))}
          </group>
        </group>
      ))}
    </group>
  );
}
export default function ParkEnvironment({
  model,
  site,
}: {
  model: TurbineModel;
  site: LandscapeSite;
}) {
  const ground = -model.simulation.hubHeightM * WORLD_SCALE - 0.22;
  const colors = settings(site);
  return (
    <>
      <color attach="background" args={[colors.sky]} />
      <fog attach="fog" args={[colors.sky, 90, 430]} />
      <Sky
        distance={600}
        sunPosition={[100, 75, -130]}
        turbidity={2.1}
        rayleigh={0.42}
        mieCoefficient={0.003}
        mieDirectionalG={0.77}
      />
      <group position={[0, ground, 0]}>
        <Terrain site={site} />
        <AccessRoad site={site} />
        <Vegetation site={site} />
        <mesh position={[0, 0.035, 0]} rotation={[-Math.PI / 2, 0, 0]} raycast={() => {}}>
          <circleGeometry args={[7.5, 40]} />
          <meshStandardMaterial color="#c2b79c" roughness={1} />
        </mesh>
        <mesh position={[0, 0.075, 0]} rotation={[-Math.PI / 2, 0, 0]} raycast={() => {}}>
          <circleGeometry args={[2.2, 32]} />
          <meshStandardMaterial color="#c9c8b8" roughness={0.9} />
        </mesh>
        <NeighbourTurbines model={model} site={site} ground={ground} />
      </group>
    </>
  );
}
