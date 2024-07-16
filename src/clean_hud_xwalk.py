import pandas as pd
import argparse

NAME_MAPPER = {"geoid": "county",
              "county": "county"}
DTYPE_DICT = {
    "zip" : int,
    "county": int,
    "res_ratio": float,
    "bus_ratio": float,
    "oth_ratio": float,
    "tot_ratio": float,
}

# takes crosswalk and does column renaming, adds leading zeroes, changes to stringxs
def clean_xwalk(year, quarter, infile):
    # read in csv
    df = pd.read_csv(infile.format(quarter=str(quarter), year=str(year)))

    # column re-naming and setting new types
    df.rename(columns=str.lower, inplace=True)
    df.rename(columns=NAME_MAPPER, inplace=True)
    df = df.dropna(subset=["zip", "county"])
    df = df.astype(DTYPE_DICT)

    # adding leading zeroes
    df["county"] = df["county"].astype(str).str.zfill(5)
    df["zip"] = df["zip"].astype(str).str.zfill(5)
    df["year"] = year
    df["quarter"] = quarter

    return(df[["zip", "county", "res_ratio", 
              "bus_ratio", "oth_ratio", 
              "tot_ratio", "year", "quarter"]])

def main(args):
    # cleaning list of xwalks and store in list for concatenation 
    min_year = args.min_year
    max_year = args.max_year

    infile = "data/input/zip2county_raw_download_{year}Q{quarter}.csv"
    outfile = f"data/intermediate/zip2county_xwalk_clean_{min_year}_{max_year}.csv"

    year_range = range(min_year, max_year+1)
    xwalk_lst = []
    for y in year_range:
        for quarter in range(1, 4+1):
            print("Cleaning: year " + str(y) + " quarter " + str(quarter) + "...")
            xwalk_lst.append(clean_xwalk(year=y, quarter=quarter, infile=infile))

    # concatenating list of dfs
    outdf = pd.concat(xwalk_lst)
    print("Saving: " + str(outfile) + "...")
    outdf.to_csv(outfile, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cleans HUD zipcode-county crosswalk for a given year range')
    parser.add_argument('--min_year', type=int, default=2010, help='Minimum year for xwalk range, inclusive')
    parser.add_argument('--max_year', type=int, default=2012, help='Maximium year for xwalk range, inclusive')
    args = parser.parse_args()
    main(args)