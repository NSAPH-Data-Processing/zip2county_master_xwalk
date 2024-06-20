import os
import pandas as pd
from pathlib import Path
import argparse
import requests

URL_PATTERN = "https://www.huduser.gov/portal/datasets/usps/ZIP_COUNTY_{month}{year}.xlsx"
M2Q = {
        1: "03",
        2: "06",
        3: "09",
        4: "12"
    }

# takes year, quarter, and api token and downloads crosswalk from HUD API
def download_xwalk(year, quarter, api_token, outfile):
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
            print("Saving: " + str(out_pth) + " ...")
            df.to_csv(out_pth, index=False)

def main(args):
    outfile="data/input/zip2fips_raw_download_{year}Q{quarter}.csv"

    # iterate through year range, download xwalk file for each
    year_range = range(args.min_year, args.max_year+1)
    for y in year_range:
        download_xwalk(year=y, 
                       quarter=args.quarter, 
                       api_token=args.api_token, 
                       outfile=outfile)


if __name__ == "__main__":
    api_token = os.getenv("HUD_API_TOKEN")
    parser = argparse.ArgumentParser(description='Downloads HUD zipcode-county crosswalk for given year and quarter')
    parser.add_argument('--api_token', type=str, default=api_token, help='API token for HUD API')
    parser.add_argument('--min_year', type=int, default=2010, help='Minimum year for xwalk range, inclusive')
    parser.add_argument('--max_year', type=int, default=2012, help='Maximium year for xwalk range, inclusive')
    parser.add_argument('--quarter', type=int, default=4, help='Quarter to be used for data downloading')
    args = parser.parse_args()
    main(args)
