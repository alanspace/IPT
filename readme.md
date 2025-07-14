# High-Precision Measurement of the Feigenbaum Constant in an R-L-D Circuit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the pdf file, Python simulation script, and final report for the research paper: **"High-Precision Experimental Determination and Theoretical Modeling of the Feigenbaum Constant in a Driven Nonlinear R-L-D Oscillator."**

This project presents an experimental and theoretical investigation into the period-doubling route to chaos. It goes beyond a standard replication by validating experimental results with a high-fidelity numerical simulation written in Python, achieving excellent agreement with theory.

## Key Result: Simulation vs. Experiment

The primary result of this work is the close agreement between the experimental data and a numerical simulation based on a first-principles model of the circuit. The simulation, run on multiple CPU cores for efficiency, successfully reproduces the period-doubling cascade and the onset of chaos observed in the laboratory.

![Simulation vs. Experiment Plot](simulation_vs_experiment.png)
*Figure 1: The final bifurcation diagram plotting the results of the numerical simulation (black points) against the bifurcation points measured experimentally (red dashed lines).*

## Key Features

*   **Detailed Theoretical Model:** Derives the circuit's governing second-order nonlinear differential equation using the Shockley diode equation.
*   **High-Precision Experimental Data:** Utilizes data from an automated laboratory setup for precise measurement of bifurcation points.
*   **Parallelized Python Simulation:** Includes a heavily commented Python script that uses `multiprocessing` and `scipy` to numerically solve the system's ODE and generate the bifurcation diagram efficiently.
*   **Rigorous Uncertainty Analysis:** Calculates the final value of Feigenbaum's constant, $\delta$, with a statistically sound uncertainty.


## How to Reproduce the Results

You can reproduce both the PDF report and the simulation plot using the files in this repository.


## Execute the Script**

Run the script from your terminal. It will automatically use all available CPU cores to speed up the computation and show a progress bar.

```bash
python bifurcation.py
```

The script will take a few minutes to run. When it's finished, it will print the total simulation time and display the final plot on your screen. The plot will also be saved as `simulation_vs_experiment.png`.

## Abstract

> The universality of the period-doubling route to chaos, characterized by the Feigenbaum constant $\delta$, is a cornerstone of nonlinear dynamics... *(The rest of your excellent abstract goes here)*

## Citation

If you use this work for reference, please cite it as follows:

```bibtex
@misc{Leung2025Feigenbaum,
  author       = {Leung, Shek Lun Alan},
  title        = {High-Precision Experimental Determination and Theoretical Modeling of the Feigenbaum Constant in a Driven Nonlinear R-L-D Oscillator},
  year         = {2025},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/alanspace/IPT}}
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.