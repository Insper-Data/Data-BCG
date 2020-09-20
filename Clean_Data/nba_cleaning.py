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

# Created a database with less columns for a less noisy visualization
performance_aggr_gmsc = performance_aggr[["year", "player", "gmsc", "birthplace", "state", "hs_city"]]
