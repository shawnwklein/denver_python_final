import logging
import argparse
import requests
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_covid_data():
    file = "full_data.csv"
    if not os.path.exists(file) or args.refresh:
        url = f"https://covid.ourworldindata.org/data/ecdc/{file}"
        logger.info(f"Downloading file from {url}")
        try:
            d = pd.read_csv("https://covid.ourworldindata.org/data/ecdc/full_data.csv")
        except:
            logger.critical(f"Could not download data from {url}")
            quit()
    else:
        try:
            logger.info(f"Opening {file}")
            d = pd.read_csv(file)
        except:
            logger.critical(f"Could not open {file}")

    d.rename(columns={"b\"date": "date"}, inplace=True)
    d['date'] = pd.to_datetime(d["date"], format="%Y-%m-%d")
    return d


def main():
    data = get_covid_data()

    if args.country:
        locations = np.unique(data["location"])
        logger.info(locations)
        quit()

    if args.for_country:
        if not args.month or not args.year:
            logger.info("Must enter a year and month for you want plotted in the pie chart")
            quit()
        country_data = data.loc[data["location"] == args.for_country]
        plots = ["new_cases", "new_deaths"]
        for i in plots:
            line_plot(i, country_data, "date", i)

        other_countries = data[data.location != "World"][["date", "location", "new_cases"]]
        other_countries["year"] = other_countries["date"].dt.year
        other_countries["month"] = other_countries["date"].dt.month
        other_countries = other_countries[["location", "new_cases", "year", "month"]].groupby(["location", "year", "month"], as_index=False).mean().sort_values(by=["new_cases"], ascending=False)
        other_countries = other_countries[(other_countries.month == args.month) & (other_countries.year == args.year)]
        other_countries = other_countries[["location", "new_cases"]].head(10)
        other_countries = other_countries.set_index("location")
        pie = other_countries.plot.pie(subplots=True, figsize=(8,8), autopct='%1.1f%%')
        plt.legend("",frameon=False)
        plt.axis('off')
        plt.savefig(f"Top 10 new cases pie for {args.month}-{args.year}")


def line_plot(title, df, x, y):
    logger.info(f"Creating {title} line plot")
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(x, y, data=df)
    [ax.spines[side].set_visible(False) for side in ["left", "right", "top", "bottom"]]
    plt.xticks(rotation=60)
    plt.savefig(f"{args.for_country} {title}")


if __name__ == "__main__":

    logger = logging.getLogger()

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser('usage: main.py [-h]')
    parser.add_argument("-r", "--refresh", default=False, action="store_true", dest="refresh")
    parser.add_argument("-l", "--countries", default=False, action="store_true", dest="country")
    parser.add_argument("-c", "--country", dest="for_country")
    parser.add_argument("-m", "--month", dest="month", type=int)
    parser.add_argument("-y", "--year", dest="year", type=int)
    args = parser.parse_args()

    logger.info('CMD arguments: ' + str(parser.parse_args()))

    main()

