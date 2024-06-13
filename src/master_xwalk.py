import pandas as pd
import numpy as np
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
#quarter = args.quarter
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
    "tot_ratio": float,
    "year": int,
    "quarter": int,
    "usps_zip_pref_city": str,
    "usps_zip_pref_state": str
}

# def get_quarter(dat, fun):
#     return(((fun(dat) % 1)* 4) +1)

# tbd on data type here. 
def find_match(fname_in, fname_out, criteria, agg=True, method1=True):
    # load xwalk
    #fname_in = ""
    print("Starting zip-fips matching...")
    df = pd.read_csv(fname_in, dtype=dtype_dict)
    df["year_float"] = df['year'] + (df['quarter'] - 1)*0.25


    # grouping df
    idxs = df.groupby(["zip", "year", "quarter"])[criteria].idxmax()
    df_match = df.loc[idxs, ["zip", "fips", "year", "year_float", criteria]]

    rows_lst = []
    count=0
    if method1:
        df_match = df_match.sort_values(["zip", "year_float"])
        # iterate through every zip code, find all best matching fips
        for z in df_match['zip'].unique():
            # set initial values
            count +=1
            if count % 500 == 0:
                print(count)
            df_z = df_match[df_match["zip"] == z].reset_index(drop=True)
            y_low = df_z.iloc[0]["year_float"]
            y_high = df_z.iloc[0]["year_float"]
            curr_match = df_z.iloc[0]["fips"]
            crit_vals = [df_z.iloc[0][criteria]]
            total_matches = 1
            # iterate through zip-code subset
            for idx in range(1, len(df_z)):
                #print(r)
                r = df_z.iloc[idx]
                if curr_match != r["fips"]:
                    #print("hello")
                    crit_vals.append(r[criteria])
                    rows_lst.append({"zip": z, "fips": curr_match, 
                                    "min_year": y_low, "max_year": y_high,
                                    'total_matches': total_matches, 
                                    f'{criteria}_avg': np.mean(crit_vals), 
                                    f'{criteria}_min': np.min(crit_vals), 
                                    f'{criteria}_max': np.max(crit_vals)})
                    y_low = r["year_float"]
                    y_high = r["year_float"]
                    curr_match = r["fips"]
                    crit_vals = [r[criteria]]
                    total_matches = 1
                else:
                    y_high = r["year_float"]
                    crit_vals.append(r[criteria])
                    total_matches += 1
            rows_lst.append({"zip": z, "fips": curr_match, 
                                    "min_year": y_low, "max_year": y_high,
                                    'total_matches': total_matches, 
                                    f'{criteria}_avg': np.mean(crit_vals), 
                                    f'{criteria}_min': np.min(crit_vals), 
                                    f'{criteria}_max': np.max(crit_vals)})
        print("Saving: " + str(fname_out) + "...")
        df_agg = pd.DataFrame.from_dict(rows_lst)
        df_agg.to_csv(fname_out, index=False)
        print("Done")
    elif agg:
        # getting summary stats across all years and quarters
        df_match["year_float_str"] = df['year_float'].astype(str)
        df_agg = df_match.groupby(['zip', 'fips']).agg(
            **{#'min_year':('year', 'min'),
                #'max_year':('year', 'max'),
                'all_matching_years':('year_float_str', lambda x: ','.join(x)),
                'min_year_float':('year_float', 'min'),
                'max_year_float':('year_float', 'max'),
                # 'min_quarter': ('year_float', lambda x: get_quarter(x, min)),
                # 'max_quarter': ('year_float', lambda x: get_quarter(x, max)),
                'total_matches':('year', 'count'),
                f'{criteria}_avg': (criteria, 'mean'),
                f'{criteria}_min': (criteria, 'min'),
                f'{criteria}_max': (criteria, 'max')}
            ).reset_index()
        
        print("Saving: " + str(fname_out) + "...")
        df_agg.to_csv(fname_out, index=False)
        print("Done")
    else:
        # writing matches to csv
        print("Saving: " + str(fname_out) + "...")
        df_match.to_csv(fname_out, index=False)

find_match(fname_in = infile,
           fname_out = outfile.format(min_year=str(min_year), 
                                        max_year = str(max_year), 
                                        criteria = criteria),
            criteria=criteria)


# # order by year
# # select one zip at a time, filter df
# # iterate through rows, is match the same? if yes bump up max year, add criteria to lst
# # is match diff? Set new match, export criteria stats

# df = pd.read_csv("data/intermediate/zip2fips_xwalk_clean.csv")
# df = df.loc[df["quarter"] == 4]
# df['group'] = (df['year'] - df.groupby(['zip', 'fips']).cumcount()).astype(str)

# result = df.groupby(['zip', 'fips', 'group']).agg(
#     start_year=('year', 'min'),
#     end_year=('year', 'max'),
#     mean_total_ratio=('tot_ratio', 'mean'),
#     max_total_ratio=('tot_ratio', 'max')
# ).reset_index()

# result.to_csv("test.csv")


# # one-to-one. usage case, want 
# df = pd.read_csv("data/intermediate/zip2fips_xwalk_clean.csv", dtype=dtype_dict)
# df = df.loc[df["quarter"] == 4]
# idxs = df.groupby(["zip", "year", "quarter"])[criteria].idxmax()
# df_match = df.loc[idxs, ["zip", "fips", "year", criteria]]
# df_match['group'] = (df_match['year'] - df_match.groupby(['zip', 'fips']).cumcount()).astype(str)
# df_agg = df_match.groupby(['zip', 'fips', 'group']).agg(
#             **{'min_year':('year', 'min'),
#                 'max_year':('year', 'max'),
#                 'total_matches':('year', 'count'),
#                 f'{criteria}_avg': (criteria, 'mean'),
#                 f'{criteria}_min': (criteria, 'min'),
#                 f'{criteria}_max': (criteria, 'max')}
#             ).reset_index()
# #df_match['cumcount'] = df.groupby(['zip', 'fips']).cumcount()).astype(str)

# df_match.loc[df_match["zip"] == "84712"]
# df_agg = df_agg.drop(columns="group")
# df_agg.loc[df_agg["zip"] == "84712"]


# # one-to-a few. usage case, want precise weights on a yearly resolution
# cutoff = 0.05
# criteria = "tot_ratio"
# # trying another method
# df = pd.read_csv("data/intermediate/zip2fips_xwalk_clean.csv", dtype=dtype_dict)
# df = df.loc[(df["quarter"] == 4) & (df[criteria] > cutoff)]
# df.loc[df["zip"] == "84712"]