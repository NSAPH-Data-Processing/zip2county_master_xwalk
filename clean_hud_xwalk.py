import pandas as pd
from pathlib import Path
import argparse
import csv


parser = argparse.ArgumentParser(description='Cleans HUD zipcode-county crosswalk for given year and quarter')
parser.add_argument('--year', type=int, help='Year for crosswalk')
parser.add_argument('--quarter', type=int, help='Quarter for crosswalk')
parser.add_argument('--wd', type=str, help='Working dir for pipeline')

args = parser.parse_args()
year = args.year
quarter = args.quarter
wd = args.wd

#wd = "/Users/jck019/desktop/nsaph/data_team/zip-fips-crosswalk"
data_files = wd + "/data/intermediate"
infile = wd + "/data/intermediate/zip2fips_raw_download_{quarter}{year}.csv"
outfile = wd + "/data/intermediate/zip2fips_clean_{quarter}{year}.csv"


# name_mapper= {"ZIP": "zip",
#               "COUNTY": "fips",
#               "RES_RATIO": "res_ratio",
#               "BUS_RATIO": "bus_ratio",
#               "OTH_RATIO": "oth_ratio",
#               "TOT_RATIO": "tot_ratio"}

name_mapper= {"county": "fips",}


def clean_xwalk(quarter, year):
    # read in csv
    df = pd.read_csv(infile.format(quarter=str(quarter), year=str(year)))

    # column re-naming and setting new types
    df.rename(columns=str.lower, inplace=True)
    df.rename(columns=name_mapper, inplace=True)
    df["fips"] = df["fips"].astype(str).str.zfill(5)
    df["zip"] = df["zip"].astype(str).str.zfill(5)

    # writing file
    out_pth = Path(outfile.format(quarter=str(quarter), year=str(year)))
    #if not out_pth.exists():
    print("Saving: " + str(out_pth) + "...")
    df.to_csv(out_pth, index=False)

clean_xwalk(quarter= quarter, year=year)


# later
    # df["fips"] = df.fips.apply(lambda x: "{:05d}".format(x)).astype(str)
    # df["zip"] = df.zip.apply(lambda x: "{:05d}".format(x)).astype("str")
