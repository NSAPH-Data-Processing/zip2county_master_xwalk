## ZIP --> FIPS master crosswalk

This pipeline pulls crosswalks from the U.S. Department of Housing and Urban Development (HUD) database, compiling a comprehensive ZIP --> FIPS crosswalk from 2010 to 2023.

In order to run the pipeline, build a conda environment with the following command.

```
conda env create -f requirements.yml
```

It is also possible to use `mamba`.

In order to use the pipeline, you must also have an API token for the HUD database. Instructions on how to quickly and freely obtain an API token can be found at this [link](https://www.huduser.gov/portal/dataset/uspszip-api.html). Then export the API as a global variable.

```
export HUD_API_TOKEN="your-token-here"
```


