#!/bin/bash

# script that runs hud pipeline script. Proper script usage:
# ./run_xwalk_pipeline 

WD="/Users/jck019/desktop/nsaph/data_team/zip-fips-crosswalk"
quarter=2
min_year=2010
max_year=2023
criteria="tot_ratio"
#year=2018
#zipcode="02478,02138,39564,43081"

python3 $WD/download_hud_xwalk.py --min_year $min_year --max_year $max_year --quarter $quarter --wd $WD
python3 $WD/clean_hud_xwalk.py --min_year $min_year --max_year $max_year --quarter $quarter --wd $WD
python3 $WD/find_county_matches.py --min_year $min_year --max_year $max_year --wd $WD --criteria $criteria