import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

def validate_inputs(alpha, eta, isp, delta_v, tb):
    if alpha <= 0 or eta <= 0 or isp <= 0 or delta_v <= 0 or tb <= 0:
        raise ValueError("All parameters must be positive.")
    if eta > 1:
        raise ValueError("Efficiency (η) must be between 0 and 1.")
    if alpha >=.266:  # speciic mass must not exceed .266, otherwise paload ratio becomes negative
        print("Warning: Structural mass fraction (α) must be betwen 0 and 0.266")

# ========== Main Equation for Payload Ratio =============
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
# ================= End of Payload Ratio Equation =============

# =============== Thruster Optimization # 1 for Isp only ==============
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

    # Use Golden-Section Search to find the peak (0 < Isp < 10000 s)
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
   # print(f"Optimal Specific Impulse: {optimal_isp:.2f} s")
   # print(f"Maximum Payload Ratio: {optimal_payload:.5f}")

from scipy.optimize import minimize

# =============== Thruster Optimization # 2: Multiple Configurations for multiple valuse of alpha, eta, and Isp============= 
def optimize_thruster(delta_v, tb, g):
    """
    Global optimization function to maximize payload ratio across 
    alpha, eta, and Isp parameters.
    
    Parameters:
        delta_v: Target delta-v (m/s)
        tb: Burn time (s)
        g: Gravitational acceleration (m/s^2)
    
    Returns:
        Optimization result object (optimal values and max payload ratio).
    """
    # Objective function: payload ratio (negative for maximization)
    def neg_payload(params):
        alpha, eta, isp = params
        return -payload_ratio(isp, alpha, delta_v, eta, tb, g)
    
    # Bounds for each parameter:
    # Alpha (kg/W), Eta (Efficiency), Isp (s)
    bounds = [
        (0.002, 0.03),  # Alpha: specific mass (1-15 g/W)
        (0.4, 0.9),      # Eta: thruster efficiency (40% to 90%)
        (100, 9000)      # Isp: Specific impulse range
    ]

    # Initial guess for the parameters, using midpoint of bounds (reccomended)
    initial_guess = initial_guess = [
        (bounds[0][0] + bounds[0][1]) / 2,  # Alpha midpoint
        (bounds[1][0] + bounds[1][1]) / 2,  # Eta midpoint
        (bounds[2][0] + bounds[2][1]) / 2   # Isp midpoint
    ]

    # Use L-BFGS-B (gradient-based method with bounds) for optimization

    opt_result = minimize(neg_payload, initial_guess, bounds=bounds, method='L-BFGS-B')
    return opt_result
# ================= End of Thruster Optimization # 2 =====================

# =============== Plotting Multiple Thruster Configurations ==============
import numpy as np
import matplotlib.pyplot as plt

def plot_multiple_thruster_configs(alpha_values, eta_values, delta_v, tb, g, isp_range):
    """
    Plot payload ratio vs. specific impulse for multiple thruster configurations.
    
    Parameters:
        alpha_values: List of alpha values (specific mass in kg/W).
        eta_values: List of eta values (efficiencies to test).
        delta_v: Delta-v for the mission (m/s).
        tb: Burn time for the thruster (seconds).
        g: Gravitational constant (m/s^2).
        isp_range: Range of specific impulse values to evaluate (s).
    """
    plt.figure(figsize=(12, 8))
    for alpha in alpha_values:
        for eta in eta_values:
            # Compute payload ratios for the given alpha and eta over all isp
            payload_ratios = [
                payload_ratio(isp, alpha, delta_v, eta, tb, g) for isp in isp_range
            ]
            # Plot the results for this configuration
            label = fr"α/η={alpha*1000/eta:.4f} [kg/kW]"  # Label for the config
            plt.plot(isp_range, payload_ratios, label=label)

    # Add graph details
    plt.title("Payload Ratio vs Specific Impulse for Various Thruster Configurations", fontsize=16)
    plt.xlabel("Specific Impulse (Isp) [s]", fontsize=14)
    plt.ylabel("Payload Ratio (M_L / M_0)", fontsize=14)
    plt.legend(fontsize=10, loc="best")  # Automatically locate the best position for the legend
    plt.grid(True)
    plt.show()
# ================= End of Multiple Thruster Configurations Plotting ==============

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

    #------------- Print Optimization results-----------------
    opt_result = optimize_thruster(delta_v, tb, g)

    if opt_result.success:
        optimal_alpha, optimal_eta, optimal_isp = opt_result.x
        max_payload_ratio = -opt_result.fun  # Convert back to positive payload ratio
        print("\nOptimization Results:")
        print(f"  Optimal Alpha: {optimal_alpha:.4f} (kg/W)")
        print(f"  Optimal Eta: {optimal_eta:.4f}")
        print(f"  Optimal Isp: {optimal_isp:.2f} (s)")
        print(f"  Maximum Payload Ratio: {max_payload_ratio:.5f}")
    else:
        print("Optimization failed!")


     # Thruster-specific parameters
    alpha_values = [0.005, 0.03]  # Structural mass ratios (kg/W)
    eta_values = [0.5, 0.8]  # Thruster efficiencies
    isp_range = np.linspace(200, 9000, 200)  # Specific impulse range (s)

    # Plot and compare thruster configurations
    plot_multiple_thruster_configs(alpha_values, eta_values, delta_v, tb, g, isp_range)
