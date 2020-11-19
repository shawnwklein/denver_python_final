import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import requests
import datetime
import os
import numpy as np
import matplotlib.ticker as tick
from matplotlib.ticker import NullFormatter
import logging


def get_file():
    file = 'output.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        url = 'https://query1.finance.yahoo.com/v7/finance/download/%5EDJI?period1=1573593278&period2=1605215678&interval=1d&events=history&includeAdjustedClose=true'
        df = pd.read_csv(url)

    df['Date'] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df['Volume'] = df['Volume'].astype("int")
    df['Volume'] = df['Volume'] / 1000000000
    df = df.loc[df["Date"] > "2020-01-01"]
    return df


def RSI(data):

    # RSI
    time_window = 14
    diff = data.diff(1).dropna()  # diff in one field(one day)

    # this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[diff > 0]
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[diff < 0]

    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi


def plots(Ticker):
    # date_vs_volume
    df = get_file()

    current_date = datetime.date.today()
    df1 = yf.download(Ticker, "2020-01-01", current_date)

    values = np.array(['Volume', 'Adj Close', 'RSI'])
    for axis in values:

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
        ax1 = fig.add_axes([0.1, 0.50, 0.85, 0.40])  # l,b,w,h
        ax2 = fig.add_axes([0.1, 0.10, 0.85, 0.35])

        # RSI
        if axis == 'RSI':
            df1['RSI'] = RSI(df1['Adj Close'])
            ax1.plot(df1['Adj Close'])
            ax1.set_ylabel(Ticker + '\n Price')
            ax1.set_title(Ticker + ' RSI Chart')
            ax1.grid(linestyle='--')

            ax2.plot(df1['RSI'], color='red')
            ax2.grid(linestyle='--')
            ax2.axhline(20, linestyle='-', alpha=0.5)
            plt.axhline(80, linestyle='-', alpha=0.5)

        # Volume and Price
        else:
            ax1.plot(df1[axis])
            ax1.set_ylabel(Ticker + '\n' + axis)
            ax1.grid(linestyle='--')

            ax2.plot(df[axis])
            ax2.set_xlabel('Trading days')
            ax2.set_ylabel('Dow Jones \n' + axis)
            ax2.grid(linestyle='--')
            if axis == 'Volume':
                ax1.set_title('Volume of DJI Vs ' + Ticker + ' Chart')
                ax2.text(0.1, 0.9, 'Volume = 10^9',
                    verticalalignment='center', horizontalalignment='center',
                    transform=ax2.transAxes,
                    color='black', fontsize=15)
            else:
                ax1.set_title('Price of DJI Vs ' + Ticker + ' Chart')
        plt.savefig(axis)




if __name__ == '__main__':
    '''
    logger = logging.getLogger()
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)
    '''

    plots('MSFT')









