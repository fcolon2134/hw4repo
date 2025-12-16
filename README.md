# Electric Propulsion Optimization Tool
## Overview

Purpose of tool **"To choose Electric Propulsion thruster configuration that maximizes payload for given mission**

It analyzes: 
- Structural mass ratio (α) in kg/W
- Thruster efficiency (η)
- Specific impulse (Isp) in seconds

And finds the configuration that maximizes payload ratio (M_L/M_0) for mission requirments: Delta-V and mission duration.

## Features

- **Three Analysis Modes:**
  - **Mode A**:  Optimize single user-specified configuration
  - **Mode B**: Compare multiple configurations and identify best
  - **Mode C**: Global optimization across full parameter space

- **Visualization**:  Plots payload ratio vs. Isp with optimal points marked
- **Input Validation**: Prevents invalid/non-physical parameter combinations
- **Smart Warnings**: Flags impossible missions with actionable suggestions

## Installation

**1. Download required files:**
- `electric_propulsion.py` 
- `interactive_tool.py`

Place both files in the same directory.

**2. Install dependencies:**
```bash
pip install numpy scipy matplotlib

```
**Usage**

Navigate to the directory containing both files: (My directory is  C:\Users\faith\ASTE404\Homework5\rocket-relations\src\rocket_relations
After, run:


