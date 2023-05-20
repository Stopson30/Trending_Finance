import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from backtesting import Backtest, Strategy

class BollingerBandsStrategy(Strategy):
    def init(self):
        self.bbands = BollingerBands(close=self.data.Close, window=20, window_dev=2)
        self.rsi = RSIIndicator(close=self.data.Close, window=14)
        self.upper_band = self.I(self.bbands.bollinger_hband)
        self.lower_band = self.I(self.bbands.bollinger_lband)
        self.rsi_val = self.I(self.rsi.rsi)
        
    def next(self):
        if (self.data.Close[-1] > self.upper_band[-1]) and (self.rsi_val[-1] > 70):
            self.sell()
        elif (self.data.Close[-1] < self.lower_band[-1]) and (self.rsi_val[-1] < 30):
            self.buy()

data = pd.read_csv('AAPL.csv')
data.index = pd.to_datetime(data.Date)
data = data.sort_index()

bt = Backtest(data, BollingerBandsStrategy, cash=10000, commission=.002,
              trailing_stop=True)
stats = bt.run()

print(stats)
bt.plot()
