import type { ComponentId } from '../store/useSimulator';
export const components: Record<ComponentId, { name: string; description: string; color: string }> =
  {
    blades: {
      name: 'Palas',
      description:
        'El viento crea una fuerza sobre las palas. Esa fuerza hace girar el rotor y convierte energía del viento en movimiento.',
      color: '#e7eef2',
    },
    hub: {
      name: 'Buje',
      description:
        'Une las palas y transmite su esfuerzo al eje. En su interior se alojan los mecanismos que ajustan el paso.',
      color: '#b8c8d2',
    },
    rotor: {
      name: 'Rotor',
      description:
        'Es el conjunto de palas y buje. Gira lentamente y entrega el movimiento al tren de potencia.',
      color: '#b8c8d2',
    },
    shaft: {
      name: 'Eje principal',
      description:
        'Transmite el giro y el par del rotor. Los apoyos soportan las cargas antes de que el movimiento llegue al generador.',
      color: '#91a7b8',
    },
    gearbox: {
      name: 'Multiplicadora',
      description:
        'Aumenta la velocidad de giro para el generador mediante engranajes. No está presente en un sistema de accionamiento directo.',
      color: '#d5a562',
    },
    generator: {
      name: 'Generador',
      description:
        'Transforma el movimiento en electricidad mediante la interacción entre un campo magnético y las bobinas.',
      color: '#5de0c9',
    },
    converter: {
      name: 'Convertidor',
      description:
        'Acondiciona la electricidad para conectarla a la red. En DFIG procesa la rama del rotor; un convertidor completo procesa toda la potencia.',
      color: '#77a9e7',
    },
    transformer: {
      name: 'Transformador',
      description:
        'Eleva la tensión para transportar electricidad por la red del parque. Su ubicación aquí es esquemática y no confirma su posición instalada.',
      color: '#e99d69',
    },
    yaw: {
      name: 'Orientación · yaw',
      description:
        'Orienta la góndola hacia el viento. En este escenario el viento está alineado y la góndola permanece estable.',
      color: '#afbcce',
    },
    pitch: {
      name: 'Paso de pala · pitch',
      description:
        'Gira cada pala sobre su eje para regular la energía captada. En el escenario normal fijo mantiene un ángulo estable.',
      color: '#bcabed',
    },
    nacelle: {
      name: 'Góndola',
      description:
        'Protege y soporta los equipos. La vista traslúcida permite ver cómo se conectan los subsistemas.',
      color: '#b9d4e1',
    },
    tower: {
      name: 'Torre',
      description:
        'Sostiene la góndola y el rotor y transmite sus cargas a la cimentación. Contiene accesos y conexiones de la máquina.',
      color: '#d4e1eb',
    },
  };
