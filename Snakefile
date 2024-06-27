import os
configfile: "config.yaml"

# Read default values from the config file
min_year = config["min_year"]
max_year = config["max_year"]
criteria = config["criteria"]
xwalk_method = config["xwalk_method"]
quarter = config["quarter"]

api_token = os.getenv("HUD_API_TOKEN")

year_list = list(range(min_year, max_year+1))
print(year_list)

rule all:
    input:
        f"data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}_{xwalk_method}.csv"

rule download_hud_xwalks:
    output:
        f"data/input/zip2fips_raw_download_{{year}}Q{{quarter}}.csv" # year and quarter are wildcards
    shell:
        f"""
        python src/download_hud_xwalk.py --api_token {api_token} --year {{wildcards.year}} --quarter {{wildcards.quarter}}
        """ # year and quarter are wildcards

rule create_clean_uds:
    input:
        expand("data/input/zip2fips_raw_download_{{year}}Q{{quarter}}.csv", 
        year=year_list, # year is a wildcard
        quarter=list(range(1,4+1)) # quarter is a wildcard
        )
    output:
        f"data/intermediate/zip2fips_xwalk_clean_{min_year}_{max_year}.csv"
    shell:
        f"python src/clean_hud_xwalk.py --min_year {min_year} --max_year {max_year}"

rule master_xwalk:
    input:
        f"data/intermediate/zip2fips_xwalk_clean_{min_year}_{max_year}.csv"
    output:
        f"data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}_{xwalk_method}.csv"
    shell:
        f"""
        python src/master_xwalk.py --min_year {min_year} --max_year {max_year} \
            --criteria {criteria} --xwalk_method {xwalk_method}
        """