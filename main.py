import logging
import argparse
import requests
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_data():
    file = "full_data.csv"
    if not os.path.exists(file) or args.refresh:
        url = "https://covid.ourworldindata.org/data/ecdc/full_data.csv"
        logger.info(f"Downloading file from {url}")
        try:
            r = str((requests.get(url)).content).split("\\n")
            data_file = open(file, 'w', newline='')
        except:
            logger.critical(f"Could not download data from {url}")
            quit()
        for i in r:
            if i[0] != "\"":
                data_file.write(i + "\n")
    else:
        try:
            logger.info(f"Opening {file}")
            data_file = open(file, 'r', newline='')
        except:
            logger.critical(f"Could not open {file}")

    logger.info("Creating panda")
    d = pd.read_csv(file)
    d.rename(columns={"b\"date": "date"}, inplace=True)
    d['date'] = pd.to_datetime(d["date"], format="%Y-%m-%d")
    return d


def main():
    data = get_data()

    if args.country:
        locations = data["location"].unique()
        print(locations)
        quit()

    if args.for_country:
        country_data = data.loc[data["location"] == args.for_country]
        plots = ["new_cases", "new_deaths"]
        for i in plots:
            logger.info(f"Creating {i} line plot")
            fig, ax = plt.subplots()
            ax.plot("date", i, data=country_data)
            [ax.spines[side].set_visible(False) for side in ["left", "right", "top", "bottom"]]
            plt.xticks(rotation=60)
            plt.savefig(f"{args.for_country} {i}")


        #not_us_data = data[data["location"] != args.for_country]
        #print(np.mean(not_us_data["new_cases"]))




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
    args = parser.parse_args()

    logger.info('CMD arguments: ' + str(parser.parse_args()))

    main()

