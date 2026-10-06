import { Suspense, useEffect, useMemo, useRef, type ComponentRef } from 'react';
import { Canvas, useFrame, useThree, type ThreeEvent } from '@react-three/fiber';
import {
  OrbitControls,
  useGLTF,
  useAnimations,
  useProgress,
  Line,
  AdaptiveDpr,
  Environment,
  Lightformer,
} from '@react-three/drei';
import { gsap } from 'gsap';
import * as THREE from 'three';
import type { TurbineModel } from '../data/types';
import { useSimulator, type ComponentId } from '../store/useSimulator';
import { normalOperation } from '../simulation/normalOperation';

const base = import.meta.env.BASE_URL;
const groupOffsets: Record<string, [number, number, number]> = {
  RotorAssembly: [-3.5, 0, 0],
  MainShaft: [-0.7, 1.7, 0],
  Gearbox: [0, 3, 0],
  Generator: [1, 2.3, 0],
  Converter: [2.6, 1.6, 2.3],
  Transformer: [2.6, -1, -2.2],
  Nacelle: [0, 5, 0],
  Yaw: [0, -1.4, 0],
};
function componentOf(object: THREE.Object3D): ComponentId | null {
  let node: THREE.Object3D | null = object;
  while (node) {
    if (node.userData.component) return node.userData.component as ComponentId;
    node = node.parent;
  }
  return null;
}
const isCover = (name: string) =>
  /^(Shell(?:_|$)|HubCover|GeneratorCasing_|GearboxCasing_)/.test(name);
function transitionDuration(seconds: number) {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : seconds;
}

function Asset({ model }: { model: TurbineModel }) {
  const { view, exploded, selected, playing, setSelected } = useSimulator();
  const url = base + (view === 'exterior' ? model.asset.lod : model.asset.glb);
  const gltf = useGLTF(url, base + 'draco/');
  const scene = useMemo(() => {
    const clone = gltf.scene.clone(true);
    clone.traverse((object) => {
      if (object instanceof THREE.Mesh) {
        object.material = Array.isArray(object.material)
          ? object.material.map((material) => material.clone())
          : object.material.clone();
        object.castShadow = false;
        object.receiveShadow = false;
      }
    });
    return clone;
  }, [gltf.scene]);
  const movingParts = useMemo(() => {
    const parts: { object: THREE.Object3D; axis: 'x' | 'y' | 'z'; ratio: number; start: number }[] =
      [];
    scene.traverse((object) => {
      const { motionAxis, motionRatio } = object.userData;
      if (['x', 'y', 'z'].includes(motionAxis) && Number.isFinite(motionRatio)) {
        const axis = motionAxis as 'x' | 'y' | 'z';
        parts.push({ object, axis, ratio: motionRatio, start: object.rotation[axis] });
      }
    });
    return parts;
  }, [scene]);
  const { actions, mixer } = useAnimations(gltf.animations, scene);
  const estimates = normalOperation(model.simulation);
  useEffect(() => {
    mixer.time = 0;
    Object.values(actions).forEach((action) => action?.reset().play());
    return () => {
      Object.values(actions).forEach((action) => action?.stop());
    };
  }, [actions, mixer]);
  useEffect(() => {
    mixer.timeScale = playing ? estimates.rotorRPM / 12 : 0;
  }, [playing, estimates.rotorRPM, mixer]);
  useEffect(() => {
    scene.traverse((object) => {
      if (!(object instanceof THREE.Mesh)) return;
      const cover = isCover(object.name);
      const blade = componentOf(object) === 'blades';
      const fade = view === 'interior' && (cover || blade);
      object.raycast = fade ? () => {} : THREE.Mesh.prototype.raycast;
      object.renderOrder = fade ? 2 : 0;
      const materials = Array.isArray(object.material) ? object.material : [object.material];
      materials.forEach((material) => {
        const mat = material as THREE.MeshStandardMaterial;
        mat.transparent = fade;
        mat.opacity = fade ? (blade ? 0.22 : object.name === 'HubCover' ? 0.09 : 0.075) : 1;
        mat.depthWrite = !fade;
        mat.side = cover ? THREE.DoubleSide : THREE.FrontSide;
        mat.envMapIntensity = 0.8;
        mat.emissive.set(componentOf(object) === selected ? '#689d70' : '#000000');
        mat.emissiveIntensity = componentOf(object) === selected ? 0.32 : 0;
        mat.needsUpdate = true;
      });
    });
  }, [scene, view, selected]);
  useEffect(() => {
    const tweens: gsap.core.Tween[] = [];
    scene.traverse((object) => {
      const offset = groupOffsets[object.name];
      if (!offset) return;
      if (!object.userData.originalPosition)
        object.userData.originalPosition = object.position.clone();
      const position = object.userData.originalPosition as THREE.Vector3;
      tweens.push(
        gsap.to(object.position, {
          x: position.x + (exploded ? offset[0] : 0),
          y: position.y + (exploded ? offset[1] : 0),
          z: position.z + (exploded ? offset[2] : 0),
          duration: transitionDuration(0.9),
          ease: 'power3.inOut',
        }),
      );
    });
    return () => {
      tweens.forEach((tween) => tween.kill());
    };
  }, [scene, exploded]);
  useEffect(() => {
    for (let i = 0; i < model.simulation.bladeCount; i++) {
      const pitch = scene.getObjectByName(`Pitch_${i}`);
      if (pitch) pitch.rotation.y = THREE.MathUtils.degToRad(estimates.pitchDeg);
    }
  }, [scene, estimates.pitchDeg, model.simulation.bladeCount]);
  useEffect(
    () => () => {
      scene.traverse((object) => {
        if (object instanceof THREE.Mesh) {
          (Array.isArray(object.material) ? object.material : [object.material]).forEach(
            (material) => material.dispose(),
          );
        }
      });
      document.body.style.cursor = '';
    },
    [scene],
  );
  useFrame(() => {
    if (!playing) return;
    const phase = (mixer.time * 12 * Math.PI) / 30;
    movingParts.forEach(({ object, axis, ratio, start }) => {
      object.rotation[axis] = start + ((phase * ratio) % (Math.PI * 2));
    });
  });
  const click = (event: ThreeEvent<MouseEvent>) => {
    event.stopPropagation();
    setSelected(componentOf(event.object));
  };
  return (
    <primitive
      object={scene}
      onClick={click}
      onPointerOver={(event: ThreeEvent<PointerEvent>) => {
        event.stopPropagation();
        document.body.style.cursor = 'pointer';
      }}
      onPointerOut={() => {
        document.body.style.cursor = '';
      }}
    />
  );
}

function EnergyFlow({ model }: { model: TurbineModel }) {
  const { view, playing, exploded } = useSimulator();
  const direct = model.specs.gearbox.value === false;
  const dfig = model.specs.generator.value?.startsWith('DFIG');
  const geared = model.specs.gearbox.value === true;
  const paths = useMemo(() => {
    const gx = direct ? -1.65 : 2.05;
    const gy = geared ? 0.69 : 0;
    const cx = direct ? 2.75 : 3.75;
    const tx = direct ? 2.85 : 3.85;
    const mechanical = geared
      ? [
          [-3.5, 0.12, 0.3],
          [-1.3, 0.12, 0.3],
          [0.1, 0.12, 0.3],
          [0.7, gy, 0.3],
          [gx, gy, 0.3],
        ]
      : [
          [-3.5, 0.12, 0.3],
          [-2.1, 0.12, 0.3],
          [gx, gy, 0.3],
        ];
    const definitions: { points: number[][]; color: string; speed: number }[] = [
      { points: mechanical, color: '#d8a356', speed: 0.12 },
      {
        points: [
          [gx, gy + 0.8, 0.75],
          [cx - 0.5, 1.3, 0.25],
          [cx, 0.8, -0.9],
          [cx + 0.65, 0.3, 0],
          [tx, -0.3, 0.65],
        ],
        color: '#3c9e78',
        speed: 0.16,
      },
      {
        points: [
          [tx, -0.52, 0.65],
          [tx - 0.4, -1.0, 0.75],
          [0.4, -1.4, 0.4],
          [0, -3.3, 0],
        ],
        color: '#739351',
        speed: 0.13,
      },
    ];
    if (dfig) {
      // Stator electricity bypasses the partial rotor converter.
      definitions[1] = {
        points: [
          [gx, gy + 0.2, 0.85],
          [tx - 0.7, 0.35, 1.25],
          [tx, -0.3, 0.65],
        ],
        color: '#3c9e78',
        speed: 0.16,
      };
      definitions.push({
        points: [
          [gx, gy + 0.8, -0.7],
          [cx, 0.8, -0.9],
          [cx + 0.65, 0.3, 0],
          [tx, -0.3, 0.65],
        ],
        color: '#718ab3',
        speed: 0.1,
      });
    }
    return definitions.map(({ points, color, speed }) => ({
      curve: new THREE.CatmullRomCurve3(
        points.map((point) => new THREE.Vector3(...(point as [number, number, number]))),
      ),
      color,
      speed,
    }));
  }, [direct, dfig, geared]);
  const particles = useRef<(THREE.Mesh | null)[]>([]);
  const elapsed = useRef(0);
  useFrame((_, delta) => {
    if (!playing || view !== 'interior' || exploded) return;
    elapsed.current += Math.min(delta, 0.1);
    paths.forEach(({ curve, speed }, pathIndex) => {
      for (let i = 0; i < 6; i++) {
        particles.current[pathIndex * 6 + i]?.position.copy(
          curve.getPoint((elapsed.current * speed + i / 6) % 1),
        );
      }
    });
  });
  if (view !== 'interior' || exploded) return null;
  return (
    <group>
      {paths.map(({ curve, color }, index) => (
        <group key={index}>
          <Line
            points={curve.getPoints(48)}
            color={color}
            lineWidth={1.2}
            transparent
            opacity={0.32}
          />
          {Array.from({ length: 6 }, (_, i) => (
            <mesh
              key={i}
              ref={(element) => {
                particles.current[index * 6 + i] = element;
              }}
            >
              <sphereGeometry args={[0.048, 8, 6]} />
              <meshBasicMaterial color={color} toneMapped={false} />
            </mesh>
          ))}
        </group>
      ))}
    </group>
  );
}

function CameraRig() {
  const ref = useRef<ComponentRef<typeof OrbitControls>>(null);
  const { size } = useThree();
  const { view, resetCount, modelId, exploded } = useSimulator();
  useEffect(() => {
    const controls = ref.current;
    if (!controls) return;
    const position = exploded
      ? [-12, 7, 19]
      : view === 'interior'
        ? [-8.7, 4.2, 12.3]
        : [-14, 5.8, 24];
    const target = exploded
      ? [0.4, 0.6, 0]
      : view === 'interior'
        ? [0.1, -0.1, 0]
        : [-1.4, -1.2, 0];
    const aspect = size.width / size.height;
    const fit = Math.max(1, (view === 'interior' ? 1.2 : 0.95) / aspect);
    if (fit > 1) {
      position[0] = target[0] + (position[0] - target[0]) * fit;
      position[1] = target[1] + (position[1] - target[1]) * fit;
      position[2] = target[2] + (position[2] - target[2]) * fit;
    }
    const duration = transitionDuration(1.15);
    const cameraTween = gsap.to(controls.object.position, {
      x: position[0],
      y: position[1],
      z: position[2],
      duration,
      ease: 'power3.inOut',
      onUpdate: () => controls.update(),
    });
    const targetTween = gsap.to(controls.target, {
      x: target[0],
      y: target[1],
      z: target[2],
      duration,
      ease: 'power3.inOut',
    });
    return () => {
      cameraTween.kill();
      targetTween.kill();
    };
  }, [view, resetCount, modelId, exploded, size.width, size.height]);
  return (
    <OrbitControls
      ref={ref}
      makeDefault
      enableDamping
      dampingFactor={0.07}
      minDistance={5.5}
      maxDistance={80}
      maxPolarAngle={Math.PI * 0.86}
    />
  );
}

function StudioLight() {
  return (
    <>
      <ambientLight intensity={0.65} />
      <hemisphereLight args={['#fff9eb', '#bbcbb5', 1.3]} />
      <directionalLight position={[-9, 13, 12]} color="#fff3d7" intensity={3.1} />
      <directionalLight position={[7, 7, -9]} color="#d4ead8" intensity={2.2} />
      <directionalLight position={[2, -4, 10]} color="#ffe6cf" intensity={0.5} />
      <Environment resolution={64} frames={1}>
        <Lightformer
          form="rect"
          intensity={2.2}
          color="#fff7e9"
          position={[-8, 6, 10]}
          scale={[14, 8, 1]}
        />
        <Lightformer
          form="rect"
          intensity={1.7}
          color="#e0eddf"
          position={[7, 3, -8]}
          rotation={[0, Math.PI, 0]}
          scale={[10, 12, 1]}
        />
        <Lightformer
          form="rect"
          intensity={2.4}
          color="#ffffff"
          position={[0, 12, 0]}
          rotation={[Math.PI / 2, 0, 0]}
          scale={[16, 5, 1]}
        />
      </Environment>
    </>
  );
}
function LoadingStatus() {
  const { active, progress } = useProgress();
  return active ? (
    <div className="scene-loading-overlay" role="status">
      <span>Cargando aerogenerador…</span>
      <small>{Math.round(progress)} %</small>
    </div>
  ) : null;
}
export default function TurbineScene({ model }: { model: TurbineModel }) {
  const playing = useSimulator((state) => state.playing);
  return (
    <div className="scene-container">
      <Canvas
        frameloop={playing ? 'always' : 'demand'}
        camera={{ position: [-14, 5.8, 24], fov: 40, near: 0.1, far: 200 }}
        dpr={[1, 1.6]}
        gl={{ antialias: true, powerPreference: 'high-performance', alpha: true }}
        fallback={
          <div className="canvas-message">
            Tu navegador no ofrece WebGL. La ficha y el catálogo siguen disponibles.
          </div>
        }
        onPointerMissed={() => useSimulator.getState().setSelected(null)}
      >
        <fog attach="fog" args={['#e8ede1', 80, 180]} />
        <StudioLight />
        <Suspense fallback={null}>
          <Asset model={model} />
          <EnergyFlow model={model} />
        </Suspense>
        <CameraRig />
        <AdaptiveDpr />
      </Canvas>
      <LoadingStatus />
    </div>
  );
}
