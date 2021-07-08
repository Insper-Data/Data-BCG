import pandas as pd
import datetime
from siuba import *

df = pd.DataFrame()

for year in range(2009, 2016):
    df_i = pd.read_csv("raw_data/df_nba_{}.csv".format(year))
    df_i.drop(["Unnamed: 0", "Unnamed: 29"], axis=1, inplace=True)
    df = pd.concat([df, df_i])

# Setting up nba dataframe
month = []
year = []

for data in df["date"]:
    month.append(datetime.datetime.strptime(data, "%Y-%m-%d").month)
    year.append(datetime.datetime.strptime(data, "%Y-%m-%d").year)

df.insert(4, "year", year)
df.insert(4, "month", month)
df.drop_duplicates(inplace=True)

df.to_csv("cleaned_data/all_games_2009_2015.csv")