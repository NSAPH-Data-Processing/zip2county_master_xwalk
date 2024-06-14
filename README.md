## ZIP --> FIPS master crosswalk

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
