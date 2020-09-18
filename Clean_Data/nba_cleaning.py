import pandas as pd

# Pulling the data from a .csv file
performance = pd.read_csv("C:/Users/USER/Downloads/performance_nba.csv")
birthplaces = pd.read_csv("C:/Users/USER/Downloads/nba_birthplaces.csv")
high_schools = pd.read_csv("C:/Users/USER/Downloads/high_schools.csv")

# Standardizing each database

# I removed the * at the end of the name of the players from every player
# Reduced the sample to data from 1980 on

performance.player = performance.player.str.replace("\*", "")
performance = performance[performance.year >= 1980]

# Eliminated columns that weren't useful to the final database
high_schools = high_schools.iloc[:, [1, 2]].rename(str.lower, axis = "columns")
high_schools.player = high_schools.player.str.replace("\*", "")

# Restricted the sample to players that were born in the US
# Eliminated columns that weren't useful to the final database
birthplaces.name = birthplaces.name.str.replace("\*", "")
birthplaces = birthplaces[birthplaces.country_iso2 == "US"]
birthplaces = birthplaces.iloc[:, [0, 2, 3]]

# Merged the databases into one, restricting the data with "inner"
performance_aggr = pd.merge(performance, birthplaces, how="inner", left_on="player", right_on="name")
performance_aggr = pd.merge(performance_aggr, high_schools, how="inner", on="player")

# Created a database with less columns for a less noisy visualization
performance_aggr_gmsc = performance_aggr[["year", "player", "gmsc", "city", "state", "hs_city"]]

# Transformed both databases into .csv files
performance_aggr_gmsc.to_csv("C:/Users/USER/Downloads/performance_gmsc.csv")
performance_aggr.to_csv("C:/Users/USER/Downloads/performance_complete.csv")