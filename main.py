import logging
import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import covid_main
import dow_main

logger = logging.getLogger(__name__)


def main():
    cd = covid_main.get_covid_data()
    covid_main.create_cases_death_plots(cd, args.for_country, args.month, args.year)
    covid_main.create_pie_plot(cd, args.month, args.year)
    dd = dow_main.get_file()
    dow_main.plots(args.ticker)

    merged = pd.merge(cd, dd, on=["date"])
    merged['new_deaths'] = merged['new_deaths'].replace(np.nan, 0)
    merged['new_cases'] = merged['new_cases'].replace(np.nan, 0)
    merged["norm_deaths"] = (merged["new_deaths"] - merged["new_deaths"].mean()) / (merged["new_deaths"].max() - merged["new_deaths"].min())
    merged["norm_cases"] = (merged["new_cases"] - merged["new_cases"].mean()) / (merged["new_cases"].max() - merged["new_cases"].min())
    merged["norm_volume"] = (merged["Volume"] - merged["Volume"].mean()) / (merged["Volume"].max() - merged["Volume"].min())


    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot("date", "norm_deaths", data=merged)
    ax.plot("date", "norm_volume", data=merged)
    plt.savefig(f"Deaths to Volume")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot("date", "norm_cases", data=merged)
    ax.plot("date", "norm_volume", data=merged)
    plt.savefig(f"Cases to Volume")

    grouped = merged.groupby(["date"]).sum()



    fig, ax = plt.subplots(figsize=(10, 8))
    plt.scatter(grouped["Volume"], grouped["new_deaths"])
    plt.savefig(f"Deaths to Volume Scatter")


    quit()

    covid_main.write_csv(cd, "covid_data.csv", "covid")
    covid_main.write_csv(dd, "dow_data.csv", "dow")


if __name__ == "__main__":

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser('usage: main.py [-h]')
    parser.add_argument("-c", "--country", dest="for_country", default='United States')
    parser.add_argument("-m", "--month", dest="month", type=int, default=11)
    parser.add_argument("-y", "--year", dest="year", type=int, default=2020)
    parser.add_argument("-t", "--ticker", dest="ticker", default='MSFT')
    args = parser.parse_args()

    logger.info('CMD arguments: ' + str(parser.parse_args()))

    main()

