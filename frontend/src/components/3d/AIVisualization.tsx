import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Line } from '@react-three/drei';
import * as THREE from 'three';

export default function AIVisualization() {
  const group = useRef<THREE.Group>(null);
  
  const nodes = [
    { pos: [0, 2, 0], label: 'AI CORE' },
    { pos: [-2, -1, 1], label: 'SOIL' },
    { pos: [2, -1, 1], label: 'WEATHER' },
    { pos: [0, -1, -2], label: 'TERRAIN' },
    { pos: [-1.5, 1, -1], label: 'MARKET' },
    { pos: [1.5, 1, -1], label: 'RISK' },
  ];

  useFrame((state, delta) => {
    if (group.current) {
      group.current.rotation.y += delta * 0.2;
    }
  });

  return (
    <group ref={group}>
      {nodes.map((node, i) => (
        <group key={i} position={node.pos as [number, number, number]}>
          <Sphere args={[0.2, 16, 16]}>
            <meshStandardMaterial color="#00ff88" emissive="#00ff88" emissiveIntensity={2} />
          </Sphere>
        </group>
      ))}
      
      {/* Connections to center */}
      {nodes.slice(1).map((node, i) => (
        <Line 
          key={`line-${i}`}
          points={[[0, 2, 0], node.pos as [number, number, number]]}
          color="#00ff88"
          lineWidth={2}
          transparent
          opacity={0.3}
        />
      ))}
    </group>
  );
}
