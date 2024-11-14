import math
from simulation import Simulation
from maker import SimpleMarketMaker as MarketMaker

DURATION = 10

def admin_run(logging=False):
    sum_profit = 0
    i = 0
    while(i < DURATION):
        mm = MarketMaker()
        sim = Simulation(mm)
        sim.run(logging=False, fast=False)
        profit = sim.get_final_profit()
        if(logging):
            print(profit, math.isnan(profit))
        if math.isnan(profit):
            continue
        sum_profit += profit
        i += 1

    print(f"Average profit: {sum_profit/DURATION}")

admin_run(True)