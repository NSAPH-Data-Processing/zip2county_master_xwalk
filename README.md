[![](<https://img.shields.io/badge/Dataverse-10.7910/DVN/SYNPBS-orange>)](https://doi.org/10.7910/DVN/0U2TCB)

# Zip code to county master crosswalk

This pipeline pulls crosswalks from the U.S. Department of Housing and Urban Development (HUD) database, compiling a comprehensive ZIP code to county crosswalk from 2010 to 2023.

In order to run the pipeline, build a conda environment with the following command.

```
conda env create -f requirements.yaml
conda activate zip2county_master_xwalk 
```

It is also possible to use `mamba` using the same commands.

You need to have an API token for the HUD database in order to use the pipeline. Instructions on how to quickly and freely obtain an API token can be found at this [link](https://www.huduser.gov/portal/dataset/uspszip-api.html). Make sure to export the API as a global variable.

```
export HUD_API_TOKEN="your-token-here"
```
**Link entrypoints to data placeholders** Add symlinks to input, intermediate and output folders inside the corresponding `/data` subfolders by running:

```bash
python utils/create_data_paths.py datapaths=cannon_datapaths
```

`snakemake` is the preferred way to run the pipeline. To run the pipeline with default parameters, simply run:
```
snakemake --cores 1
```

To modify any of the default parameters, modify the `config.yaml` file or pass the `-C` flag to snakemake followed by your desired parameters.
```
snakemake --cores 1 -C min_year={min_year} max_year={max_year} criteria={criteria} xwalk_method={xwalk_method}
```

### Dockerized Pipeline

Create the folder where you would like to store the output dataset.

```bash 
mkdir <path>/zip2county_master_xwalk/
```

Create your own docker image
```bash
docker build -t <image_name> .
```

Then run the docker container
```bash
docker run -v <path>/zip2county_master_xwalk/:/app/data/output --env HUD_API_TOKEN=$HUD_API_TOKEN <image_name>
```

If you are also interested in storing the raw and intermediate data run

```bash
docker run -v <path>/zip2county_master_xwalk/:/app/data/ --env HUD_API_TOKEN=$HUD_API_TOKEN <image_name>
```

And modifications to default arguments can also be made as follows:
```bash
docker run -v <path>/zip2county_master_xwalk/:/app/data/ --env HUD_API_TOKEN=$HUD_API_TOKEN <image_name> -C min_year={min_year} max_year={max_year}
```

Output crosswalks for default parameters and several different `xwalk_method` parameters can be found on the Harvard Dataverse [https://doi.org/10.7910/DVN/0U2TCB](https://doi.org/10.7910/DVN/0U2TCB). To cite with Bibtex use:
```
@data{DVN/0U2TCB_2024,
author = {Kitch, James},
publisher = {Harvard Dataverse},
title = {{ZIP Code to County Crosswalk}},
year = {2024},
version = {DRAFT VERSION},
doi = {10.7910/DVN/0U2TCB},
url = {https://doi.org/10.7910/DVN/0U2TCB}
}
```

## Data information

Crosswalks assist researchers in translating data between different geographic units. For instance, a researcher might have hospitalization data at the ZIP-code level but other relevant variables at the U.S. county level. If the analysis is to be conducted at the county level, it's crucial in most traditional study designs to convert ZIP-level hospitalizations to county-level hospitalizations.

Both ZIP code and county boundaries, like many government-established geographic structures, are dynamic and change over time. While counties generally remain consistent, they can occasionally be subject to changes such as boundary adjustments, renaming, or splitting into new counties, usually due to administrative decisions or legislative actions. ZIP codes, managed by the U.S. Postal Service, are also subject to change.

This pipeline uses crosswalks from the U.S. Department of Housing and Urban Development (HUD), maintained on a quarterly basis, to facilitate these translations. Only Q4 crosswalks are used to construct the master crosswalk in this pipeline, though intermediate quarterly crosswalks are also downloaded. Differences between quarterly crosswalks within a year (e.g., Q3 2020 and Q4 2020) are typically minor. A brief overview of these differences is provided in `notes/notes.Rmd`.

### Parameter adjustment

In its default form, which we call `xwalk_criteria = "one2one"`, this crosswalk pipeline outputs the one "best" matching county for every ZIP code for each year from 2010 to 2023. 

|zip  |county |year|tot_ratio|
|-----|-----|----|---------|
|84712|49017|2016|1.0000000|
|84712|49031|2017|0.6666667|
|84712|49031|2018|0.6666667|
|84712|49031|2019|0.6666667|
|84712|49031|2020|0.6666667|
|84712|49017|2021|0.8928571|

Matches were determined by finding the county code that contained the highest number of addresses from a given ZIP code, `tot_ratio`. It is also possible to set the configuration parameter `criteria` to `bus_ratio`, `res_ratio`, or `oth_ratio` which represent business addresses, residential addresses, and other addresses. These other criteria may provide lower numbers of zip matches depending on the area and years considered.

While the majority of ZIP-codes fall neatly into a single county, a significant fraction--roughly 15%--have at least 10% of addresses in a second, non-primary county. While certain types of analyses, especially those dealing with count data, may ignore this nuance, it may be important to keep in mind for other kinds of research. This pipeline can also return a more detailed breakdown of *all* the counties that have at least some shared addresses with a given FIPS code. We call this `xwalk_criteria = "one2few"`. 

|zip  |county |year|tot_ratio|top_match|
|-----|-----|----|---------|---------|
|84712|49017|2016|1.0000000|True     |
|84712|49031|2017|0.6666667|True     |
|84712|49017|2017|0.3333333|False    |
|84712|49031|2018|0.6666667|True     |
|84712|49017|2018|0.3333333|False    |
|84712|49031|2019|0.6666667|True     |

In this case, the column `top_match` indicates if the `county` in that row is the highest-ranking match for the given `zip` in that specific `year`. Other options for crosswalk output are `one2one_summy` and `one2few_summy`, which simplify the data frame output through summarizing it across years. The following is example output from the pipeline with `xwalk_method=one2one_summy`:

|zip  |county |min_year|max_year|tot_ratio_avg|tot_ratio_min|tot_ratio_max|
|-----|-----|--------|--------|-------------|-------------|-------------|
|84712|49017|2010    |2016    |1.0000000    |1.0000000    |1.0000000    |
|84712|49031|2017    |2020    |0.6666667    |0.6666667    |0.6666667    |
|84712|49017|2021    |2023    |0.9036797    |0.8928571    |0.9090909    |


The `min_year` and `max_year`, and parameters control the minimum year for crosswalk analysis (data not available before 2010), maximum year for crosswalk analysis (maximum is 2023 at time of writing). 