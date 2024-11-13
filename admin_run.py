from simulation import Simulation
from maker import SimpleMarketMaker as MarketMaker
import sys

DURATION = 10

def admin_run():
    for i in range(DURATION):
        print(f"Running simulation iteration {i+1}")
        mm = MarketMaker()
        sim = Simulation(mm)
        sim.run(logging=False, fast=False)
        print(f"Simulation iteration {i+1} complete")