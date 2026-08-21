import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

function Particles() {
  const points = useRef<THREE.Points>(null);
  const particleCount = 1000;
  const positions = new Float32Array(particleCount * 3);
  
  for(let i = 0; i < particleCount; i++) {
    const r = 2.5 + Math.random() * 2;
    const theta = 2 * Math.PI * Math.random();
    const phi = Math.acos(2 * Math.random() - 1);
    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    positions[i*3] = x;
    positions[i*3+1] = y;
    positions[i*3+2] = z;
  }

  useFrame((state, delta) => {
    if (points.current) {
      points.current.rotation.y += delta * 0.05;
    }
  });

  return (
    <Points ref={points} positions={positions} stride={3}>
      <PointMaterial transparent color="#00ff88" size={0.02} sizeAttenuation={true} depthWrite={false} />
    </Points>
  );
}

export default function EarthGlobe() {
  const meshRef = useRef<THREE.Mesh>(null);
  const cloudRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current) meshRef.current.rotation.y += delta * 0.1;
    if (cloudRef.current) {
      cloudRef.current.rotation.y += delta * 0.12;
      cloudRef.current.rotation.z += delta * 0.01;
    }
  });

  return (
    <group>
      <Sphere ref={meshRef} args={[2, 64, 64]}>
        <meshStandardMaterial
          color="#0d2615"
          wireframe={true}
          roughness={0.8}
          metalness={0.2}
          transparent
          opacity={0.3}
        />
      </Sphere>
      
      {/* Solid inner core */}
      <Sphere args={[1.98, 64, 64]}>
        <meshStandardMaterial
          color="#05100a"
          roughness={1}
        />
      </Sphere>

      {/* Atmosphere glow */}
      <Sphere ref={cloudRef} args={[2.1, 64, 64]}>
        <meshStandardMaterial
          color="#00ff88"
          transparent
          opacity={0.08}
          side={THREE.BackSide}
          blending={THREE.AdditiveBlending}
        />
      </Sphere>
      
      <Particles />
    </group>
  );
}
