import { Suspense, useEffect, useMemo, useRef } from 'react';
import { Canvas, useFrame, type ThreeEvent } from '@react-three/fiber';
import {
  OrbitControls,
  useGLTF,
  useAnimations,
  useProgress,
  Line,
  AdaptiveDpr,
} from '@react-three/drei';
import { gsap } from 'gsap';
import * as THREE from 'three';
import type { TurbineModel } from '../data/types';
import { useSimulator, type ComponentId } from '../store/useSimulator';
import { normalOperation } from '../simulation/normalOperation';
import type { ComponentRef } from 'react';

const base = import.meta.env.BASE_URL;
const groupOffsets: Record<string, [number, number, number]> = {
  RotorAssembly: [-3, 0, 0],
  MainShaft: [-1, 1, 0],
  Gearbox: [0, 3, 0],
  Generator: [1, 2, 0],
  Converter: [3, 2, 2],
  Transformer: [3, -1, -2],
  Nacelle: [0, 5, 0],
  Yaw: [0, -1, 0],
};
function componentOf(object: THREE.Object3D): ComponentId | null {
  let node: THREE.Object3D | null = object;
  while (node) {
    if (node.userData.component) return node.userData.component as ComponentId;
    node = node.parent;
  }
  return null;
}

function Asset({ model }: { model: TurbineModel }) {
  const { view, exploded, selected, playing, setSelected } = useSimulator();
  const url = base + (view === 'exterior' ? model.asset.lod : model.asset.glb);
  const gltf = useGLTF(url, base + 'draco/');
  const scene = useMemo(() => {
    const clone = gltf.scene.clone(true);
    clone.traverse((o) => {
      if (o instanceof THREE.Mesh) {
        o.material = Array.isArray(o.material)
          ? o.material.map((m) => m.clone())
          : o.material.clone();
        o.castShadow = false;
      }
    });
    return clone;
  }, [gltf.scene]);
  const { actions, mixer } = useAnimations(gltf.animations, scene);
  const estimates = normalOperation(model.simulation);
  useEffect(() => {
    Object.values(actions).forEach((a) => a?.reset().play());
    return () => {
      Object.values(actions).forEach((a) => a?.stop());
    };
  }, [actions]);
  useEffect(() => {
    mixer.timeScale = playing ? estimates.rotorRPM / 12 : 0;
  }, [playing, estimates.rotorRPM, mixer]);
  useEffect(() => {
    scene.traverse((o) => {
      if (!(o instanceof THREE.Mesh)) return;
      const materials = Array.isArray(o.material) ? o.material : [o.material];
      const shell = o.name === 'Shell';
      const fade =
        view === 'interior' && (shell || componentOf(o) === 'blades' || o.name === 'HubCover');
      o.raycast = shell && view === 'interior' ? () => {} : THREE.Mesh.prototype.raycast;
      materials.forEach((material) => {
        const mat = material as THREE.MeshStandardMaterial;
        mat.transparent = fade;
        mat.opacity = fade ? (shell ? 0.1 : 0.35) : 1;
        mat.depthWrite = !fade;
        mat.side = shell ? THREE.DoubleSide : THREE.FrontSide;
        mat.emissive.set(componentOf(o) === selected ? '#64d9c2' : '#000000');
        mat.emissiveIntensity = 0.35;
        mat.needsUpdate = true;
      });
    });
  }, [scene, view, selected]);
  useEffect(() => {
    const animations: gsap.core.Tween[] = [];
    scene.traverse((o) => {
      const offset = groupOffsets[o.name];
      if (!offset) return;
      if (!o.userData.originalPosition) o.userData.originalPosition = o.position.clone();
      const p = o.userData.originalPosition as THREE.Vector3;
      animations.push(
        gsap.to(o.position, {
          x: p.x + (exploded ? offset[0] : 0),
          y: p.y + (exploded ? offset[1] : 0),
          z: p.z + (exploded ? offset[2] : 0),
          duration: 0.65,
          ease: 'power2.inOut',
        }),
      );
    });
    return () => animations.forEach((a) => a.kill());
  }, [scene, exploded]);
  useEffect(() => {
    for (let i = 0; i < 3; i++) {
      const p = scene.getObjectByName(`Pitch_${i}`);
      if (p) p.rotation.y = THREE.MathUtils.degToRad(estimates.pitchDeg);
    }
  }, [scene, estimates.pitchDeg]);
  useEffect(
    () => () => {
      scene.traverse((o) => {
        if (o instanceof THREE.Mesh) {
          (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => m.dispose());
        }
      });
    },
    [scene],
  );
  useFrame((_, dt) => {
    if (!playing) return;
    const ratio = model.specs.gearbox.value === true ? model.simulation.gearRatio : 1;
    const rotor = scene.getObjectByName('GeneratorRotor');
    if (rotor)
      rotor.rotation.x -= ((Math.min(dt, 0.08) * estimates.rotorRPM * Math.PI) / 30) * ratio;
    for (let i = 0; i < 3; i++) {
      const cog = scene.getObjectByName(`GearWheel_${i}`);
      if (cog)
        cog.rotation.x += ((Math.min(dt, 0.08) * estimates.rotorRPM * Math.PI) / 30) * (i + 1) * 3;
    }
  });
  const click = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    setSelected(componentOf(e.object));
  };
  return <primitive object={scene} onClick={click} />;
}

function EnergyFlow({ model }: { model: TurbineModel }) {
  const { view, playing, exploded } = useSimulator();
  const direct = model.specs.gearbox.value === false;
  const dfig = model.specs.generator.value?.startsWith('DFIG');
  const curves = useMemo(() => {
    const gx = direct ? -1.9 : 1.9;
    // DFIG includes stator bypass and rotor converter branch.
    const paths = dfig
      ? [
          [
            [gx, 0, -1.1],
            [2.5, 0, -1.4],
            [3.2, -0.3, -0.85],
          ],
          [
            [gx, 0.2, 1.1],
            [3.4, 0.2, 0.9],
            [4, 0.2, 0],
            [3.2, -0.3, -0.85],
          ],
        ]
      : [
          [
            [-3, 0, 0],
            [gx, 0, 0],
            [3.4, 0.2, 0.9],
            [4, 0.2, 0],
            [3.2, -0.3, -0.85],
          ],
        ];
    return paths.map(
      (p) =>
        new THREE.CatmullRomCurve3(
          p.map((v) => new THREE.Vector3(...(v as [number, number, number]))),
        ),
    );
  }, [direct, dfig]);
  const particles = useRef<(THREE.Mesh | null)[]>([]);
  useFrame(({ clock }) => {
    if (!playing) return;
    curves.forEach((curve, c) => {
      for (let i = 0; i < 6; i++) {
        particles.current[c * 6 + i]?.position.copy(
          curve.getPoint((clock.elapsedTime * 0.12 + i / 6) % 1),
        );
      }
    });
  });
  if (view !== 'interior' || exploded) return null;
  return (
    <group>
      {curves.map((curve, c) => (
        <group key={c}>
          <Line
            points={curve.getPoints(32)}
            color={c === 1 ? '#8daff1' : '#68e3c6'}
            lineWidth={1.4}
            transparent
            opacity={0.6}
          />
          {Array.from({ length: 6 }, (_, i) => (
            <mesh
              key={i}
              ref={(el) => {
                particles.current[c * 6 + i] = el;
              }}
            >
              <sphereGeometry args={[0.065, 8, 6]} />
              <meshBasicMaterial color={c === 1 ? '#a8c9ff' : '#8effde'} />
            </mesh>
          ))}
        </group>
      ))}
    </group>
  );
}

function CameraRig() {
  const ref = useRef<ComponentRef<typeof OrbitControls>>(null);
  const { view, resetCount, modelId } = useSimulator();
  useEffect(() => {
    const controls = ref.current;
    if (!controls) return;
    const p = view === 'interior' ? [-11, 5.5, 13] : [-16, 5, 24];
    const target = view === 'interior' ? [0, 0, 0] : [-1, -1, 0];
    const cameraTween = gsap.to(controls.object.position, {
      x: p[0],
      y: p[1],
      z: p[2],
      duration: 0.8,
      onUpdate: () => controls.update(),
    });
    const targetTween = gsap.to(controls.target, {
      x: target[0],
      y: target[1],
      z: target[2],
      duration: 0.8,
    });
    return () => {
      cameraTween.kill();
      targetTween.kill();
    };
  }, [view, resetCount, modelId]);
  return (
    <OrbitControls
      ref={ref}
      makeDefault
      enableDamping
      dampingFactor={0.08}
      minDistance={7}
      maxDistance={85}
      maxPolarAngle={Math.PI * 0.85}
    />
  );
}

function LoadingStatus() {
  const { active } = useProgress();
  return active ? (
    <div className="scene-loading-overlay" role="status">
      Cargando aerogenerador…
    </div>
  ) : null;
}
export default function TurbineScene({ model }: { model: TurbineModel }) {
  return (
    <div className="scene-container">
      <Canvas
        camera={{ position: [-16, 5, 24], fov: 40, near: 0.1, far: 200 }}
        dpr={[1, 1.6]}
        gl={{ antialias: true, powerPreference: 'high-performance' }}
        fallback={
          <div className="canvas-message">
            Tu navegador no ofrece WebGL. La ficha y el catálogo siguen disponibles.
          </div>
        }
        onPointerMissed={() => useSimulator.getState().setSelected(null)}
      >
        <color attach="background" args={['#142231']} />
        <fog attach="fog" args={['#142231', 75, 160]} />
        <ambientLight intensity={1.5} />
        <hemisphereLight args={['#d5f1ff', '#475b72', 2]} />
        <directionalLight position={[-10, 14, 15]} intensity={3} />
        <directionalLight position={[8, 5, -8]} color="#8ce8db" intensity={2} />
        <Suspense fallback={null}>
          <Asset model={model} />
          <EnergyFlow model={model} />
        </Suspense>
        <CameraRig />
        <AdaptiveDpr pixelated />
      </Canvas>
      <LoadingStatus />
    </div>
  );
}
