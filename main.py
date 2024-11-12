from simulation import Simulation
from maker import SimpleMarketMaker as MarketMaker
import sys

def main():
    print("Welcome to the game!")
    mm = MarketMaker()
    sim = Simulation(mm)
    
    # Check for -f flag
    fast = '-f' in sys.argv
    
    sim.run(logging=True, fast=fast)
    sim.summarize(logging=True)
    

if __name__ == "__main__":
    main()