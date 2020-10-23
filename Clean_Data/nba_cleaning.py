import pandas as pd
import os
import sys

cwd = os.getcwd()
project_wd = os.path.dirname(cwd)
download_wd = os.path.join(project_wd, "Download_Data")
sys.path.insert(1, download_wd)

import scraping_Functions as sf

# Pulling the data scraping functions

performance = sf.get_aggregated_season_data(1980)
birthplaces = sf.get_birthplaces()
high_schools = sf.get_high_school_cities()

# Standardizing each database

# I removed the * at the end of the name of the players from every player

performance.player = performance.player.str.replace("\*", "")

# Eliminated columns that weren't useful to the final database
high_schools = high_schools.iloc[:, [0, 1, 2]].rename(str.lower, axis = "columns")
high_schools.player = high_schools.player.str.replace("\*", "")

# Restricted the sample to players that were born in the US
# Eliminated columns that weren't useful to the final database
birthplaces.player = birthplaces.player.str.replace("\*", "")
birthplaces = birthplaces[birthplaces.country_iso2 == "US"]
birthplaces = birthplaces.iloc[:, [0, 1, 3]]

# Merged the databases into one, restricting the data with "inner"
performance_aggr = pd.merge(performance, birthplaces, how="inner", on="player")
performance_aggr = pd.merge(performance_aggr, high_schools, how="inner", on=["player", "state"])

# Merging metropolitan area data
df_fips = pd.read_csv("{}/Data/fips_data.csv".format(download_wd))
df_final = pd.merge(performance_aggr, df_fips, how="left", left_on=["state", "birthplace"], right_on=["state_id", "city_ascii"])
df_final.drop(["state_id", "city_ascii"], inplace=True, axis=1)
df_final.sort_values(["metfips"], inplace=True)

# Checking Na percentage
percent_missing = df_final.isnull().sum() * 100 / len(df_final)
missing_value_df = pd.DataFrame({"column_name": df_final.columns, "percent_missing": percent_missing})

# Checking cities/county's with problems
df_nas_metfips = df_final[df_final["metfips"].isna()]
df_nas_countyfips = df_final[df_final["county_fips"].isna()]
df_nas = df_nas_countyfips.append(df_nas_metfips)
df_nas = df_nas["birthplace"].unique()

# Saving dataframe
df_final.to_csv("cleaned_data/nba_cleaned")

# Created a database with less columns for a less noisy visualization
performance_aggr_gmsc = performance_aggr[["year", "player", "gmsc", "birthplace", "state", "hs_city"]]
