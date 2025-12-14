
# Rocket Relations
# rocket_relations
Basic ideal rocket relations for calculating characteristic velocity and thrust coefficient.

The _'init' file is a package that computes ideal rocket calculations. It contains modules that have functions to perform these calculations.

## Installation

Download the source code or clone the repo locally.  
In the project root directory (rocket_relations inside HW5) open a terminal and create/activate a conda environment.

Steps
1. Ensure you have python installed
2. Activate your conda environment (ex: (aste404))
 
   ```bash
   conda activate aste404

3. Navigate to your root folder which contains rocket_relations
 ensure you have hatchling build

    Mamba install hatchling build   # (if error, do following)

        Mamba install hatchling  # (first, then make sure you're in root directory)
    pip install build
    pip install -e .  # (For editable files)


## Quickstart 

from rocket_relations import char_vel, thrust_coeff

char_vel = char_vel(1.2, 350, 3500)
thrust_coeff = thrust_coeff(1.2, 0.0125, 0.02, 10)

print("c* =", char_vel)
print("Cf =", thrust_coeff)

## Documentation

import rocket_relations
help(rocket_relations.char_vel)
help(rocket_relations.thrust_coefficient)

## Tests
Run pytest check function correctnes/input validation:
```bash
    pytest -q
```
Example Result
2 passed in 0.05s

