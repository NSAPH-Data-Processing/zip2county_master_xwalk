# ZIP --> FIPS master crosswalk

This pipeline pulls crosswalks from the U.S. Department of Housing and Urban Development (HUD) database, compiling a comprehensive ZIP --> FIPS crosswalk from 2010 to 2023.

In order to run the pipeline, build a conda environment with the following command.

```
conda env create -f requirements.yaml
conda activate zip_fips_master_xwalk 
```

It is also possible to use `mamba` using the same commands.

In order to use the pipeline, you must also have an API token for the HUD database. Instructions on how to quickly and freely obtain an API token can be found at this [link](https://www.huduser.gov/portal/dataset/uspszip-api.html). Then export the API as a global variable.

```
export HUD_API_TOKEN="your-token-here"
```

`snakemake` is the preferred way to run the pipeline. To run the pipeline with default parameters, simply run:
```
snakemake --cores 1
```

To modify any of the default parameters, modify the `config.yaml` file or pass the `-C` flag to snakemake followed by your desired parameters.
```
snakemake --cores 1 -C min_year={min_year} max_year={max_year} quarter={quarter} criteria={criteria} xwalk_method={xwalk_method}
```

Output crosswalks for default parameters and several different `xwalk_method` parameters can be found on the Harvard Dataverse ([link] https://dataverse.harvard.edu/dataverse/zip2fips_crosswalk/)

## Data information

Crosswalks are important data files that help researchers translate between different geographies. For example, a researcher might have hospitalization data at the ZIP-code level but other variables at the U.S. county (FIPS) level. If the analysis is going to be conducted at the FIPS level, it would be important to convert ZIP-level hospitalizations into FIPS-level hospitalizations.

ZIP and FIPS boundaries, like many government-established geographic structures, are dynamic and change from year to year. Some ZIP or FIPS codes exist in 2010 but are retired once new post office or census data arrives in 2020. The U.S. Department of Housing and Urban Development (HUD) bases their crosswalks on address data from the U.S. Postal Service (USPS), and this data also changes! 

### Parameter adjustment

In its default form, which we call `xwalk_criteria = "one2one"`, this crosswalk pipeline outputs the one "best" matching FIPS for every ZIP code for each year from 2010 to 2023. 

|zip  |fips |year|tot_ratio|
|-----|-----|----|---------|
|84712|49017|2016|1.0000000|
|84712|49031|2017|0.6666667|
|84712|49031|2018|0.6666667|
|84712|49031|2019|0.6666667|
|84712|49031|2020|0.6666667|
|84712|49017|2021|0.8928571|

Matches were determined by finding the FIPS code that contained the highest number of addresses from a given ZIP code, `tot_ratio`. It is also possible to set the configuration parameter `criteria` to `bus_ratio`, `res_ratio`, or `oth_ratio` which represent business addresses, residential addresses, and other addresses. These other criteria may provide lower numbers of zip matches depending on the area and years considered.

While the majority of ZIP-codes fall neatly into a single FIPS code, a significant fraction--roughly 15%--have at least 10% of addresses in a second, non-primary county. While certain types of analyses, especially those dealing with count data, may ignore this nuance, it may be important to keep in mind for other kinds of research. This pipeline can also return a more detailed breakdown of *all* the FIPS codes that have at least some shared addresses with a given FIPS code. We call this `xwalk_criteria = "one2few"`. 

|zip  |fips |year|tot_ratio|top_match|
|-----|-----|----|---------|---------|
|84712|49017|2016|1.0000000|True     |
|84712|49031|2017|0.6666667|True     |
|84712|49017|2017|0.3333333|False    |
|84712|49031|2018|0.6666667|True     |
|84712|49017|2018|0.3333333|False    |
|84712|49031|2019|0.6666667|True     |

In this case, the column `top_match` indicates if the `fips` in that row is the highest-ranking match for the given `zip` in that specific `year`. Other options for crosswalk output are `one2one_summy` and `one2few_summy`, which simplify the data frame output through summarizing it across years. The following is example output from the pipeline with `xwalk_method=one2one_summy`:

|zip  |fips |min_year|max_year|tot_ratio_avg|tot_ratio_min|tot_ratio_max|
|-----|-----|--------|--------|-------------|-------------|-------------|
|84712|49017|2010    |2016    |1.0000000    |1.0000000    |1.0000000    |
|84712|49031|2017    |2020    |0.6666667    |0.6666667    |0.6666667    |
|84712|49017|2021    |2023    |0.9036797    |0.8928571    |0.9090909    |


The `min_year`, `max_year`, and `quarter` parameters control the minimum year for crosswalk analysis (data not available before 2010), maximum year for crosswalk analysis (maximum is 2023 at time of writing), and quarter for crosswalk analysis (default = 4).