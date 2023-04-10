import yfinance as yf 
import mysql.connector
import pandas as pd 
import talipp as tp
import matplotlib.pyplot as plt
from config.db import connection

def analyze_stock(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
  
    conn = connection
    stock_data.to_sql(symbol, conn, if_exists="replace")

    df = pd.read_sql_query(f"Select * from {symbol}", conn)

    ma5 = tp.sma(df["Close"],5)
    ma10 = tp.sma(df["Close"],10)
    ma15 = tp.sma(df["Close"], 15)

    rsi = tp.rsi(df["Close"], 14)

    result = {}
    result["MA5"] = ma5.iloc[-1]
    result["MA10"] = ma10.iloc[-1]
    result["MA15"] = ma15.iloc[-1]

    result1 ={}
    result1["RSI"] = rsi.iloc[-1]

    # Store the results in a collection
    results_collection = {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "moving_average": result,
        "rsi": result1
    }

    # Store the visualization in the file system
    plt.figure(figsize=(12,6))
    plt.plot(df['Close'], label='Close Price')
    plt.plot(ma5, label='MA5')
    plt.plot(ma10, label='MA10')
    plt.plot(ma15, label='MA15')
    plt.legend()
    plt.savefig(f"{symbol}.png")

    return results_collection