# Battery Change Point Analysis

Unified pipeline for detecting change points in lithium-ion battery
voltage, incremental capacity (dQ/dV), and differential voltage (dV/dQ)
profiles using the PELT algorithm.

## Features
- Cycling and OCV datasets supported via configuration files
- SOH calculation (cycle-2 reference or nominal capacity)
- Optional clustering-based relabeling
- Publication-quality visualization

## Usage

```bash
cp configs/cycling.yaml config.yaml
python scripts/run_analysis.py
