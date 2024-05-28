import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Finds county match for given zip code')
parser.add_argument('--zipcode', type=str, help='Zip code(s) of interest')
parser.add_argument('--year', type=int, help='Year for crosswalk')
parser.add_argument('--quarter', type=int, help='Quarter for crosswalk')
parser.add_argument('--wd', type=str, help='Working dir for pipeline')

args = parser.parse_args()
zip_codes = args.zipcode.split(",")
year = args.year
quarter = args.quarter
wd = args.wd

# input/output file setup
#wd = "/Users/jck019/desktop/nsaph/data_team/zip-fips-crosswalk"
infile = wd + "/data/intermediate/zip2fips_clean_{quarter}{year}.csv"
outfile = wd + "/data/output/zip2fips_matches_{quarter}{year}_{criteria}.csv"

# full criteria list ["res_ratio", "bus_ratio", "oth_ratio", "tot_ratio"]

dtype_dict = {
    "zip" : str,
    "fips": str,
    "res_ratio": float,
    "bus_ratio": float,
    "oth_ratio": float,
    "tot_ratio": float
}

# tbd on data type here. 
def find_match(zip_lst, quarter, year, criteria = "tot_ratio"):
    # load xwalk
    df = pd.read_csv(infile.format(quarter = str(quarter), year = str(year)),
                     dtype=dtype_dict)
    
    # filter df for zip codes in list
    df = df[df["zip"].isin(zip_lst)]
    idxs = df.groupby("zip")[criteria].idxmax()
    df_match = df.loc[idxs, ["zip", "fips", criteria]]
    df_match["year"] = year
    df_match["quarter"] = quarter

    # writing matches to csv
    df_match.to_csv(outfile.format(quarter=str(quarter), 
                                    year = str(year), 
                                    criteria = str(criteria)),
                    index=False)
    #return(df_match)
    
find_match(zip_lst=zip_codes, quarter=quarter, year=year)