# takes cleaned, concatenated xwalk files and creates master xwalk according to given method and criteria
import pandas as pd
import argparse

CRITERIA_LST = ["tot_ratio", "res_ratio", "bus_ratio", "oth_ratio"]
DTYPE_DICT = {
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

# Returns one-to-one matches
def make_one2one(df, criteria):
    print("Starting zip-fips matching...")
    # one match per zip per year according to criteria
    idxs = df.groupby(["zip", "year"])[criteria].idxmax()
    df_match = df.loc[idxs, ["zip", "fips", "year", criteria]]

    return df_match

# Returns "summary format" of one-to-one matches
def make_one2one_summy(df, criteria):
    df_match = make_one2one(df, criteria)
    # keeping track of "breaks" in best matches
    df_match['group'] = (df_match['year'] - df_match.groupby(['zip', 'fips']).cumcount()).astype(str)

    # return aggregated df with summy statistics
    df_agg = df_match.groupby(['zip', 'fips', 'group']).agg(
        **{
        "min_year": ('year', 'min'),
        "max_year": ('year', 'max'),
        f'{criteria}_avg': (criteria, 'mean'),
        f'{criteria}_min': (criteria, 'min'),
        f'{criteria}_max': (criteria, 'max')}
    ).reset_index()

    df_agg = df_agg.sort_values(["zip", "min_year"])
    df_agg = df_agg.drop(columns=["group"])

    return(df_agg)

# Returns weighted zip2fips matches
def make_one2few(df, criteria, cutoff=0.05):
    idxs = df.groupby(["zip", "year"])[criteria].idxmax()
    df['top_match'] = df.index.isin(idxs)
    df = df.loc[(df[criteria] > cutoff)]
    return(df[["zip", "fips", "year", criteria, 'top_match']])


# Returns summaries of weighted one2few matches
def make_one2few_summy(df, criteria, cutoff = 0.05):
    # make one2few matches
    df = make_one2few(df=df, criteria=criteria, cutoff=cutoff)

    # add indicator if it is an exact match
    df['exact_match'] = df[criteria].apply(lambda x: True if x > 1-cutoff else False)

    # identify consecutive years, return aggregated
    df['group'] = (df['year'] - 
                    df.groupby(['zip', 'fips', "exact_match", 'top_match']).cumcount()).astype(str)
    df_agg = df.groupby(['zip', 'fips', 'group', 'top_match']).agg(
                **{'min_year':('year', 'min'),
                    'max_year':('year', 'max'),
                    'total_matches':('year', 'count'),
                    f'{criteria}_avg': (criteria, 'mean'),
                    f'{criteria}_min': (criteria, 'min'),
                    f'{criteria}_max': (criteria, 'max')}
                ).reset_index()
    
    df_agg = df_agg.sort_values(["zip", "min_year"])
    df_agg = df_agg.drop(columns=["group"])
    return(df_agg)


def main(args):
    # process arguments
    min_year = args.min_year
    max_year = args.max_year
    criteria = args.criteria
    xwalk_method = args.xwalk_method
    cutoff = args.cutoff

    # input/output file setup
    infile = "data/intermediate/zip2fips_xwalk_clean.csv"
    outfile = f"data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}_{xwalk_method}.csv"

    # read df
    df = pd.read_csv(infile, dtype=DTYPE_DICT)

    # execute xwalk creation based on chosen method along with given criteria
    if criteria not in CRITERIA_LST:
        raise ValueError("Unrecognized xwalk criteria. Valid criteria are " + ", ".join(CRITERIA_LST))
    if xwalk_method == "one2one":
        df_out = make_one2one(df=df, criteria=criteria)
    elif xwalk_method == "one2one_summy":
        df_out = make_one2one_summy(df=df, criteria=criteria)
    elif xwalk_method == "one2few":
        df_out = make_one2few(df=df, criteria=criteria, cutoff=cutoff)
    elif xwalk_method == "one2few_summy":
        df_out = make_one2few_summy(df=df, criteria=criteria, cutoff=cutoff)
    else:
        raise ValueError("Unrecognized crosswalk-matching method. Valid methods are 'one2one', 'one2few', and 'one2few_summy'.")
    
    print("Saving: " + str(outfile) + "...")
    df_out.to_csv(outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finds county match for given zip code')
    parser.add_argument('--min_year', 
                        default=2010,
                        type=int, help='Minimum year for xwalk range, inclusive')
    parser.add_argument('--max_year', 
                        default=2012,
                        type=int, 
                        help='Maximium year for xwalk range, inclusive')
    parser.add_argument('--criteria', 
                        choices = ["tot_ratio", "res_ratio", "bus_ratio", "oth_ratio"],
                        default="tot_ratio", 
                        type=str,
                        help='Method to determine crosswalk matches by')
    parser.add_argument('--xwalk_method', 
                        choices = ['one2one', 'one2few','one2one_summy', 'one2few_summy'],
                        default="one2one",
                        type=str, 
                        help='Method to make crosswalk')
    parser.add_argument('--cutoff', type=float, default=0, help='Cutoff to include fips codes in one2few output')
    args = parser.parse_args()
    main(args)