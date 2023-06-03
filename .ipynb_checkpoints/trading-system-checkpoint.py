import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
from functools import reduce
import datetime
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Importing the Data
myPath = r"C:\Users\rrain\Desktop\trading\Crude-Trading-System-Code\Crude-Trading-System\bb_crude_data.xlsx"
my_ohlc_data = pd.read_excel(myPath)# Converting to Array
my_ohlc_data.tail(20)
# my_ohlc_data = np.array(my_ohlc_data)


def SMA(data, ndays): 
    # SMA addition for each column - based on close price
    data["{0}SMA".format(ndays)] = data['Close'].rolling(ndays).mean()
    return data

def EMA(data,ndays):
    # EMA Calculation - preferred calc method for moving averages.
    data["{0}EMA".format(ndays)] = data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean()
    
    return data
    
def core_logic(data=pd.DataFrame()): #trading logic - generate a buy and sell signals
    # Generate signal: If 9SMA > 21MA
    data = data.set_index('Dates')
    
    # Account for NaN values
    data = data[data.index > '2010-05-10'] #start the rolling window at 5/10/2010
    
    # Create Signal & Position Column
    data['Signal'] = np.where(data['9EMA'] > data['21EMA'], 1, 0)
    data['Position'] = data['Signal'].diff()
    print(data.tail(15))
    return data

# creating the 9 & 21 Day moving averages
df = EMA(my_ohlc_data,9)
df = EMA(my_ohlc_data,21)

# create buy / sell signals
df = core_logic(data=df)


def ohlc_plot_sma(df):
    fig = go.Figure(data=[
                    go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'], 
                        close=df['Close'],
                        name = 'WTI Prompt Month Contract - CL1'
                                        ),
                    go.Scatter(
                        x=df.index,
                        y=df['9EMA'],
                        name = '9EMA')]
                   )
                   
    fig.add_trace(go.Scatter(
                    x=df.index, 
                    y=df['21EMA'],
                    mode='lines',
                    name='21EMA')
                 
                 )
    # buy signals
    fig.add_trace(go.Scatter(
                    x=df[df['Position'] == 1].index, 
                    y=df['9EMA'][df['Position'] == 1],
                    mode='markers',
                    name='Buy',
                    marker_symbol='triangle-up',
                    marker_color='green',
                    marker_size=14))
    
    # sell signals
    fig.add_trace(go.Scatter(
                    x=df[df['Position'] == -1].index, 
                    y=df['21EMA'][df['Position'] == -1],
                    mode='markers',
                    name='Sell',
                    marker_symbol='triangle-down',
                    marker_color='red',
                    marker_size=14))
    
    fig.update_layout(xaxis_rangeslider_visible=False,width=1800, height=1300)
    fig.show()
ohlc_plot_sma(df=df)