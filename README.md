# Battery Change Point Analysis

This repository provides a unified pipeline for detecting
change points in lithium-ion battery voltage, incremental
capacity (dQ/dV), and differential voltage (dV/dQ) curves
using the PELT algorithm from the `ruptures` library.

## Features
- Cycle-wise change point detection
- Support for cycling and OCV datasets
- Configurable penalty and jump parameters
- SOH computation (cycle-2 reference or nominal capacity)
- Optional clustering-based relabeling
- Publication-ready visualization

## Usage
```bash
python scripts/run_analysis.py --config configs/cycling.yaml
