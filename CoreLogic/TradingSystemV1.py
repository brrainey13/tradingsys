import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

class TradingSystem:
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path)
        self.data['Cash Position'] = 0.0
        self.data['Portfolio Value'] = 0.0
        self.data['PnL'] = 0.0
        self.cash_position = 25000.0
        self.portfolio_value = 0.0
        self.pnl = 0.0
        self.buy_price = 0.0

    def SMA(self, ndays): 
        self.data["{0}SMA".format(ndays)] = self.data['Close'].rolling(ndays).mean()

    def EMA(self, ndays):
        self.data["{0}EMA".format(ndays)] = self.data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean()

    def core_logicv1(self): 
        self.data = self.data.set_index('Dates')
        self.data = self.data[self.data.index > '2010-05-10'] 
        std_dev = self.data['9EMA'].std()
        self.data['Signal'] = np.where((self.data['9EMA'] > self.data['21EMA']) & (std_dev > .5) , 1, 0)
        self.data['Position'] = self.data['Signal'].diff()
     
    def core_logic(self, **signals_and_weights): 
        self.data = self.data.set_index('Dates')
        self.data = self.data[self.data.index > '2010-05-10']

        # Initial signal is always true
        self.data['Signal'] = np.ones(len(self.data))

        # Update the signal based on each function
        for signal_function, weight in signals_and_weights.items():
            self.data['Signal'] = np.where(self.data['Signal'] & (signal_function(self.data) * weight), 1, 0)
        
        self.data['Position'] = self.data['Signal'].diff() 

    def calculate_PnL(self):
        for i, row in self.data.iterrows():
            if row['Position'] == 1:
                self.cash_position -= row['Close']
                self.portfolio_value = row['Close']
                self.buy_price = row['Close']  
            elif row['Position'] == -1:
                self.cash_position += row['Close']
                self.pnl += row['Close'] - self.buy_price  
                self.portfolio_value = 0.0
            else:
                if self.portfolio_value > 0:  
                    self.portfolio_value = row['Close']  

            self.data.at[i, 'Cash Position'] = self.cash_position
            self.data.at[i, 'Portfolio Value'] = self.portfolio_value
            self.data.at[i, 'PnL'] = self.pnl

    def plot_data(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data.index, self.data['Close'], label='Close Price', color='blue', alpha=0.5)
        plt.plot(self.data.index, self.data['9EMA'], label='9 Day EMA', color='red', alpha=0.9)
        plt.plot(self.data.index, self.data['21EMA'], label='21 Day EMA', color='green', alpha=0.9)
        plt.plot(self.data[self.data['Position'] == 1].index, self.data['9EMA'][self.data['Position'] == 1], '^', markersize=10, color='m', label='buy signal')
        plt.plot(self.data[self.data['Position'] == -1].index, self.data['21EMA'][self.data['Position'] == -1], 'v', markersize=10, color='k', label='sell signal')
        plt.title('9 EMA and 21 EMA')
        plt.legend()
        plt.show()

    def save_data(self):
        self.data.to_csv('trading-output-test.csv')
        
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# Load the data from the Excel file
x = find('bb_crude_data.xlsx', os.getcwd())
data = pd.read_excel(x)
trading_system = TradingSystem(x)
trading_system.EMA(9)
trading_system.EMA(21)
trading_system.core_logicv1()
trading_system.calculate_PnL()
trading_system.plot_data()
trading_system.save_data()
