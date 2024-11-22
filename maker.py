from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Literal
import numpy as np

@dataclass
class OrderType:
    """
    Data class to represent the order type, which can be either "limit" or "market"
    """
    type: Literal["limit", "market"]
    from_time: int
    to_time: int

    def __init__ (self, type: Literal["limit", "market"], from_time: int, to_time: int):
        self.type = type
        self.from_time = from_time
        self.to_time = to_time

    def __str__(self):
        return f"OrderType(type={self.type}, from_time={self.from_time}, to_time={self.to_time})"
    
    def new_limit_order(from_time: int, to_time: int):
        """
        Create a new limit order with the given from_time and to_time
        """
        return OrderType("limit", from_time, to_time)
    
    def new_market_order(timestamp: int):
        """
        Create a new market order with the given timestamp
        """
        return OrderType("market", timestamp, timestamp)

class MarketMaker(ABC):
    """
    Abstract class for market maker, where each player will use previous interval data to make decisions
    to buy or sell stocks. The market maker will return the bid and ask prices, and the volume to buy and sell.
    The bid price represents the highest amount a buyer is willing to pay for a stock, 
    while the ask price describes the lowest level at which a seller is willing to sell their shares
    """
    @abstractmethod
    def update(self, prev_bid_price, prev_ask_price, holding, money, timestamp) -> Tuple[float, int, float, int, OrderType]:
        """
        Update the market maker with the previous bid and ask prices, and the timestamp of the current interval,
        and return the new bid and ask prices, and the volume to buy and sell

        There are two type of order you can make each time interval: market order and limit order.

        Market order: an order to buy or sell a stock at the current market price. The buy and sell price
        is determined by the market (not you). Market order doesn't have a time frame. If you are setting the
        next bid price and next ask price for a market order, it will be defaulted to the market bid and ask price.

        Limit order: an order to buy or sell a stock at a specific price or better. 
        A buy limit order can only be executed at the limit price or lower (compare to market ask/sell price), 
        and a sell limit order can only be executed at the limit price or higher (compare to market bid/buy price). 
        Limit order have a time frame, from_time and to_time, which specifies the time interval in which the
        order is valid.

        Market order have higher priority than limit order. If you are setting both market order and limit order
        in a given time interval, the market order will be executed first.

        :param prev_bid_price: the previous bid price
        :param prev_ask_price: the previous ask price
        :param holding: the number of stocks you are holding from previous interval
        :param money: the amount of money you have from previous interval
        :param timestamp: the timestamp of the current (not previous) interval

        :return: a tuple containing the new bid price limit, the volume to buy, the new ask price limit, 
        the volume to sell, and the order type as OrderType object
        """
        pass

class SimpleMarketMaker(MarketMaker):
        """
        An example on how to implement a market maker.
        """
        def __init__(self):
            self.prev_bid_history = []
            self.prev_ask_history = []
            
            """
            Stats for our previous bid/asks orders:
            For amount bought/sold calculations
            """
            self.prev_mm_bid_price_history = []
            self.prev_mm_ask_price_history = []
            self.prev_mm_bid_amt_history = []
            self.prev_mm_ask_amt_history = []
            self.prev_holding_history = []
            self.prev_money_history = []
            
            self.spread_pct = 0.5

            self.window = 10
            self.simulations = 10
            self.sim_horizon = 3
                      
        """
        Example on how to implement the update method for the market maker.

        This example will return the previous bid price and ask price, and the volume to buy and sell
        as 100, and a new limit order with the timestamp and timestamp + 100.

        To return a market order, you can use OrderType.new_market_order(timestamp)
        ```
        return prev_bid_price, 100, prev_ask_price, 100, OrderType.new_market_order(timestamp)
        ```
        For market order, the limit price will be defaulted to the market bid and ask price.

        Note that the volume to buy and sell can be any integer value, including 0. If the volume is negative,
        it will be set to 0. If the volume to sell is more than the holding, it will be set to the holding.

        :param prev_bid_price: the previous bid price
        :param prev_ask_price: the previous ask price
        :param holding: the number of stocks you are holding from previous interval
        :param money: the amount of money you have from previous interval
        :param timestamp: the timestamp of the current (not previous) interval

        :return: a tuple containing the new bid price limit, the volume to buy, the new ask price limit,
        the volume to sell, and the order type as OrderType object

        """
        def update(self, prev_bid_price, prev_ask_price, holding, money, timestamp) -> Tuple[float, int, float, int, OrderType]:
             
            self.prev_bid_history.append(prev_bid_price)
            self.prev_ask_history.append(prev_ask_price)
            self.prev_money_history.append(money)
            self.prev_holding_history.append(holding)
            
            """
            Calculate amount bought and sold in last round
            """

            if len(self.prev_bid_history) <= 1:
                """
                no prev amt history
                
                Currently implementing naive split spread strategy
                Buy at halfway between previous bid and midpoint
                Sell at halfway between midpoint and previous ask
                """
                p_diff = prev_ask_price - prev_bid_price
                cur_bid = prev_bid_price + p_diff/4
                cur_ask = prev_ask_price - p_diff/4
                
                prev_mm_bid_price_history.append(cur_bid)
                prev_mm_ask_price_history.append(cur_ask)

                prev_mm_bid_amt_history.append(((money//cur_bid)//2))
                prev_mm_ask_amt_history.append(0)
                
                """trying to do it on a quicker limit order time scale
                same amount scale for now"""
                return cur_bid, ((money//cur_bid)//2),cur_ask, 0,OrderType.new_limit_order(timestamp, timestamp + 1)
                                   
            diff_money = money - self.prev_money_history[len(self.prev_money_history)-1]
            diff_hold = holding - self.holding_history[len(self.prev_holding_history)-1]
            mm_prev_bid_price = self.prev_mm_bid_price_history[len(self.prev_mm_bid_price_history) - 1]
            mm_prev_ask_price = self.prev_mm_ask_price_history[len(self.prev_mm_ask_price_history) - 1]

            prev_bid_amt = self.prev_mm_bid_amt_history[self.prev_mm_bid_amt_history.len -1]
            prev_ask_amt = self.prev_mm_ask_amt_history[self.prev_mm_ask_amt_history.len -1]
            
            prev_bid_filled = (diff_money - mm_prev_ask_price * diff_hold) / (prev_ask_price - prev_bid_price)
            prev_ask_filled = (diff_money - mm_prev_bid_price * diff_hold) / (prev_ask_price - prev_bid_price)

            """
            implementing new semi-naive strategy, where we go self.spread_pct out from the mean price

            we adjust this self.spread_pct based on how much orders got filled
            We are targeting getting around 75% of our orders being filled

            There's more math to this in Grossman-Miller, we can figure that out
            """
            if ((prev_bid_filled/prev_bid_amt) + (prev_ask_filled/prev_ask_amt))/2 > 0.75:
                """
                reduce spread_pct
                """
                self.spread_pct-= 0.005
                """
                artificial cap on max spread down
                """
                self.spread_pct = min(self.spread_pct, 0.9)
            else:
                """
                increase spread_pct
                """
                self.spread_pct += 0.005
                """
                artificial cap on max spread down
                """
                self.spread_pct = max(self.spread_pct, 0.1)


            mean, std = self.simulate()
            
            buy_dev = std * -0.1
            sell_dev = std * 0.1
            
            max_buy_price = prev_bid_price + buy_dev
            max_sell_price = prev_ask_price + sell_dev
            
            """return max_buy_price, int(money/max_buy_price - 1) // 2, max_sell_price, holding//2, OrderType.new_limit_order(timestamp, timestamp + 1)
            """

            diff_p = (prev_ask_price - prev_bid_price) * self.spread_pct
            midpoint = (prev_ask_price + prev_bid_price) / 2

            cur_bid = midpoint - diff_p
            cur_ask = midpoint + diff_p

            prev_mm_bid_price_history.append(cur_bid)
            prev_mm_ask_price_history.append(cur_ask)

            prev_mm_bid_amt_history.append(((money//cur_bid)//2))
            prev_mm_ask_amt_history.append(holdings//2)

            return cur_bid, ((money//cur_bid)//2), cur_ask, holdings//2, OrderType.new_limit_order(timestamp, timestamp + 1)
        
        def simulate(self): 
            if len(self.prev_bid_history) < self.window: 
                avg_orig_price = (self.prev_bid_history[0] + self.prev_ask_history[0])/2
                return avg_orig_price, 0.05 * avg_orig_price
            
            price_history = (np.array(self.prev_bid_history[-self.window:]) + np.array(self.prev_ask_history[-self.window:])) / 2
            diffs = np.diff(np.log(price_history))
            
            std = np.std(diffs) ** 2
            drift = np.mean(diffs) + std ** 2 / 2
            
            future = []
            for _ in range(self.simulations): 
                future.append(np.cumsum(np.random.normal(drift, std, self.sim_horizon)))
                
            future_prices_estimates = price_history[-1] * np.exp(np.array(future))

            return np.mean(future_prices_estimates), np.std(future_prices_estimates)  