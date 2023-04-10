from fastapi import APIRouter
from config.db import conn
import requests
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import mysql.connector
import json
import numpy as np
from mysql.connector import errorcode

app = APIRouter()

async def fetch_ticker_data(ticker):
    data = yf.download(ticker, start="2020-01-01", end="2023-04-10")
    return data['Adj Close']

def save_ticker_data(ticker,data):
    df = pd.DataFrame(data,columns=[ticker])
    df.to_sql(ticker, conn, if_exists='replace', index=False)

def get_ticker_data(tickers):
    data = {}
    for ticker in tickers:
        ticker_data = fetch_ticker_data(ticker)
        save_ticker_data(ticker, ticker_data)
        data[ticker] = ticker_data

    return pd.DataFrame(data)

def correlation_analysis(ticker_data):
    corr_matrix = ticker_data.corr()
    fig, ax = plt.subplots()
    ax.imshow(corr_matrix)
    ax.set_xticks(np.arange(len(ticker_data.columns)))
    ax.set_yticks(np.arange(len(ticker_data.columns)))
    ax.set_xtickslabels(ticker_data.columns)
    ax.set_yticklabels(ticker_data.columns)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    plt.savefig('correlation.png')

    return corr_matrix


def save_correlation_data(correlation_matrix):
    df = pd.DataFrame(correlation_matrix)
    df.to_sql('correlation', conn, if_exists='replace',index=False)

def save_results_to_database(tickers):
    ticker_data = get_ticker_data(tickers)
    correlation_matrix = correlation_analysis(ticker_data)
    save_correlation_data(correlation_matrix)
    collection_data = {'tickers':tickers, 'image_path': 'correlation.png'}
    collection_json = json.dumps(collection_data)
    with conn.connect() as connection:
        connection.execute('INSERT INTO collection (data) VALUES (%s)', collection_json)

input_json = '{ticker:["APPL","GOOG","TSLA"]}'
input_data = json.loads(input_json)
tickers = input_data['ticker']

save_results_to_database(tickers)