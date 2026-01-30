"""
BTB/C Simulation Runner
======================

Educational entrypoint for running BTB/C protocol simulations.

Usage:
    python3 run.py simulation/example.b2b
"""

import sys
from simulation.runner import SimulationRunner


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run.py <simulation_file.b2b>")
        sys.exit(1)

    simulation_file = sys.argv[1]

    runner = SimulationRunner()
    runner.run_file(simulation_file)


if __name__ == "__main__":
    main()
