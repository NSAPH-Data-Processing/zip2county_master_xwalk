FROM condaforge/mambaforge:23.3.1-1

# install build essentials
RUN apt-get update && apt-get install -y build-essential

# this seems not correct
WORKDIR /app

# Clone your repository
RUN git clone --branch jckitch/issue13 https://github.com/NSAPH-Data-Processing/zip_fips_master_xwalk/ .

# Update the base environment
RUN mamba env update -n base -f requirements.yaml 

# snakemake --configfile conf/config.yaml --cores 4 -C temporal_freq=annual
ENTRYPOINT ["snakemake", "--configfile", "config.yaml", "--cores", "4"]
CMD ["-C", "min_year=2010", "max_year=2023", "quarter=4", "criteria=tot_ratio", "xwalk_method=one2one"]