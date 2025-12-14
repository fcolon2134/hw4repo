# Tests Ideal.py file in rocket_relations package.
from rocket_relations.ideal import char_vel, thrust_coeff
import numpy as np
from math import sqrt

def test_char_vel_scalar():
    result = char_vel(1.2, 350, 3500)
    assert abs(result - 1706.6214) < 1e-3  # example expected value

def test_thrust_coeff_scalar():
    result = thrust_coeff(1.2, 0.0125, 0.02, 10)
    assert abs(result - 1.5423079) < 1e-6

