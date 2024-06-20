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
        "data/intermediate/zip2fips_xwalk_clean.csv"

rule download_hud_xwalks:
    output:
        f"data/input/zip2fips_raw_download_{{year}}Q{quarter}.csv" # year is a wildcard
    shell:
        f"""
        python src/download_hud_xwalk.py --api_token {api_token} --year {{wildcards.year}} 
        """ # year is a wildcard

rule create_clean_uds:
    input:
        expand(f"data/input/zip2fips_raw_download_{{year}}Q{quarter}.csv", 
        year=year_list) # year is a wildcard
    output:
        "data/intermediate/zip2fips_xwalk_clean.csv"
    shell:
        f"python src/clean_hud_xwalk.py --min_year {min_year} --max_year {max_year}"

rule master_xwalk:
    input:
        "data/intermediate/zip2fips_xwalk_clean.csv"
    output:
        f"data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}_{xwalk_method}.csv"
    shell:
        f"""
        python src/master_xwalk.py --min_year {min_year} --max_year {max_year} \
            --criteria {criteria} --xwalk_method {xwalk_method}
        """