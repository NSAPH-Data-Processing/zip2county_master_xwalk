FROM condaforge/mambaforge:23.3.1-1

# install build essentials
RUN apt-get update && apt-get install -y build-essential

# set working directory
WORKDIR /app

# Clone your repository
RUN git clone https://github.com/NSAPH-Data-Processing/zip2county_master_xwalk/ .

# Update the base environment
RUN mamba env update -n base -f requirements.yaml 

# snakemake --configfile config.yaml --cores 1
ENTRYPOINT ["snakemake", "--configfile", "config.yaml", "--cores", "1"]
CMD ["-C", "min_year=2010", "max_year=2023", "criteria=tot_ratio", "xwalk_method=one2one"]