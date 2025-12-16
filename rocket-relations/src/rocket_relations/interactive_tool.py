# interactive_tool.py

from electric_propulsion import find_optimal_isp, plot_payload_vs_isp, optimize_thruster, payload_ratio
import numpy as np
import matplotlib.pyplot as plt

def interactive_tool():
    """
    Interactive tool for electric propulsion optimization.
    """
    print("Welcome to the Electric Propulsion Interactive Tool!")
    print("This tool will guide you through analyzing thruster configurations.\n")

    print("Please adhere to the suggested input bounds.\n")

    # Step 1: Prompt for Mission Requirements
    while True:
        delta_v = float(input("Enter the required Delta-V (m/s) [range: 5000-15000]: "))
        if 5000 <= delta_v <= 15000:
            break
        else:
            print("Error: Delta-V must be within the range of 5000 to 15000 m/s.")
        
    while True:
        td = float(input("Enter the mission duration (burn time, in days) [range:20-200]: "))
        if 20<=td<=200:
            break
        else:
            print("Error: Mission duration must be within the range of 20 to 200 days.")
        
    tb = td * 86400  # Convert burn time from days to seconds
    g = 9.81  # Gravitational constant in m/s²

    # Step 2: Prompt for Analysis Method
    print("\nChoose a method for thruster analysis:")
    print("A: Optimize for a single configuration (user chooses 1 specific mass and efficiency value)\n")
    print("B: Optimize for multiple configurations (user chooses multiple specific mass and efficiency values)\n")
    print("C: Global optimization for mission requirements\n")
    method = input("Enter 'A', 'B', or 'C': ").strip().upper()

    # Analysis Mode A: Single Configuration
    if method == "A":
        print("\n--- Single Configuration ---")
        while True:
            try:
             alpha = float(input("Enter structural mass ratio α (Kg/W, range: 0.0015-0.266): "))
             if 0.0015 <= alpha <= 0.266:
                 break
             else:
                 print("Error: Structural mass ratio α must be within the range of 0.0015 to 0.266 Kg/W.")
            except ValueError:
                print("Error: Please enter a valid number for α.")
                 
        while True:
            try:
             eta = float(input("Enter thruster efficiency η (0-1, e.g., 0.8): "))
             if 0 <= eta <= 1:
                 break
             else:
                 print("Error: Thruster efficiency η must be between 0 and 1.")
            except ValueError:
                print("Error: Please enter a valid number for η.")  
        
        
        # Perform optimization for a single configuration
        optimal_isp, optimal_payload = find_optimal_isp(alpha, delta_v, eta, tb, g)
        # Check for excessively high Isp
        if optimal_isp > 9000:
            print("\nWarning: Required Specific Impulse (Isp) exceeds 9000 seconds!")
            print("This indicates very high propulsion demands, which may be impractical.")
            print("Suggestions:")
            print("- Increase structural mass fraction (α) — this reduces thruster requirements.")
            print("- Reduce mission Delta-V by optimizing the trajectory (e.g., using gravity assists).")
            print("- Increase burn time — spreading thrust over longer periods reduces propulsion load.")
            print("- Increase thruster efficiency (η).")

            restart = input("\nWould you like to restart with new inputs? (y/n): ").strip().lower()
            if restart == 'y':
                return interactive_tool()  # Restart the tool
            else:
                print("Exiting the tool. Thank you for using the Electric Propulsion Interactive Tool!")
                return  # Stop execution

         # Display Results
        print("\nResults for Single Thruster Configuration:")
        print(f"  Optimal Specific Impulse (Isp): {optimal_isp:.2f} seconds")
        print(f"  Maximum Payload Ratio: {optimal_payload:.5f}")
        
        # Plot payload ratio vs. specific impulse for the given configuration
        plot_payload_vs_isp(alpha, delta_v, eta, tb, g)
        return
       

    # Analysis Mode B: Range-Based Comparison
    elif method == "B":  
    
        while True:
            try: 
                alpha_values = list(map(float, input("Enter alpha values (comma-separated, within range of 0.0015 to 0.266 g/W): ").split(",")))
                if all(0.0015 <= a <= 0.266 for a in alpha_values):
                    break      
                else:   
                    print("Error: All alpha values must be within the range of 0.0015 to 0.266 Kg/W.")
            except ValueError:
             print("Error: Please enter valid numbers for alpha values.")

        while True:
            try:  
                eta_values = list(map(float, input("Enter eta values (comma-separated, e.g., 0.5,0.8): ").split(",")))
                if all(0 <= e <= 1 for e in eta_values):
                    break   
                else:   
                    print("Error: All eta values must be between 0 and 1.")
            except ValueError:
                print("Error: Please enter valid numbers for eta values.")

        isp_range = np.linspace(100, 9000, 200)
        
        
    
# ========= Find Best Configuration from User's Inputs =========
        print("\n--- Best Configuration from user inputs ---")
        best_config = {"alpha": None, "eta": None, "isp": None, "payload": -np.inf}

        for alpha in alpha_values:
            for eta in eta_values: 
                config_optimal_isp, config_optimal_payload = find_optimal_isp(alpha, delta_v, eta, tb, g)
                
                if config_optimal_payload > best_config["payload"]: 
                    best_config = {
                        "alpha": alpha,
                        "eta": eta,
                        "isp": config_optimal_isp,
                        "payload": config_optimal_payload
                    }

        # Print best from user inputs
        if best_config["payload"] > 0:
            print(f"  Best Alpha (α): {best_config['alpha']:.5f} kg/W")
            print(f"  Best Eta (η): {best_config['eta']:.4f}")
            print(f"  Best Isp: {best_config['isp']:.2f} s")
            print(f"  Best Payload Ratio: {best_config['payload']:.5f}")
        else:
            print("⚠️  No positive payload ratio found in user input configurations!")
            print("     This means the mission is physically impossible with current constraints.")
            print("     Suggestions:")
            print("     - Reduce Delta-V requirement")
            print("     - Increase burn time (mission duration)")
            print("     - Use more efficient thrusters (higher η)")
            print("     - Use lighter thruster structures (lower α)")

## ================== Plot Multiple Thruster Configurations ==================
# Create and display comparison plots for each alpha/eta combo
        print("Generating plots for multiple configurations...")
        plt.figure(figsize=(12, 8))
        # Mark the user's best configuration with red dot and line
        
        # Inside the plotting loop
        for alpha in alpha_values:
            for eta in eta_values:
                payload_ratios = [
                    payload_ratio(isp, alpha, delta_v, eta, tb, g) for isp in isp_range
                ]
                
                # Check if all payload ratios are negative
                if all(pr < 0 for pr in payload_ratios):
                    print(f"\n⚠️  WARNING: Configuration α={alpha}, η={eta} produces negative payload ratios!")
                    print("       This means the mission is physically impossible with these parameters.")
                    print("       Suggestions:")
                    print("       - Decrease alpha (use lighter thruster structures)")
                    print("       - Increase eta (use more efficient thrusters)")
                    print("       - Reduce Delta-V or increase burn time")
                # Check if this is the best configuration
                if alpha == best_config["alpha"] and eta == best_config["eta"]:
                    label = f"α={alpha}, η={eta} (Optimal Configuration)"
                else:
                    label = f"α={alpha}, η={eta}"
                plt.plot(isp_range, payload_ratios, label=label)
                
        if best_config["payload"] > 0:
            plt.scatter(best_config["isp"], best_config["payload"], color="red", zorder=5, s=80, label=f"Optimal Isp = {best_config['isp']:.1f} s")
            plt.axvline(best_config["isp"], color="red", linestyle="--", alpha=0.6)        

        
        # Add title and labels
        plt.title("Payload Ratio vs Specific Impulse for Multiple Configurations")
        plt.xlabel("Specific Impulse (Isp) [s]")
        plt.ylabel("Payload Ratio (M_L / M_0)")
        plt.legend(fontsize=10)
        plt.grid(True)
        plt.show()

        print("\nRange-based analysis complete.")
        print(f"Alpha values tested: {alpha_values}")
        print(f"Efficiency values tested: {eta_values}")
    
    elif method == "C":
        # ========= Perform global optimization across all configurations =========
        opt_results = optimize_thruster(delta_v, tb, g)
        optimal_alpha, optimal_eta, optimal_isp = opt_results.x
       # Print global optimal results
        if opt_results.success:
            optimal_alpha, optimal_eta, optimal_isp = opt_results.x
            max_payload_ratio = -opt_results. fun
            
            # Check if the optimal payload ratio is negative or equal to zero
            if max_payload_ratio <= 0:
                print("\n⚠️  WARNING: Global optimization found NO positive payload ratio!")
                print("       This means the mission is physically impossible with current constraints.")
                print("       Suggestions:")
                print("       - Reduce Delta-V requirement")
                print("       - Increase burn time (mission duration)")
                print("       - Use more efficient thrusters (higher η)")
                print("       - Use lighter thruster structures (lower α)")
            else:
                print("\n--- Global Optimization for Mission Requirements: ---")
                print(f"  Optimal Alpha (α): {optimal_alpha:.5f} kg/W")
                print(f"  Optimal Eta (η): {optimal_eta:.4f}")
                print(f"  Optimal Isp: {optimal_isp:.2f} s")
                print(f"  Maximum Payload Ratio: {max_payload_ratio:.5f}")
        else:
            print("Global optimization failed.  Please check your input parameters.")

    else:
        print("Invalid method selected. Please restart and choose 'A', 'B', or 'C'.")

    

if __name__ == "__main__":
    interactive_tool()