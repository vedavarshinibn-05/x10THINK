import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Box } from '@react-three/drei';
import * as THREE from 'three';

export default function SoilLayers() {
  const group = useRef<THREE.Group>(null);

  useFrame((state, delta) => {
    if (group.current) {
      group.current.rotation.y += delta * 0.1;
    }
  });

  const layers = [
    { color: '#00ff88', depth: 0.1, y: 1.5 }, // Topsoil / Vegetation
    { color: '#452c10', depth: 0.8, y: 1.0 }, // A Horizon
    { color: '#5c3a21', depth: 1.2, y: 0.0 }, // B Horizon
    { color: '#7a5a41', depth: 1.5, y: -1.4 }, // C Horizon (Subsoil)
  ];

  return (
    <group ref={group} rotation={[0.2, 0, 0]}>
      {layers.map((layer, i) => (
        <Box key={i} args={[3, layer.depth, 3]} position={[0, layer.y, 0]}>
          <meshStandardMaterial 
            color={layer.color} 
            roughness={0.9} 
            transparent 
            opacity={0.9}
            wireframe={i === 0}
          />
        </Box>
      ))}
    </group>
  );
}
