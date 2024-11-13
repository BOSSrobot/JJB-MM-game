from simulation import Simulation
from maker import SimpleMarketMaker as MarketMaker

DURATION = 100

def admin_run(logging=False):
    sum_profit = 0
    for i in range(DURATION):
        mm = MarketMaker()
        sim = Simulation(mm)
        sim.run(logging=False, fast=False)
        profit = sim.get_final_profit()
        if(logging):
            print("Iteration: ", i)
        sum_profit += profit

    print(f"Average profit: {sum_profit/DURATION}")

admin_run()