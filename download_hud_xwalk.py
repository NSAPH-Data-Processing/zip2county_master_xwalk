import pandas as pd
#import os.path
from pathlib import Path
import argparse
from urllib.error import HTTPError
import requests

# temporary argument situation
parser = argparse.ArgumentParser(description='Downloads HUD zipcode-county crosswalk for given year and quarter')
parser.add_argument('--min_year', type=int, default=None, help='Minimum year for xwalk range, inclusive')
parser.add_argument('--max_year', type=int, default=None, help='Maximium year for xwalk range, inclusive')
parser.add_argument('--quarter', type=int, help='Quarter for crosswalk')
parser.add_argument('--wd', type=str, help='Working dir for pipeline')

args = parser.parse_args()
min_year = args.min_year
max_year = args.max_year
quarter = args.quarter
wd = args.wd

TABLE = "public.hud_zip2fips"
URL_PATTERN = "https://www.huduser.gov/portal/datasets/usps/ZIP_COUNTY_{month}{year}.xlsx"
outfile = wd + "/data/intermediate/zip2fips_raw_download_{quarter}{year}.csv"
year_range = range(min_year, max_year+1)

M2Q = {
        1: "03",
        2: "06",
        3: "09",
        4: "12"
    }


# def getXwalk(year, quarter):
#     # helper function to deal with year/quarter adjustments
#     def makeValidTime(year, quarter):
#         if quarter > 4 & quarter < 8:
#             return((year + 1, quarter % 4))
#         elif quarter == 0:
#             return((year - 1, 4))
#         else: 
#             raise ValueError("Invalid quarter argument " + str(quarter))

#     m = M2Q[quarter]
#     url = URL_PATTERN.format(month=m, year=str(year))
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an HTTPError for bad responses
        
#         # Use a BytesIO object to read the Excel file from the response content
#         df = pd.read_excel(response.content)
        
#         # Continue with your processing
#         return df
        
#     except HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#         if year != 2024:
#             getXwalk()
#     except Exception as err:
#         print(f'Other error occurred: {err}')
#     else:
#         print('File read successfully')

# helper function to deal with year/quarter adjustments
def makeValidTime(year, quarter):
    if quarter > 4 & quarter < 8:
        return((year + 1, quarter % 4))
    elif quarter == 0:
        return((year - 1, 4))
    else: 


def getXwalk(year, quarter):
    m = M2Q[quarter]
    url = URL_PATTERN.format(month=m, year=str(year))
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # Use a BytesIO object to read the Excel file from the response content
        df = pd.read_excel(response.content)
        
        # Continue with your processing
        return df
        
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if year != 2024:
            getXwalk()
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('File read successfully')


def download_xwalk(quarter, year):
    # checking quarter/year parameters
    if quarter not in range(1,4):
        raise ValueError("Quarter must be between 1 and 4: " + str(quarter))
    elif year not in range(2010, 2024):
        raise ValueError("Year must be between 2010 and 2023")
    # if csv is already downloaded, don't download again
    else:
        out_pth = Path(outfile.format(quarter=str(quarter), year=str(year)))
        if out_pth.exists():
            print("Crosswalk for Q" + str(quarter) + " " + str(year) + " already downloaded")
        # download csv
        else:
            m = M2Q[quarter]
            url = URL_PATTERN.format(month=m, year=str(year))
            print("Downloading: " + url + " ...")
            df: pd.DataFrame = pd.read_excel(url)
            print("Saving: " + str(out_pth) + " ...")
            df.to_csv(out_pth, index=False)


# downloading list of xwalks
for year in year_range:
    download_xwalk(quarter=quarter, year=year)
