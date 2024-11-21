from simulation import Simulation
from maker import SimpleMarketMaker, MarketMaker, OrderType
from typing import List, Tuple, Literal
from abc import ABCMeta

import numpy as np
import pandas as pd
from time import time

import seaborn as sns
import matplotlib.pyplot as plt

class DataTracker:
    def __init__(self, save_csv: str = None):
        self.save_csv = save_csv
        self.information = []
        
        self.more_info = []
        self.column_names = None
        
    def update(self, *args):
        self.information.append([*args])
        
    def config_info(self, column_names: str): 
        self.column_names = column_names
    
    def update_info(self, *args):
        self.more_info.append([*args])

    def close(self): 
        default_cols = ["Market Bid Price", "Market Ask Price", "Holding", "Money", "Timestamp", 
                        "Bid Price", "Bid Vol", "Ask Price", "Ask Vol"]
        data = pd.DataFrame(self.information, columns = default_cols)

        if self.more_info: 
            data2 = pd.DataFrame(self.more_info, columns = self.column_names)
            data = pd.concat([data, data2], axis = 1)
        
        data.set_index('Timestamp', inplace=True)
        
        if self.save_csv: 
            data.to_csv(self.save_csv)

        return data
    
# A metaclass intended to automatically log data provided 
class DataMarketMakerMeta(ABCMeta):
    
     def __new__(cls, name, bases, dct):
            
        dct['tracker'] = DataTracker()

        update_method = dct.get("update") or any(hasattr(base, "update") for base in bases)
        
        if not update_method: 
            raise ValueError("MarketMaker ")
            
        def tracking_update(self, *args):
            info = [*args]
            actions = list(update_method(self, *args))
            self.tracker.update(*(info + actions[:-1])) # Get rid of the limit order from tracking
            return tuple(actions)
        
        dct['update'] = tracking_update
        
        def close(self):
            return self.tracker.close()
        
        dct['close'] = close
        
        return super().__new__(cls, name, bases, dct)
    
class DataMarketMaker(MarketMaker, metaclass = DataMarketMakerMeta):
    pass

def plot_defaults(data, additional_cols: List = None):
    df = data.reset_index()
    df['Market Spread'] = (df['Market Ask Price'] - df['Market Bid Price']).rolling(window=100).mean()
    df['Market Price'] = ((df['Market Ask Price'] + df['Market Bid Price']) / 2).rolling(window=10).mean()

    df['Agent Spread'] = (df['Ask Price'] - df['Bid Price']).rolling(window=100).mean()
    df['Agent Price'] = ((df['Ask Price'] + df['Bid Price']) / 2).rolling(window=10).mean()

    sns.set(style="whitegrid")

    columns_to_plot = ['Market Price', 'Agent Price', 'Market Spread', 'Agent Spread',
                       'Holding', 'Money', 'Bid Vol', 'Ask Vol']

    if additional_cols: 
        columns_to_plot += additional_cols
    
    fig, axes = plt.subplots(len(columns_to_plot), 1, figsize=(10, 2 * len(columns_to_plot)))

    for ax, column in zip(axes, columns_to_plot):
        sns.lineplot(data=df, x='Timestamp', y=column, ax=ax)
        ax.set_title(f'{column} over Time')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel(column)

    plt.tight_layout()
    plt.show()
    
def run_mm(mm: MarketMaker): 
    
    print("Running")
    start = time()

    sim = Simulation(mm)
    sim.run(logging=True)
    sim.summarize(logging=True)

    end = time()
    print(f"Game completed in {end - start} seconds")
    
def run_mm_plus(mm: DataMarketMaker): 
    run_mm(mm)
    return mm.close()