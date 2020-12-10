import pandas as pd
import numpy as np
import os
from sklearn import preprocessing
import tkinter as tk
from tkinter import filedialog
from siuba import *
from datetime import datetime

##### Functions

# Setting up paths
cwd = os.getcwd()
project_wd = os.path.dirname(cwd)
clean_wd = os.path.join(project_wd, "Clean_Data")

# Function that identifies the database's filepath
# def get_datapath(message):
#     root = tk.Tk()
#     root.withdraw()
#     return filedialog.askopenfilename(title=message)

# Function that turns a string of minutes into seconds
def min_to_sec(string):
    ls = string.split(sep=":")
    min = int(ls[0])
    sec = int(ls[1])
    return min * 60 + sec

# Importing dataframe
df = pd.read_csv("{}/cleaned_data/df_prepoc_2009_2015.csv".format(clean_wd))

df_antes = df

# Renaming columns
df.drop(["Unnamed: 0", "Unnamed: 29", "metfips_x", "metfips_y", "YEAR_x", "YEAR_y"], axis=1, inplace=True)

# Creating and shifting variables

# Arrests
df["norm_arrests"] = preprocessing.scale(df["OCCUR"])
df["mean_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("mean")
df["std_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("std")
df["max_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("max")
df["min_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("min")
df["median_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("median")

df["lag_arrests"] = df.groupby(["METFIPS"]).norm_arrests.shift()
df["lag_mean_arrests_year"] = df.groupby(["METFIPS"]).mean_arrests_year.shift()
df["lag_std_arrests_year"] = df.groupby(["METFIPS"]).std_arrests_year.shift()
df["lag_max_arrests_year"] = df.groupby(["METFIPS"]).max_arrests_year.shift()
df["lag_min_arrests_year"] = df.groupby(["METFIPS"]).min_arrests_year.shift()
df["lag_median_arrests_year"] = df.groupby(["METFIPS"]).median_arrests_year.shift()

df["lag_rolling_avg3_arrests"] = df.groupby(["METFIPS"]).lag_arrests.transform(lambda x: x.rolling(3, min_periods=2).mean())
df["lag_rolling_avg6_arrests"] = df.groupby(["METFIPS"]).lag_arrests.transform(lambda x: x.rolling(6, min_periods=2).mean())
df["lag_rolling_avg9_arrests"] = df.groupby(["METFIPS"]).lag_arrests.transform(lambda x: x.rolling(9, min_periods=2).mean())
df["lag_rolling_std3_arrests"] = df.groupby(["METFIPS"]).lag_arrests.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_rolling_std6_arrests"] = df.groupby(["METFIPS"]).lag_arrests.transform(lambda x: x.rolling(6, min_periods=2).std())
df["lag_rolling_std9_arrests"] = df.groupby(["METFIPS"]).lag_arrests.transform(lambda x: x.rolling(9, min_periods=2).std())

# NBA
df["norm_pts"] = preprocessing.scale(df["pts"])
df["time_played"] = df.mp.apply(lambda x: min_to_sec(x))
df["norm_time_played"] = df.mp.apply(lambda x: min_to_sec(x))
df["age"] = df.age.apply(lambda x: int(x.split(sep="-")[0]))
df["norm_age"] = preprocessing.scale(df["age"])
df["norm_gmsc"] = preprocessing.scale(df["gmsc"])

# Pts
df["lag_pts"] = df.groupby(["id"]).norm_pts.shift()

df["lag_point_rolling3_avg"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
df["lag_point_rolling6_avg"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
df["lag_point_rolling9_avg"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

df["lag_point_rolling3_max"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
df["lag_point_rolling6_max"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
df["lag_point_rolling9_max"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

df["lag_point_rolling3_min"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
df["lag_point_rolling6_min"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
df["lag_point_rolling9_min"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

df["lag_point_rolling3_std"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_point_rolling6_std"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
df["lag_point_rolling9_std"] = df.groupby(["id"]).norm_pts.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# Gmsc
df["lag_gmsc"] = df.groupby(["id"]).norm_gmsc.shift()

df["lag_gmsc_rolling3_avg"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
df["lag_gmsc_rolling6_avg"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
df["lag_gmsc_rolling9_avg"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

df["lag_gmsc_rolling3_max"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
df["lag_gmsc_rolling6_max"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
df["lag_gmsc_rolling9_max"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

df["lag_gmsc_rolling3_min"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
df["lag_gmsc_rolling6_min"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
df["lag_gmsc_rolling9_min"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

df["lag_gmsc_rolling3_std"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_gmsc_rolling6_std"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
df["lag_gmsc_rolling9_std"] = df.groupby(["id"]).norm_gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# Time played
df["lag_time_played"] = df.groupby(["id"]).time_played.shift()

df["lag_time_played_rolling3_avg"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
df["lag_time_played_rolling6_avg"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
df["lag_time_played_rolling9_avg"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

df["lag_time_played_rolling3_max"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
df["lag_time_played_rolling6_max"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
df["lag_time_played_rolling9_max"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

df["lag_time_played_rolling3_min"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
df["lag_time_played_rolling6_min"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
df["lag_time_played_rolling9_min"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

df["lag_time_played_rolling3_std"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_time_played_rolling6_std"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
df["lag_time_played_rolling9_std"] = df.groupby(["id"]).norm_time_played.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# age
df["lag_age"] = df.groupby(["id"]).norm_age.shift()

# CPS
df["norm_hhtenure"] = preprocessing.scale(df["HHTENURE"])
df["norm_ownershp"] = preprocessing.scale(df["OWNERSHP"])
df["norm_hhincome"] = preprocessing.scale(df["HHINCOME"])
df["norm_pubhous"] = preprocessing.scale(df["PUBHOUS"])
df["norm_rentsub"] = preprocessing.scale(df["RENTSUB"])
df["norm_foodstmp"] = preprocessing.scale(df["FOODSTMP"])
df["norm_atelunch"] = preprocessing.scale(df["ATELUNCH"])
df["norm_lunchsub"] = preprocessing.scale(df["LUNCHSUB"])
df["norm_frelunch"] = preprocessing.scale(df["FRELUNCH"])
df["norm_stampval"] = preprocessing.scale(df["STAMPVAL"])
df["norm_faminc"] = preprocessing.scale(df["FAMINC"])
df["norm_nfams"] = preprocessing.scale(df["NFAMS"])
df["norm_ncouples"] = preprocessing.scale(df["NCOUPLES"])
df["norm_nmothers"] = preprocessing.scale(df["NMOTHERS"])
df["norm_nfathers"] = preprocessing.scale(df["NFATHERS"])

df["lag_norm_hhtenure"] = df.groupby(["METFIPS"]).norm_hhtenure.shift()
df["lag_norm_ownershp"] = df.groupby(["METFIPS"]).norm_ownershp.shift()
df["lag_norm_hhincome"] = df.groupby(["METFIPS"]).norm_hhincome.shift()
df["lag_norm_pubhous"] = df.groupby(["METFIPS"]).norm_pubhous.shift()
df["lag_norm_rentsub"] = df.groupby(["METFIPS"]).norm_rentsub.shift()
df["lag_norm_foodstmp"] = df.groupby(["METFIPS"]).norm_foodstmp.shift()
df["lag_norm_atelunch"] = df.groupby(["METFIPS"]).norm_atelunch.shift()
df["lag_norm_lunchsub"] = df.groupby(["METFIPS"]).norm_lunchsub.shift()
df["lag_norm_frelunch"] = df.groupby(["METFIPS"]).norm_frelunch.shift()
df["lag_norm_stampval"] = df.groupby(["METFIPS"]).norm_stampval.shift()
df["lag_norm_faminc"] = df.groupby(["METFIPS"]).norm_faminc.shift()
df["lag_norm_nfams"] = df.groupby(["METFIPS"]).norm_nfams.shift()
df["lag_norm_ncouples"] = df.groupby(["METFIPS"]).norm_ncouples.shift()
df["lag_norm_nmothers"] = df.groupby(["METFIPS"]).norm_nmothers.shift()
df["lag_norm_nfathers"] = df.groupby(["METFIPS"]).norm_nfathers.shift()

df["lag_hhtenure_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_hhtenure.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_ownershp_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_ownershp.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_hhincome_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_hhincome.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_pubhous_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_pubhous.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_rentsub_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_rentsub.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_foodstmp_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_foodstmp.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_atelunch_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_atelunch.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_lunchsub_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_lunchsub.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_frelunch_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_frelunch.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_stampval_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_stampval.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_faminc_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_faminc.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_nfams_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_nfams.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_ncouples_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_ncouples.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_nmothers_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_nmothers.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_nfathers_rolling3_std"] = df.groupby(["METFIPS"]).lag_norm_nfathers.transform(lambda x: x.rolling(3, min_periods=2).std())

id_df = pd.DataFrame([(x, y) for x in list(set(df.year)) for y in list(set(df.g))], columns = ["year", "g"])
id_df["game_id"] = np.array(range(len(id_df))) + 1

df = df.merge(id_df, how = "inner", on = ["year", "g"])

df.to_csv("pre_model_data/df_2009_2015_feat_engineered5.csv")

#### CÓDIGO PARA CRIAR DADOS DOS TIMES A SEREM UTILIZADOS ####

# teams = ((df >>
#   select(_["g", "year", "tm", "fg":"pts"]))
#    .filter(regex="[^%]$")
#    .groupby(["g", "year", "tm"])
#    .agg("sum")
#    .reset_index()
#    .add_prefix("opp_")
#    .rename(columns={"opp_year": "year",
#                     "opp_tm": "opp",
#                     "opp_g": "g"}))

# df.merge(teams, how="inner", on=["opp", "g", "year"])
# df.merge(teams, how="inner", on=["tm", "g", "year"])

df.to_csv("pre_model_data/df_2009_2015_feat_engineered8.csv")
