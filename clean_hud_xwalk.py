import pandas as pd
from pathlib import Path
import argparse
import csv


parser = argparse.ArgumentParser(description='Cleans HUD zipcode-county crosswalk for given year and quarter')
parser.add_argument('--min_year', type=int, default=None, help='Minimum year for xwalk range, inclusive')
parser.add_argument('--max_year', type=int, default=None, help='Maximium year for xwalk range, inclusive')
parser.add_argument('--wd', type=str, help='Working dir for pipeline')
parser.add_argument('--min_quarter', type=int, default=1, help='Quarter start for crosswalk')
parser.add_argument('--max_quarter', type=int, default=4, help='Quarter end for crosswalk')

args = parser.parse_args()
min_year = args.min_year
max_year = args.max_year
min_quarter = args.min_quarter
max_quarter = args.max_quarter
wd = args.wd

data_files = wd + "/data/intermediate"
infile = wd + "/data/intermediate/zip2fips_raw_download_{quarter}{year}.csv"
outfile = wd + "/data/intermediate/zip2fips_xwalk_clean.csv"
year_range = range(min_year, max_year+1)

name_mapper= {"geoid": "fips",
              "county": "fips"}


dtype_dict = {
    "zip" : int,
    "fips": int,
    "res_ratio": float,
    "bus_ratio": float,
    "oth_ratio": float,
    "tot_ratio": float,
}



# takes crosswalk and does column renaming, adds leading zeroes, changes to stringxs
def clean_xwalk(year, quarter):
    # read in csv
    df = pd.read_csv(infile.format(quarter=str(quarter), year=str(year)))

    # column re-naming and setting new types
    df.rename(columns=str.lower, inplace=True)
    df.rename(columns=name_mapper, inplace=True)
    df = df.dropna(subset=["zip", "fips"])
    df = df.astype(dtype_dict)

    # adding leading zeroes
    df["fips"] = df["fips"].astype(str).str.zfill(5)
    df["zip"] = df["zip"].astype(str).str.zfill(5)
    df["year"] = year
    df["quarter"] = quarter

    return(df[["zip", "fips", "res_ratio", 
              "bus_ratio", "oth_ratio", 
              "tot_ratio", "year", "quarter"]])

# cleaning list of xwalks and store in list for concatenation 
xwalk_lst = []
for y in year_range:
    for q in range(1, 5):
        if y == max_year and q > max_quarter:
            break
        elif y == min_year and q < min_quarter:
            pass
        else:
            print("Cleaning: year " + str(y) + " quarter " + str(q) + "...")
            xwalk_lst.append(clean_xwalk(year=y, quarter=q))


outdf = pd.concat(xwalk_lst)
print("Saving: " + str(outfile) + "...")
outdf.to_csv(outfile, index=False)