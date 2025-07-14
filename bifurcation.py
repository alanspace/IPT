import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import warnings
import time  # For the timer
from tqdm import tqdm  # For the progress bar
import multiprocessing  # For CPU parallelization

# Suppress RuntimeWarning from potential exp() overflow, which is handled.
warnings.filterwarnings("ignore", category=RuntimeWarning)

# --- 1. Define Model Parameters (from the user's paper) ---
# This dictionary holds all constant parameters
PARAMS = {
    'R': 10.0,          # Resistance (Ohm)
    'L': 0.239e-3,      # Inductance (H)
    'Cj': 30e-12,       # Diode Junction Capacitance (F)
    'f': 376.6e3,       # Driving Frequency (Hz)
    'Is': 2.5e-9,       # Assumed Reverse saturation current (A)
    'n_ideality': 1.75, # Assumed Ideality factor
    'Vt': 0.026,        # Thermal voltage at room temp (V)
}
PARAMS['w'] = 2 * np.pi * PARAMS['f'] # Angular frequency

# --- 2. Define the System of First-Order ODEs ---
def model(t, y, V0, p):
    V_D, dV_D_dt = y
    Vs_t = V0 * np.sin(p['w'] * t)
    
    V_D_clipped = np.clip(V_D, -100, 1.5)
    exp_term = np.exp(V_D_clipped / (p['n_ideality'] * p['Vt']))
    
    i_D = p['Is'] * (exp_term - 1)
    di_D_dt = (p['Is'] / (p['n_ideality'] * p['Vt'])) * exp_term * dV_D_dt

    d2V_D_dt = (Vs_t - V_D - p['R'] * i_D - p['R'] * p['Cj'] * dV_D_dt - p['L'] * di_D_dt) / (p['L'] * p['Cj'])
    
    return [dV_D_dt, d2V_D_dt]

# --- 3. Define a Worker Function for a Single Simulation Point ---
# This function will be run in parallel on different CPU cores
def simulate_point(V0):
    p = PARAMS
    num_cycles_transient = 400
    num_cycles_steady = 500
    t_transient_end = num_cycles_transient / p['f']
    # THE FIX IS ON THE NEXT LINE
    t_steady_end = t_transient_end + (num_cycles_steady / p['f']) # <-- Corrected this line

    y0 = [0, 0]
    
    sol = solve_ivp(
        fun=lambda t, y: model(t, y, V0, p), 
        t_span=[0, t_steady_end], 
        y0=y0, 
        dense_output=True,
        method='RK45',
        t_eval=np.linspace(t_transient_end, t_steady_end, 15000)
    )
    
    V_D_solution = sol.y[0]
    peaks, _ = find_peaks(V_D_solution, height=0.1)
    unique_peaks = np.unique(np.round(V_D_solution[peaks], 4))
    
    # Return a list of (V0, peak_value) tuples for this V0
    return [(V0, peak) for peak in unique_peaks]

# --- Main Execution Block ---
if __name__ == "__main__":
    # This __name__ == "__main__" guard is essential for multiprocessing
    
    start_time = time.time() # Start the timer

    # Voltage range based on the experimental data
    V0_range = np.linspace(1.8, 5.5, 400)
    
    # Set up the multiprocessing pool to use all available CPU cores
    num_cores = multiprocessing.cpu_count()
    print(f"Starting simulation on {num_cores} CPU cores...")
    
    results = []
    with multiprocessing.Pool(processes=num_cores) as pool:
        # Use tqdm to create a progress bar
        # pool.imap_unordered is efficient as it processes results as they complete
        pbar = tqdm(pool.imap_unordered(simulate_point, V0_range), total=len(V0_range))
        for point_results in pbar:
            results.extend(point_results)

    # --- Process and Plot Results ---
    print("\nSimulation finished. Processing results for plotting...")
    
    # Unzip the results for plotting
    bifurcation_V0, bifurcation_peaks = zip(*results)

    end_time = time.time() # Stop the timer
    print(f"Total simulation time: {end_time - start_time:.2f} seconds")

    # Experimental Data from Paper
    V_exp_bifurcation = [1.915, 4.645, 5.235, 5.365, 5.395, 5.401]
    periods = [2, 4, 8, 16, 32, 64]

    # Plotting
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(bifurcation_V0, bifurcation_peaks, 'k.', markersize=0.8, alpha=0.8, label='Simulation')

    for i, v_exp in enumerate(V_exp_bifurcation):
        label = f'Exp. Period-{periods[i]} Bifurcation' if i == 0 else None
        ax.axvline(x=v_exp, color='red', linestyle='--', linewidth=1.0, alpha=0.7)

    # Create a single legend entry for the red lines
    ax.plot([], [], color='red', linestyle='--', label='Experimental Bifurcation Points')


    ax.set_title('Simulated vs. Experimental Bifurcation in R-L-D Circuit', fontsize=16)
    ax.set_xlabel('Driving Voltage Amplitude $V_0$ (V)', fontsize=12)
    ax.set_ylabel('Diode Peak Voltage $V_D$ (V)', fontsize=12)
    ax.set_xlim(V0_range[0], V0_range[-1])
    ax.set_ylim(0, 2.0)
    ax.legend()
    plt.tight_layout()
    plt.show()