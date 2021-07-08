import pandas as pd
import datetime

def join_all_dataframes(season, specify_occurrences=False):
    # Reading dataframes
    df_nba = pd.read_csv("cleaned_data/nba_cleaned_game_{}.csv".format(season), index_col=[0])
    df_cps = pd.read_csv("cleaned_data/cps_2000_2016_cleaned.csv", index_col=[0])
    df_ucr_season1 = pd.read_csv("cleaned_data/{}_cleaned.csv".format(season), index_col=[0])
    df_ucr_season2 = pd.read_csv("cleaned_data/{}_cleaned.csv".format(season-1), index_col=[0])
    df_ucr_season = pd.concat([df_ucr_season1, df_ucr_season2])

    # Filtering cps years (2015) and removing duplicates
    df_cps = df_cps[(df_cps["YEAR"] == season) | (df_cps["YEAR"] == season-1)]
    df_cps = df_cps.drop_duplicates()

    # Grouping cps
    df_cps.drop("METAREA", axis=1, inplace=True)
    cps_colnames = df_cps.loc[:, "ASECFLAG":"HHRESPLN"].columns.tolist()
    df_cps = df_cps.groupby(by=["YEAR", "METFIPS"], as_index=False,)[cps_colnames].mean()

    # Setting up nba dataframe
    month = []
    year = []
    for data in df_nba["date"]:
        month.append(datetime.datetime.strptime(data, "%Y-%m-%d").month)
        year.append(datetime.datetime.strptime(data, "%Y-%m-%d").year)
    df_nba.insert(4, "year", year)
    df_nba.insert(4, "month", month)
    df_nba.drop_duplicates(inplace=True)

    # Joining cps and NBA
    df_cps_nba = pd.merge(df_nba, df_cps, how="inner", left_on=["metfips", "year"], right_on=["METFIPS", "YEAR"])

    # Preparing crime dataframe
    crime_columns = df_ucr_season.loc[:, "OCCUR":"JN"].columns.tolist()
    df_ucr_season[crime_columns] = df_ucr_season[crime_columns].apply(pd.to_numeric,errors='coerce')
    df_ucr_season = df_ucr_season.fillna(0)

    # Grouping ucr by metfips, month, year
    arrests_columns = df_ucr_season.loc[:, "OCCUR":"JN"].columns.tolist()
    df_ucr_season = df_ucr_season.groupby(by=["metfips", "YEAR", "city_ascii"], as_index=False)["OCCUR"].sum()

    if specify_occurrences:
        grouped_ucr_age = df_ucr_season.groupby(by=["MONTH", "metfips", "YEAR", "city_ascii", "SUB"], as_index=False)[arrests_columns].sum()

        # Melting ucr to long format
        grouped_ucr_age = grouped_ucr_age.melt(id_vars=["MONTH", "metfips", "YEAR", "city_ascii", "SUB"], value_name="age_arrests", var_name="age_range")

        # Creating dataframe with total arrests
        total_arrests = grouped_ucr_age.groupby(by=["MONTH", "metfips", "YEAR", "city_ascii", "SUB"], as_index=False)["age_arrests"].sum()
        total_arrests.columns = ["MONTH", "metfips", "YEAR", "city_ascii", "SUB", "total_arrests"]

        # Merging crime dataframes
        df_ucr_season = pd.merge(grouped_ucr_age, total_arrests, how="inner", on=["MONTH", "metfips", "YEAR", "city_ascii", "SUB"])
        df_ucr_season.columns = ["month","metfips","year","city_ascii","sub","age_range","age_arrests","total_arrests"]

    # Merging all dataframes
    df_final = pd.merge(df_cps_nba, df_ucr_season, how="inner", left_on=["METFIPS", "year", "birthplace"], right_on=["metfips", "YEAR", "city_ascii"])

    return df_final

df_2009 = join_all_dataframes(2009)
df_2010 = join_all_dataframes(2010)
df_2011 = join_all_dataframes(2011)
df_2012 = join_all_dataframes(2012)
df_2013 = join_all_dataframes(2013)
df_2014 = join_all_dataframes(2014)
df_2015 = join_all_dataframes(2015)

df_2009_2015 = pd.concat([df_2009,df_2010,df_2011,df_2012,df_2013,df_2014,df_2015])
df_2009_2015.to_csv("cleaned_data/df_prepoc_2009_2015.csv")