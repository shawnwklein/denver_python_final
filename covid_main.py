import logging
import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv


logger = logging.getLogger(__name__)


def get_covid_data(is_refresh=False):
    file = "full_data.csv"
    if not os.path.exists(file) or is_refresh:
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


def list_counties(data):
    locations = np.unique(data["location"])
    return locations


def create_cases_death_plots(data, country, month, year):
    if not month or not year:
        logger.info("Must enter a year and month for you want plotted in the pie chart")
        quit()
    country_data = data.loc[data["location"] == country]
    plots = ["new_cases", "new_deaths"]
    for i in plots:
        line_plot(i, country_data, "date", i, country)


def line_plot(title, df, x, y, country="United States"):
    logger.info(f"Creating {title} line plot")
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(x, y, data=df)
    [ax.spines[side].set_visible(False) for side in ["left", "right", "top", "bottom"]]
    plt.xticks(rotation=60)
    plt.savefig(f"{country} {title}")


def create_pie_plot(data, month, year):
    other_countries = data[data.location != "World"][["date", "location", "new_cases"]]
    other_countries["year"] = other_countries["date"].dt.year
    other_countries["month"] = other_countries["date"].dt.month
    other_countries = other_countries[["location", "new_cases", "year", "month"]].groupby(["location", "year", "month"],
                                                                                          as_index=False).mean().sort_values(by=["new_cases"], ascending=False)
    other_countries = other_countries[(other_countries.month == month) & (other_countries.year == year)]
    other_countries = other_countries[["location", "new_cases"]].head(10)
    other_countries = other_countries.set_index("location")
    pie = other_countries.plot.pie(subplots=True, figsize=(8, 8), autopct='%1.1f%%')
    plt.legend("", frameon=False)
    plt.axis('off')
    plt.savefig(f"Top 10 new cases pie for {month}-{year}")


def write_csv(data, file, covid_or_dow):
    out = open(file, 'w', newline='')
    csvwriter = csv.writer(out)
    recs = []
    logger.info(f"Writing {covid_or_dow} data to file...")
    for i in data.index:
        one_rec = [[]]
        for c in data.columns:
            one_rec[0].append(data.at[i,c])
        recs.append(one_rec)

    csvwriter.writerows(recs)
    out.close()


def main():
    data = get_covid_data()

    if args.country:
        c = list_counties(data)
        logger.info(c)
        quit()

    if args.for_country:
        create_cases_death_plots(data, args.for_country, args.month, args.year)
        create_pie_plot(data, args.month, args.year)


if __name__ == "__main__":

    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser('usage: covid_main.py [-h]')
    parser.add_argument("-r", "--refresh", default=False, action="store_true", dest="refresh")
    parser.add_argument("-l", "--countries", default=False, action="store_true", dest="country")
    parser.add_argument("-c", "--country", dest="for_country")
    parser.add_argument("-m", "--month", dest="month", type=int)
    parser.add_argument("-y", "--year", dest="year", type=int)
    args = parser.parse_args()

    logger.info('CMD arguments: ' + str(parser.parse_args()))

    main()

