#!/bin/python3

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

installments = 4

def burrito_arbitrage(ticker: str, start: str, end: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if data is None:
        exit(1)
    pos = pd.DataFrame()
    pos['open_value'] = data['Close'][ticker]

    for payment in range(1, installments + 1):
        pos[f'close_value_{payment}'] = pos['open_value'].shift(-14 * payment)
        pos[f'profit_{payment}'] = (pos[f'close_value_{payment}'] - pos['open_value']) / pos['open_value'] / installments
    pos['profit'] = pos['profit_1'] + pos['profit_2'] + pos['profit_3'] + pos['profit_4']
    pos['profit_percentage'] = pos['profit'] * 100
    pos = pos.dropna()

    print('Average Return', f'({ticker}): ', f'{pos['profit_percentage'].mean():.3f}%')
    return pos
 
def main():
    start_date = '2010-01-01'
    end_date = '2025-01-01'
    print('Date Range: ', start_date, 'to', end_date)
    spy = burrito_arbitrage('SPY', start_date, end_date)
    qqq = burrito_arbitrage('QQQ', start_date, end_date)
    upro = burrito_arbitrage('UPRO', start_date, end_date)
    tqqq = burrito_arbitrage('TQQQ', start_date, end_date)

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    spy.plot(ax=ax, y='profit_percentage', label='SPY')
    qqq.plot(ax=ax, y='profit_percentage', label='QQQ')
    upro.plot(ax=ax, y='profit_percentage', label='UPRO')
    tqqq.plot(ax=ax, y='profit_percentage', label='TQQQ')
    fig.tight_layout()
    fig.savefig('arbitrage_returns.png', format='png')

if __name__ == "__main__":
    main()
