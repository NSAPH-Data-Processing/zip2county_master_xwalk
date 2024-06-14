import pandas as pd
#import os.path
from pathlib import Path
import argparse
from urllib.error import HTTPError
import requests

# temporary argument situation
parser = argparse.ArgumentParser(description='Downloads HUD zipcode-county crosswalk for given year and quarter')
parser.add_argument("api_token", type=str, help="Token for HUD API (required)")
parser.add_argument('--min_year', type=int, default=2010, help='Minimum year for xwalk range, inclusive')
parser.add_argument('--max_year', type=int, default=2023, help='Maximium year for xwalk range, inclusive')
parser.add_argument('--quarter', type=int, default=4, help='Quarter to be used for data downloading')

args = parser.parse_args()
min_year = args.min_year
max_year = args.max_year
api_token = args.api_token
quarter = args.quarter

URL_PATTERN = "https://www.huduser.gov/portal/datasets/usps/ZIP_COUNTY_{month}{year}.xlsx"
outfile = "data/input/zip2fips_raw_download_{quarter}{year}.csv"
year_range = range(min_year, max_year+1)

M2Q = {
        1: "03",
        2: "06",
        3: "09",
        4: "12"
    }


def download_xwalk(quarter, year):
    if quarter not in range(1,5):
        raise ValueError("Quarter must be between 1 and 4: " + str(quarter))
    elif year not in range(2010, 2025):
        raise ValueError("Year must be between 2010 and 2024, inclusive")
    # if csv is already downloaded, don't download again
    else:
        out_pth = Path(outfile.format(quarter=str(quarter), year=str(year)))
        url = "https://www.huduser.gov/hudapi/public/usps?type=2&query=All&year={year}&quarter={quarter}".format(quarter=str(quarter), year=str(year))
        headers = {"Authorization": "Bearer {0}".format(api_token)}

        print("Downloading: " + url + " ...")
        response = requests.get(url, headers = headers)

        if response.status_code != 200:
            print ("Failure, see status code: {0}".format(response.status_code))
        else: 
            df = pd.DataFrame(response.json()["data"]["results"])	
            #df: pd.DataFrame = pd.read_excel(url)
            print("Saving: " + str(out_pth) + " ...")
            df.to_csv(out_pth, index=False)


# downloading list of xwalks
for y in year_range:
    download_xwalk(quarter=quarter, year=y)
