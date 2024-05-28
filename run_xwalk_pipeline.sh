#!/bin/bash

# script that runs hud pipeline script. Proper script usage:
# ./run_xwalk_pipeline 

WD="/Users/jck019/desktop/nsaph/data_team/zip-fips-crosswalk"
quarter=1
year=2018
zipcode="02478,02138,39564,43081"

python3 $WD/download_hud_xwalk.py --year $year --quarter $quarter --wd $WD
python3 $WD/clean_hud_xwalk.py --year $year --quarter $quarter --wd $WD
python3 $WD/find_county_matches.py --zipcode $zipcode --year $year --quarter $quarter --wd $WD