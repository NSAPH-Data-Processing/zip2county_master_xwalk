import os
configfile: "config.yaml"

# Read default values from the config file
min_year = config["min_year"]
max_year = config["max_year"]
criteria = config["criteria"]
xwalk_method = config["xwalk_method"]
quarter = config["quarter"]

API_TOKEN = os.getenv("HUD_API_TOKEN")

rule all:
    input:
        f"data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}_{xwalk_method}.csv"

rule download_uds_xwalks:
    output:
        expand("data/input/zip2fips_raw_download_{year}Q{quarter}.csv", year=range(min_year, max_year+1), quarter=quarter)
    shell:
        """
        python src/download_hud_xwalk.py $HUD_API_TOKEN --min_year {min_year} --max_year {max_year}
        """

rule create_clean_uds:
    input:
        expand("data/input/zip2fips_raw_download_{year}Q{quarter}.csv", year=range(min_year, max_year+1), quarter=quarter)
    output:
        "data/intermediate/zip2fips_xwalk_clean.csv"
    shell:
        "python src/clean_hud_xwalk.py --min_year {min_year} --max_year {max_year}"

rule master_xwalk:
    input:
        "data/intermediate/zip2fips_xwalk_clean.csv"
    output:
        f"data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}_{xwalk_method}.csv"
    shell:
        """
        python src/master_xwalk.py --min_year {min_year} --max_year {max_year} \
            --criteria {criteria} --xwalk_method {xwalk_method}
        """