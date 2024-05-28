import pandas as pd
from pathlib import Path
import argparse
import csv


parser = argparse.ArgumentParser(description='Cleans HUD zipcode-county crosswalk for given year and quarter')
parser.add_argument('--min_year', type=int, default=None, help='Minimum year for xwalk range, inclusive')
parser.add_argument('--max_year', type=int, default=None, help='Maximium year for xwalk range, inclusive')
parser.add_argument('--quarter', type=int, default=None, help='Quarter for crosswalk')
parser.add_argument('--wd', type=str, help='Working dir for pipeline')

args = parser.parse_args()
min_year = args.min_year
max_year = args.max_year
quarter = args.quarter
wd = args.wd

data_files = wd + "/data/intermediate"
infile = wd + "/data/intermediate/zip2fips_raw_download_{quarter}{year}.csv"
outfile = wd + "/data/intermediate/zip2fips_xwalk_clean.csv"
year_range = range(min_year, max_year+1)

name_mapper= {"county": "fips"}


# takes crosswalk and does column renaming, adds leading zeroes, changes to stringxs
def clean_xwalk(year, quarter):
    # read in csv
    df = pd.read_csv(infile.format(quarter=str(quarter), year=str(year)))

    # column re-naming and setting new types
    df.rename(columns=str.lower, inplace=True)
    df.rename(columns=name_mapper, inplace=True)
    df["fips"] = df["fips"].astype(str).str.zfill(5)
    df["zip"] = df["zip"].astype(str).str.zfill(5)
    df["year"] = year
    df["quarter"] = quarter

    return(df)

# cleaning list of xwalks and store in list for concatenation 
xwalk_lst = []
for year in year_range:
    print("Cleaning: year " + str(year) + " quarter " + str(quarter) + "...")
    xwalk_lst.append(clean_xwalk(year=year, quarter= quarter))


outdf = pd.concat(xwalk_lst)
print("Saving: " + str(outfile) + "...")
outdf.to_csv(outfile, index=False)