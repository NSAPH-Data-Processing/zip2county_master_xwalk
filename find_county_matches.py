import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Finds county match for given zip code')
parser.add_argument('--min_year', type=int, help='Minimum year for xwalk range, inclusive')
parser.add_argument('--max_year', type=int, help='Maximium year for xwalk range, inclusive')
parser.add_argument('--wd', type=str, help='Working dir for pipeline')
parser.add_argument('--criteria', 
                    type=str, default="total_ratio", 
                    help='Method to determine crosswalk groupings by')

args = parser.parse_args()
min_year = args.min_year
max_year = args.max_year
wd = args.wd
criteria = args.criteria

# input/output file setup
infile = wd + "/data/intermediate/zip2fips_xwalk_clean.csv"
outfile = wd + "/data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}.csv"

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
def find_match(fname_in, fname_out, criteria):
    # load xwalk
    df = pd.read_csv(fname_in, dtype=dtype_dict)
    
    # grouping df
    idxs = df.groupby(["zip", "year", "quarter"])[criteria].idxmax()
    df_match = df.loc[idxs, ["zip", "fips", "year", "quarter", criteria]]

    # writing matches to csv
    df_match.to_csv(fname_out, index=False)
    #return(df_match)

find_match(fname_in = infile,
           fname_out = outfile.format(min_year=str(min_year), 
                                        max_year = str(max_year), 
                                        criteria = criteria),
            criteria=criteria)