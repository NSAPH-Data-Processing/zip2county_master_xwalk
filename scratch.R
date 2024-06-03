library(dplyr)

tmp <- read.csv("/Users/jck019/Desktop/nsaph/data_team/zip-fips-crosswalk/data/intermediate/zip2fips_raw_download_22014.csv")
tmp2 <- read.csv("/Users/jck019/Desktop/nsaph/data_team/zip-fips-crosswalk/data/intermediate/zip2fips_xwalk_clean.csv")


tmp3 <- tmp2 %>% filter(year == 2014)
which(is.na(tmp$COUNTY))


setwd("~/Desktop/nsaph/data_team/zip-fips-crosswalk/data/output")
# downloading xwalks for each quarter option
fname_str <- "zip2fips_master_xwalk_2010_2021_%d_tot_ratio.csv"
# selecting column names
nms <- c("zip", "fips", "total_matches")
colClasses <- c("character", "character", rep("integer", 3), rep("numeric", 3))
q1_df <- read.csv(sprintf(fname_str, 1), colClasses = colClasses) %>% 
  #select_at(nms) %>%
  mutate(quarter = 1)
q2_df <- read.csv(sprintf(fname_str, 2), colClasses = colClasses) %>% 
  #select_at(nms) %>%
  mutate(quarter = 2)
q3_df <- read.csv(sprintf(fname_str, 3), colClasses = colClasses) %>% 
  #select_at(nms) %>%
  mutate(quarter = 3)
q4_df <- read.csv(sprintf(fname_str, 4), colClasses = colClasses) %>% 
  #select_at(nms) %>%
  mutate(quarter = 4)


sum_q4 <- q4_df %>% group_by(zip) %>% summarize(total=n())
m1 <- merge(q1_df, 
            q4_df, 
            by=nms,
            all.x=T, all.y = T)

sum_m1 <- m1 %>% group_by(zip) %>% summarize(total=n())



# Master xwalk ------------------------------------------------------------

xwalk <- read.csv("~/Desktop/nsaph/data_team/zip-fips-crosswalk/data/output/zip2fips_master_xwalk_2010_2021_tot_ratio.csv")
sum_xwalk <- xwalk %>% group_by(zip) %>% summarize(total=n())

# Model xwalk -------------------------------------------------------------

model_xwalk <- 
  read.csv("~/Desktop/nsaph/data_team/zip2zcta_master_xwalk/data/output/zip2zcta_master_xwalk/zip2zcta_master_xwalk.csv") #%>%

sum_xwalk <- model_xwalk %>%
  group_by(zip) %>%
  summarize(total=n())
