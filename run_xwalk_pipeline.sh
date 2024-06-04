#!/bin/bash

# script that runs hud pipeline script. Proper script usage:
# ./run_xwalk_pipeline <quarter> <min_year> <max_year> <criteria>

# Check if the correct number of arguments are provided
if [ "$#" -ne 4 ] && [ "$#" -ne 6 ]; then
    echo "Usage: $0 <min_year> <max_year> <criteria> <api_token> <min_quarter> <max_quarter>"
    exit 1
fi

# Assign arguments to variables
min_year=$1
max_year=$2
criteria=$3
api_token=$4
min_quarter=${5:-1}
max_quarter=${6:-4}

# # Validate quarter
# if ! [[ "$min_quarter" =~ ^[1-4]$ ]] || ! [[ "$max_quarter" =~ ^[1-4]$ ]]; then
#     echo "Error: min_quarter and max_quarter should be an integer between 1 and 4."
#     exit 1
# fi

# Validate min_year and max_year
if ! [[ "$min_year" =~ ^[0-9]{4}$ ]] || ! [[ "$max_year" =~ ^[0-9]{4}$ ]]; then
    echo "Error: min_year and max_year should be four-digit integers."
    exit 1
fi

# Ensure min_year and max_year are between 2010 and 2021
if [ "$min_year" -lt 2010 ] || [ "$min_year" -gt 2024 ]; then
    echo "Error: min_year should be between 2010 and 2021."
    exit 1
fi

if [ "$max_year" -lt 2010 ] || [ "$max_year" -gt 2024 ]; then
    echo "Error: max_year should be between 2010 and 2021."
    exit 1
fi

if [ "$min_year" -gt "$max_year" ]; then
    echo "Error: min_year should be less than or equal to max_year."
    exit 1
fi

# Print the provided arguments
echo "Minimum Year: $min_year"
echo "Maximum Year: $max_year"
echo "Criteria: $criteria"
echo "Minimum Quarter: $min_quarter"
echo "Maximum Quarter: $max_quarter"

working_dir="$(dirname "$(readlink -f "$0")")"
echo $working_dir

python3 $working_dir/download_hud_xwalk.py --min_year $min_year \
    --max_year $max_year --wd $working_dir --token $api_token \
    --min_quarter $min_quarter --max_quarter $max_quarter
python3 $working_dir/clean_hud_xwalk.py --min_year $min_year \
    --max_year $max_year --wd $working_dir \
    --min_quarter $min_quarter --max_quarter $max_quarter
python3 $working_dir/find_county_matches.py --min_year $min_year \
    --max_year $max_year --wd $working_dir \
    --criteria $criteria