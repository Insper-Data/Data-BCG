import pandas as pd
from Data_BCG.Download_Data import scraping_Functions as sf

df = sf.get_game_data(2015)

player_id = sf.get_players_id()
player_id = player_id.rename(str.lower, axis="columns")
df = pd.merge(df, player_id, how="left", on="id")
names = df["player"]
df.drop("player", axis=1, inplace=True)
df.insert(0, "player", names)

df.to_csv("raw_data/df_nba_2015.csv")
