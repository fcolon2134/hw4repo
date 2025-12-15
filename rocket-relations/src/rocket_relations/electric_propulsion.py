import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar


def payload_ratio(isp, alpha, delta_v, eta, tb, g):
    """
    This section defines main equation to use and plot
    Calculate the payload mass ratio (M_L / M_0) as a function of specific impulse (Isp).
    Parameters:
        isp: Specific impulse (s); alpha: structural mass ratio (M_s / M_0); delta_v: Required delta-v (m/s) eta: efficiency; tb: burn time (s) g: gravity (m/s^2)
    Returns:
        Payload mass ratio (M_L / M_0)
    """
    ve = isp * g  # Exhaust velocity (m/s)
    c_factor = (alpha * ve**2) / (2 * eta * tb)  # Structural inefficiency term
    return np.exp(-delta_v / ve) * (1 + c_factor) - c_factor


def find_optimal_isp(alpha, delta_v, eta, tb, g):
    """
    Find the optimal specific impulse (Isp) that maximizes the payload mass ratio.
    
    Parameters:
        alpha: Structural mass fraction (M_s / M_0)
        delta_v: Required delta-v (m/s)
        eta: Thruster efficiency
        tb: Thrust power (W)
        g: Gravitational acceleration (m/s^2)
        
    Returns:
        optimal_isp: Specific impulse that maximizes the payload ratio
        optimal_payload: The maximum payload mass ratio
    """
    # Function to minimize (negative payload ratio since we are maximizing)
    def neg_payload(isp):
        return -payload_ratio(isp, alpha, delta_v, eta, tb, g)

    # Use Golden-Section Search to find the peak (0 < Isp < 9000 s)
    result = minimize_scalar(neg_payload, bounds=(100, 9000), method='bounded')

    # Extract optimal Isp and corresponding payload ratio
    optimal_isp = result.x
    optimal_payload = -result.fun  # Convert back to positive payload ratio
    return optimal_isp, optimal_payload


def plot_payload_vs_isp(alpha, delta_v, eta, tb, g):
    """
    Plot the payload ratio (M_L / M_0) as a function of specific impulse (Isp),
    and highlight the optimal point.
    
    Parameters:
        alpha: Structural mass fraction (M_s / M_0)
        delta_v: Required delta-v (m/s)
        eta: Thruster efficiency
        tb: Thrust power (W)
        g: Gravitational acceleration (m/s^2)    
    """
    # Define range of Isp values
    isp_values = np.linspace(100, 9000, 100)
    # Calculate payload ratios for all Isp values
    payload_ratios = [payload_ratio(isp, alpha, delta_v, eta, tb, g) for isp in isp_values]

    # Find the optimal Isp and corresponding payload ratio
    optimal_isp, optimal_payload = find_optimal_isp(alpha, delta_v, eta, tb, g)

    # Plot the curve
    plt.figure(figsize=(10, 6))
    plt.plot(isp_values, payload_ratios, label=r"$M_L / M_0$", color="blue")
    plt.scatter(optimal_isp, optimal_payload, color="red", zorder=5, label=f"Optimal Isp = {optimal_isp:.1f} s")
    plt.axvline(optimal_isp, color="red", linestyle="--", alpha=0.6)

    # Graph details
    plt.title("Payload Ratio vs. Specific Impulse", fontsize=14)
    plt.xlabel("Specific Impulse (Isp) [s]", fontsize=12)
    plt.ylabel("Payload Ratio (M_L / M_0)", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print the optimal values
    print(f"Optimal Specific Impulse: {optimal_isp:.2f} s")
    print(f"Maximum Payload Ratio: {optimal_payload:.5f}")


if __name__ == "__main__":
    # Constants
    delta_v = 9500  # Mission delta-v in m/s (e.g., interplanetary mission)
    g = 9.81  # Gravitational acceleration in m/s^2
    alpha = .0054  # Specific mass of power plant [kg/W] # H&P value range from 1.4-7 kg/kW, which equals .0014-.007 kg/W
    eta = 0.9  # Thruster efficiency (60%)
    td = 200 # Total mission duration in days
    tb = td * 24 * 3600  # burn time in seconds (arbitrary for electric propulsion)

    # Plot payload ratio vs. specific impulse and find the optimal point
    plot_payload_vs_isp(alpha, delta_v, eta, tb, g)