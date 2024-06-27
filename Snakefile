import os
configfile: "config.yaml"

# Read default values from the config file
min_year = config["min_year"]
max_year = config["max_year"]
criteria = config["criteria"]
xwalk_method = config["xwalk_method"]
quarter = config["quarter"]

rule all:
    input:
        f"data/output/zip2fips_master_xwalk_{min_year}_{max_year}_{criteria}_{xwalk_method}.csv"

rule download_hud_xwalks:
    output:
        expand("data/input/zip2fips_raw_download_{year}Q{quarter}.csv", year=range(min_year, max_year+1), quarter=quarter)
    shell:
        """
        python src/download_hud_xwalk.py --min_year {min_year} --max_year {max_year}
        """

rule create_clean_hud_xwalks:
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