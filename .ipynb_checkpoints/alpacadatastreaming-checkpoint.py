from alpaca.trading.client import TradingClient
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from alpaca.data.enums import CryptoFeed
from alpaca.data.enums import DataFeed
import asyncio
from alpaca.data.live import CryptoDataStream
import pandas as pd
import threading


#


import pandas as pd
import asyncio
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.data.live import CryptoDataStream

# Initialize empty DataFrame
df = pd.DataFrame(columns=['T', 'S', 'bp', 'bs', 'ap', 'as', 't'])

endpoint = 'https://paper-api.alpaca.markets'
API_KEY = 'PK6OJ8TDPLJ0COVLA084'
API_SECRET = '9jDumPY06ACzRCc8rK9vKKcXsSUBh5VdupyuPBmN'

trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

crypto_stream = CryptoDataStream(API_KEY, API_SECRET, raw_data=True)

async def quote_data_handler(data):
    global df  # Make sure you're modifying the global df variable

    # Append the new data to the DataFrame
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    print(data)


    # Start the append task, if it hasn't been started already
    if 'append_task' not in globals():
        globals()['append_task'] = asyncio.create_task(append_df())

crypto_stream.subscribe_quotes(quote_data_handler, "BTC/USD")

async def append_df():
    global df  # Make sure you're modifying the global df variable

    while True:
        # Wait for 60 seconds
        print('in Async loop')
        await asyncio.sleep(60)

        # Get the last 60 seconds of data
        one_minute_ago = pd.Timestamp.now() - pd.Timedelta(minutes=1)
        last_minute_df = df[df['t'] > one_minute_ago]

        # Append the last minute's data to the DataFrame
        df = pd.concat([df, last_minute_df], ignore_index=True)

        # Write the DataFrame to a CSV file
        print(df)
        df.to_csv('crypto_data.csv', index=False)

# Start the WebSocket stream
threading.Thread(target=crypto_stream.run).start()

