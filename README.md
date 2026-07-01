# SkoltechGamez
This repository contains the source code and simulations developed for two areas of applied research: Optical Physics (digital signal processing and beam propagation) and Operations Engineering (supply chain management )

.
├── matlab/                          # Simulaciones ópticas
│   ├── bessel_interference/         # Interferencia de haces Bessel
│   │   ├── main_bessel.m            # Script principal
│   │   ├── bessel_beam.m            # Función generadora de haz
│   │   └── results/                 # Figuras generadas
│   │
│   └── gaussian_ssfm/               # Propagación en medio no lineal
│       ├── main_ssfm.m             # Script principal (SSFM)
│       ├── split_step_fourier.m    # Función núcleo del método
│       └── plots/                   # Visualizaciones de propagación
│
├── python/                          # Simulación de inventarios
│   ├── inventory_policies.py       # Clases y funciones principales
│   ├── demand_generator.py         # Generación de demanda estocástica
│   ├── run_simulation.py           # Ejecución de escenarios
│   └── outputs/                    # Resultados numéricos y gráficos
│
├── requirements.txt                # Librerías necesarias para Python (numpy, scipy, matplotlib)
└── README.md                       # Este archivo
