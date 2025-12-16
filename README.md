# Electric Propulsion Optimization Tool
###  ASTE404 Mini-Project 
###  Faith Colon 
## Overview

Purpose of tool **"To choose Electric Propulsion thruster configuration that maximizes payload for given mission**

It analyzes: 
- Structural mass ratio (α) in kg/W
- Thruster efficiency (η)
- Specific impulse (Isp) in seconds

And finds the configuration that maximizes payload ratio (M_L/M_0) for mission requirments: Delta-V and mission duration.

**Note: all git commits for ASTE404 Miniproject are located in MASTER branch**

## Features

- **Three Analysis Modes:**
  - **Mode A**:  Optimize single user-specified configuration
  - **Mode B**: Compare multiple configurations and identify best
  - **Mode C**: Global optimization across full parameter space

- **Visualization**:  Plots payload ratio vs. Isp with optimal points marked
- **Input Validation**: Prevents invalid/non-physical parameter combinations
- **Smart Warnings**: Flags impossible missions with actionable suggestions

## Installation

**1. Download and/or ensure required files are in same folder:**
- `electric_propulsion.py` - Equations and core functions (minimize, and optimization) 
- `interactive_tool.py`-  Interactive Tool file to prompt user inputs and display results

Place both files in the same directory (if needed)

**2. Install dependencies:**
```bash
pip install numpy matplotlib scipy
```
## Usage

The main files are located in `src/rocket_relations/`:
- `electric_propulsion.py` - core functions
- `interactive_tool.py` - Run this file 

### Running the Interactive Tool
```bash
cd src/rocket_relations
python interactive_tool.py
```

The tool will prompt you for mission parameters (delta-v, structural mass, efficiency, burn time) and generate optimization results and plots.

### Example
```python
from electric_propulsion import find_optimal_isp

delta_v = 9500  # m/s
alpha = 0.0054  # kg/W
eta = 0.9
tb = 200 * 24 * 3600  # seconds
g = 9.81

optimal_isp, max_payload = find_optimal_isp(alpha, delta_v, eta, tb, g)
print(f"Optimal Isp: {optimal_isp:.2f} s")
```
## Author
Faith Colon - ASTE404
