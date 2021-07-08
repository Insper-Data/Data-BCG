import pandas as pd
from Data_BCG.Download_Data import scraping_Functions as sf

# performance = sf.get_aggregated_season_data(1980)
per_game_data = sf.get_game_data(2009)
birthplaces = sf.get_birthplaces()
high_schools = sf.get_high_school_cities()
player_id = sf.get_players_id()

# Standarizing each database

# I removed the * at the end of the name of the players from every player

# performance.player = performance.player.str.replace("\*", "")

player_id = player_id.rename(str.lower, axis="columns")
per_game_data = pd.merge(per_game_data, player_id, how="left", on="id")
names = per_game_data["player"]
per_game_data.drop("player", axis=1, inplace=True)
per_game_data.insert(0, "player", names)

# Eliminated columns that weren't useful to the final database
high_schools = high_schools.iloc[:, [0, 1, 2]].rename(str.lower, axis="columns")
high_schools.player = high_schools.player.str.replace("\*", "")

# Restricted the sample to players that were born in the US
# Eliminated columns that weren't useful to the final database
birthplaces.player = birthplaces.player.str.replace("\*", "")
birthplaces = birthplaces[birthplaces.country_iso2 == "US"]
birthplaces = birthplaces.iloc[:, [0, 1, 3]]

# Merged the databases into one, restricting the data with "inner"
# performance_aggr = pd.merge(performance, birthplaces, how="inner", on="player")
# performance_aggr = pd.merge(performance_aggr, high_schools, how="inner", on=["player", "state"])

per_game_aggr = pd.merge(per_game_data, birthplaces, how="inner", on="player")
per_game_aggr = pd.merge(per_game_aggr, high_schools, how="inner", on=["player", "state"])

# Merging metropolitan area data
df_fips = pd.read_csv("{}/Data/fips_data.csv".format(download_wd))

# df_final_season = pd.merge(performance_aggr, df_fips, how="left", left_on=["state", "birthplace"], right_on=["state_id", "city_ascii"])
# df_final_season.drop(["state_id", "city_ascii"], inplace=True, axis=1)
# df_final_season.sort_values(["metfips"], inplace=True)

df_final_game = pd.merge(per_game_aggr, df_fips, how="left", left_on=["state", "birthplace"], right_on=["state_id", "city_ascii"])
df_final_game.drop(["state_id", "city_ascii"], inplace=True, axis=1)
df_final_game.sort_values(["metfips"], inplace=True)

# Checking Na percentage
# percent_missing = df_final_season.isnull().sum() * 100 / len(df_final_season)
# missing_value_df = pd.DataFrame({"column_name": df_final_season.columns, "percent_missing": percent_missing})

# Checking cities/county's with problems
# df_nas_metfips = df_final_season[df_final_season["metfips"].isna()]
# df_nas_countyfips = df_final_season[df_final_season["county_fips"].isna()]
# df_nas = df_nas_countyfips.append(df_nas_metfips)
# df_nas = df_nas["birthplace"].unique()

# Saving dataframe
# df_final_season.to_csv("cleaned_data/nba_cleaned_season.csv")
df_final_game.to_csv("cleaned_data/nba_cleaned_game_2009.csv")

# Created a database with less columns for a less noisy visualization
# performance_aggr_gmsc = performance_aggr[["year", "player", "gmsc", "birthplace", "state", "hs_city"]]
