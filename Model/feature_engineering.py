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

# Renaming columns
df.drop(["Unnamed: 0", "Unnamed: 29", "metfips_x", "metfips_y", "YEAR_x", "YEAR_y"], axis=1, inplace=True)

## creating variables from df arrest variables
df["norm_arrests"] = preprocessing.scale(df["OCCUR"])
df["mean_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("mean")
df["std_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("std")
df["max_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("max")
df["min_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("min")
df["median_arrests_year"] = df.groupby(["METFIPS", "year"]).OCCUR.transform("median")

df["rolling_avg3_arrests"] = df.groupby(["METFIPS"]).OCCUR.transform(lambda x: x.rolling(3, min_periods=2).mean())
df["rolling_avg6_arrests"] = df.groupby(["METFIPS"]).OCCUR.transform(lambda x: x.rolling(6, min_periods=2).mean())
df["rolling_avg9_arrests"] = df.groupby(["METFIPS"]).OCCUR.transform(lambda x: x.rolling(9, min_periods=2).mean())
df["rolling_std3_arrests"] = df.groupby(["METFIPS"]).OCCUR.transform(lambda x: x.rolling(3, min_periods=2).std())
df["rolling_std6_arrests"] = df.groupby(["METFIPS"]).OCCUR.transform(lambda x: x.rolling(6, min_periods=2).std())
df["rolling_std9_arrests"] = df.groupby(["METFIPS"]).OCCUR.transform(lambda x: x.rolling(9, min_periods=2).std())

## creating variables from nba variables
# points
df["norm_pts"] = preprocessing.scale(df["pts"])

df["lag_point_rolling3_avg"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
df["lag_point_rolling6_avg"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
df["lag_point_rolling9_avg"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

df["lag_point_rolling3_max"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
df["lag_point_rolling6_max"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
df["lag_point_rolling9_max"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

df["lag_point_rolling3_min"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
df["lag_point_rolling6_min"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
df["lag_point_rolling9_min"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

df["lag_point_rolling3_std"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_point_rolling6_std"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
df["lag_point_rolling9_std"] = df.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# gmsc
df["lag_gmsc_rolling3_avg"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
df["lag_gmsc_rolling6_avg"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
df["lag_gmsc_rolling9_avg"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

df["lag_gmsc_rolling3_max"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
df["lag_gmsc_rolling6_max"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
df["lag_gmsc_rolling9_max"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

df["lag_gmsc_rolling3_min"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
df["lag_gmsc_rolling6_min"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
df["lag_gmsc_rolling9_min"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

df["lag_gmsc_rolling3_std"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_gmsc_rolling6_std"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
df["lag_gmsc_rolling9_std"] = df.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# Time played
df["seconds_played"] = df.mp.apply(lambda x: min_to_sec(x))

df["lag_time_played_rolling3_avg"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
df["lag_time_played_rolling6_avg"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
df["lag_time_played_rolling9_avg"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

df["lag_time_played_rolling3_max"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
df["lag_time_played_rolling6_max"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
df["lag_time_played_rolling9_max"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

df["lag_time_played_rolling3_min"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
df["lag_time_played_rolling6_min"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
df["lag_time_played_rolling9_min"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

df["lag_time_played_rolling3_std"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_time_played_rolling6_std"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
df["lag_time_played_rolling9_std"] = df.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# age
df["age"] = df.age.apply(lambda x: int(x.split(sep="-")[0]))

## creating variables from cps variables
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

df["norm_hhtenure_lag"] = df.groupby(["METFIPS"]).norm_hhtenure.shift()
df["norm_ownershp_lag"] = df.groupby(["METFIPS"]).norm_ownershp.shift()
df["norm_hhincome_lag"] = df.groupby(["METFIPS"]).norm_hhincome.shift()
df["norm_pubhous_lag"] = df.groupby(["METFIPS"]).norm_pubhous.shift()
df["norm_rentsub_lag"] = df.groupby(["METFIPS"]).norm_rentsub.shift()
df["norm_foodstmp_lag"] = df.groupby(["METFIPS"]).norm_foodstmp.shift()
df["norm_atelunch_lag"] = df.groupby(["METFIPS"]).norm_atelunch.shift()
df["norm_lunchsub_lag"] = df.groupby(["METFIPS"]).norm_lunchsub.shift()
df["norm_frelunch_lag"] = df.groupby(["METFIPS"]).norm_frelunch.shift()
df["norm_stampval_lag"] = df.groupby(["METFIPS"]).norm_stampval.shift()
df["norm_faminc_lag"] = df.groupby(["METFIPS"]).norm_faminc.shift()
df["norm_nfams_lag"] = df.groupby(["METFIPS"]).norm_nfams.shift()
df["norm_ncouples_lag"] = df.groupby(["METFIPS"]).norm_ncouples.shift()
df["norm_nmothers_lag"] = df.groupby(["METFIPS"]).norm_nmothers.shift()
df["norm_nfathers_lag"] = df.groupby(["METFIPS"]).norm_nfathers.shift()

df["lag_hhtenure_rolling3_std"] = df.groupby(["METFIPS"]).norm_hhtenure_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_ownershp_rolling3_std"] = df.groupby(["METFIPS"]).norm_ownershp_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_hhincome_rolling3_std"] = df.groupby(["METFIPS"]).norm_hhincome_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_pubhous_rolling3_std"] = df.groupby(["METFIPS"]).norm_pubhous_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_rentsub_rolling3_std"] = df.groupby(["METFIPS"]).norm_rentsub_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_foodstmp_rolling3_std"] = df.groupby(["METFIPS"]).norm_foodstmp_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_atelunch_rolling3_std"] = df.groupby(["METFIPS"]).norm_atelunch_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_lunchsub_rolling3_std"] = df.groupby(["METFIPS"]).norm_lunchsub_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_frelunch_rolling3_std"] = df.groupby(["METFIPS"]).norm_frelunch_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_stampval_rolling3_std"] = df.groupby(["METFIPS"]).norm_stampval_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_faminc_rolling3_std"] = df.groupby(["METFIPS"]).norm_faminc_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_nfams_rolling3_std"] = df.groupby(["METFIPS"]).norm_nfams_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_ncouples_rolling3_std"] = df.groupby(["METFIPS"]).norm_ncouples_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_nmothers_rolling3_std"] = df.groupby(["METFIPS"]).norm_nmothers_lag.transform(lambda x: x.rolling(3, min_periods=2).std())
df["lag_nfathers_rolling3_std"] = df.groupby(["METFIPS"]).norm_nfathers_lag.transform(lambda x: x.rolling(3, min_periods=2).std())

id_df = pd.DataFrame([(x, y) for x in list(set(df.year)) for y in list(set(df.g))],
                     columns = ["year", "g"])
id_df["game_id"] = np.array(range(len(id_df))) + 1

df = df.merge(id_df, how = "inner", on = ["year", "g"])

df.to_csv("pre_model_data/df_2009_2015_feat_engineered5.csv")