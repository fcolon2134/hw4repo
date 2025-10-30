# ASTE 404 Homework 5
# Imports
"""
Module containing functions for calculating rocket characteristic velocity and thrust coefficient.
"""
import numpy as np
from math import sqrt

# Characteristic Velocity
def char_vel(gamma, R, T0):
    """ 
    Calculate the characteristic velocity (c*) of a rocket engine.

    C* - Ratio of product of Chamber Pressure and Throat Area to mass flow rate

    Inputs: Gamma - Sp.Heat Ratio , R- Specific Gas Constant, and T0- Total Temperature
    
    """

    if T0 <= 0:
        raise ValueError("Stagnation temperature must be > 0") # in Kelvin or Rankine
    
    if R <= 0:
        raise ValueError("Specific gas constant must be > 0") # In any units

    c_star = np.sqrt((1/gamma) * ((gamma + 1)/2)**((gamma + 1)/(gamma - 1)) * R*T0)
    # c_star = np.sqrt( (R * T0 / gamma) * (2/(gamma+1))**((gamma+1)/(gamma-1)) )
    return c_star

# Thrust Coefficient 
# Ratio of thrust to product of Pc and At
def thrust_coeff(gamma, Pe_P0,Pa_P0, Ae_At):
    """ 
    Calculate the thrust coefficient (Cf) of a rocket engine.

    Cf - Ratio of Thrust to product of Chamber Pressure and Throat Area

    Inputs: Gamma - Sp.Heat Ratio , Pe- Exit Pressure, Pc- Chamber Pressure, Ae- Exit Area, At- Throat Area
    Notes: Arrays are supported for all inputs.
    
    """
    # input errors
    inputs = [gamma, Pe_P0, Pa_P0, Ae_At]

    for var, name in [(gamma, "gamma"), (Pe_P0, "Pe_P0"), (Pa_P0, "Pa_P0"), (Ae_At, "Ae_At")]:
        if not isinstance(var, (int, float,np.ndarray)):
         raise TypeError(f"{name} must be numeric")

    shapes = [x.shape for x in inputs if isinstance(x, np.ndarray)]

    if len(shapes) > 1 and not all (shape == shapes[0] for shape in shapes):
        raise ValueError("All array inputs must have the same shape.")

    
    if np.any(Pe_P0 < 0) or np.any(Pe_P0 >=1):
        raise ValueError("Pe/P0 must be in the range [0, 1).")  # Exit pressure cannot exceed chamber pressure. [ means exclusive, ) means inclusive
    
    if np.any(Pa_P0 < 0) or np.any(Pa_P0 >= 1):
        raise ValueError("Pa/P0 must be in the range [0, 1).")  # Ambient pressure cannot exceed chamber pressure.
    
    if np.any(Ae_At < 1):
        raise ValueError("Ae/At must be greater than or equal to 1.")  # Exit area must be greater than or equal to throat area, by definitions of choked flow
    
    if np.any((gamma <= 1) | (gamma > 1.8)):
        raise ValueError("Specific heat ratio γ must be > 1 and <= 1.8")

   # if np.any(Pe_P0< Pa_P0):
   #     raise ValueError("Exit pressure cannot be less than ambient pressure.")

    # function
    term1 = np.sqrt((2*gamma**2)/(gamma-1) * (2/(gamma+1))**((gamma+1)/(gamma-1)) * (1 - (Pe_P0)**((gamma-1)/gamma)))
    term2 = (Pe_P0-Pa_P0) * Ae_At
    Cf = term1 + term2
    return Cf
