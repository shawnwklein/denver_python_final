import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
import os
import numpy as np
import logging
import argparse
import sys

logger = logging.getLogger(__name__)


def get_file():
    file = 'output.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        logger.info(f"read {file} into dataframe")
    else:
        try:
            url = 'https://query1.finance.yahoo.com/v7/finance/download/%5EDJI?period1=1573593278&period2=1605215678&interval=1d&events=history&includeAdjustedClose=true'
            df = pd.read_csv(url)
        except:
            logger.critical('Could not read URL')
            sys.exit()
    df['Date'] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df['Volume'] = df['Volume'].astype("int")
    df['Volume'] = df['Volume'] / 1000000000
    df = df.loc[df["Date"] >= "2020-01-01"]
    df.rename(columns={"Date": "date"}, inplace=True)
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
    # down change is equal to negative difference, otherwise equal to zero
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
    try:
        df1 = yf.download(Ticker, "2020-01-01", current_date)
        logger.info("Downloading data from yfinance.")
    except:
        logger.critical('Could not download data from yfinance.')
        sys.exit()

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
    # use of logging module
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Use of parsing module
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--refresh", default=False, action="store_true", dest="refresh")
    parser.add_argument('-Ticker', dest='T', metavar='<Ticker>', help='Ticker of your choice', default='MSFT')
    args = parser.parse_args()
    T = args.T
    logger.info('CMD arguments: ' + str(parser.parse_args()))

    # Plot charts
    plots(T)
















