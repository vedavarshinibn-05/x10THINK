import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function FarmTerrain({ layer = 'LAND' }: { layer?: string }) {
  const meshRef = useRef<THREE.Mesh>(null);

  // Generate procedural terrain geometry
  const geometry = useMemo(() => {
    const size = 50;
    const segments = 50;
    const geo = new THREE.PlaneGeometry(size, size, segments, segments);
    const pos = geo.attributes.position;
    const col = new Float32Array(pos.count * 3);
    const colorObj = new THREE.Color();

    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i);
      const y = pos.getY(i);
      const dist = Math.sqrt(x * x + y * y);
      const z = Math.sin(x * 0.2) * Math.cos(y * 0.2) * (dist > 5 ? 1 : 0.2);
      pos.setZ(i, z);

      if (layer === 'WATER') {
        colorObj.set(z < 0 ? '#3b82f6' : '#1e3a8a');
      } else if (layer === 'SOIL') {
        colorObj.set(z > 0.5 ? '#78350f' : '#92400e');
      } else if (layer === 'RISK') {
        colorObj.set(z < -0.5 ? '#ef4444' : '#f59e0b');
      } else {
        colorObj.set(z > 0 ? '#00ff88' : '#059669');
      }

      col[i * 3] = colorObj.r;
      col[i * 3 + 1] = colorObj.g;
      col[i * 3 + 2] = colorObj.b;
    }

    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    geo.computeVertexNormals();
    return geo;
  }, [layer]);

  useFrame((_state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.z += delta * 0.05;
    }
  });

  return (
    <mesh ref={meshRef} rotation={[-Math.PI / 2.5, 0, 0]} geometry={geometry}>
      <meshStandardMaterial
        vertexColors={true}
        wireframe={layer === 'RISK'}
        roughness={0.8}
        metalness={0.1}
      />
    </mesh>
  );
}
