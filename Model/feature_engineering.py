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
df["norm_hhincome"] = preprocessing.scale(df["HHINCOME"])
df["norm_atelunch"] = preprocessing.scale(df["ATELUNCH"])
df["norm_frelunch"] = preprocessing.scale(df["FRELUNCH"])
df["norm_stampval"] = preprocessing.scale(df["STAMPVAL"])
df["norm_faminc"] = preprocessing.scale(df["FAMINC"])


df["mean_hhtenure_year"] = df.groupby(["METFIPS", "year"]).HHTENURE.transform("mean")
df["std_hhtenure_year"] = df.groupby(["METFIPS", "year"]).HHTENURE.transform("std")
df["max_hhtenure_year"] = df.groupby(["METFIPS", "year"]).HHTENURE.transform("max")
df["min_hhtenure_year"] = df.groupby(["METFIPS", "year"]).HHTENURE.transform("min")
df["median_hhtenure_year"] = df.groupby(["METFIPS", "year"]).HHTENURE.transform("median")

df["mean_ownershp_year"] = df.groupby(["METFIPS", "year"]).OWNERSHP.transform("mean")
df["std_ownershp_year"] = df.groupby(["METFIPS", "year"]).OWNERSHP.transform("std")
df["max_ownershp_year"] = df.groupby(["METFIPS", "year"]).OWNERSHP.transform("max")
df["min_ownershp_year"] = df.groupby(["METFIPS", "year"]).OWNERSHP.transform("min")
df["median_ownershp_year"] = df.groupby(["METFIPS", "year"]).OWNERSHP.transform("median")

df["mean_hhincome_year"] = df.groupby(["METFIPS", "year"]).HHINCOME.transform("mean")
df["std_hhincome_year"] = df.groupby(["METFIPS", "year"]).HHINCOME.transform("std")
df["max_hhincome_year"] = df.groupby(["METFIPS", "year"]).HHINCOME.transform("max")
df["min_hhincome_year"] = df.groupby(["METFIPS", "year"]).HHINCOME.transform("min")
df["median_hhincome_year"] = df.groupby(["METFIPS", "year"]).HHINCOME.transform("median")

df["rolling_avg3_hhincome"] = df.groupby(["METFIPS"]).HHINCOME.transform(lambda x: x.rolling(3, min_periods=2).mean())
df["rolling_avg6_hhincome"] = df.groupby(["METFIPS"]).HHINCOME.transform(lambda x: x.rolling(6, min_periods=2).mean())
df["rolling_avg9_hhincome"] = df.groupby(["METFIPS"]).HHINCOME.transform(lambda x: x.rolling(9, min_periods=2).mean())
df["rolling_std3_hhincome"] = df.groupby(["METFIPS"]).HHINCOME.transform(lambda x: x.rolling(3, min_periods=2).std())
df["rolling_std6_hhincome"] = df.groupby(["METFIPS"]).HHINCOME.transform(lambda x: x.rolling(6, min_periods=2).std())
df["rolling_std9_hhincome"] = df.groupby(["METFIPS"]).HHINCOME.transform(lambda x: x.rolling(9, min_periods=2).std())

df["mean_pubhous_year"] = df.groupby(["METFIPS", "year"]).PUBHOUS.transform("mean")
df["std_pubhous_year"] = df.groupby(["METFIPS", "year"]).PUBHOUS.transform("std")
df["max_pubhous_year"] = df.groupby(["METFIPS", "year"]).PUBHOUS.transform("max")
df["min_pubhous_year"] = df.groupby(["METFIPS", "year"]).PUBHOUS.transform("min")
df["median_pubhous_year"] = df.groupby(["METFIPS", "year"]).PUBHOUS.transform("median")

df["mean_rentsub_year"] = df.groupby(["METFIPS", "year"]).RENTSUB.transform("mean")
df["std_rentsub_year"] = df.groupby(["METFIPS", "year"]).RENTSUB.transform("std")
df["max_rentsub_year"] = df.groupby(["METFIPS", "year"]).RENTSUB.transform("max")
df["min_rentsub_year"] = df.groupby(["METFIPS", "year"]).RENTSUB.transform("min")
df["median_rentsub_year"] = df.groupby(["METFIPS", "year"]).RENTSUB.transform("median")

df["mean_foodstmp_year"] = df.groupby(["METFIPS", "year"]).FOODSTMP.transform("mean")
df["std_foodstmp_year"] = df.groupby(["METFIPS", "year"]).FOODSTMP.transform("std")
df["max_foodstmp_year"] = df.groupby(["METFIPS", "year"]).FOODSTMP.transform("max")
df["min_foodstmp_year"] = df.groupby(["METFIPS", "year"]).FOODSTMP.transform("min")
df["median_foodstmp_year"] = df.groupby(["METFIPS", "year"]).FOODSTMP.transform("median")

df["rolling_avg3_foodstmp"] = df.groupby(["FOODSTMP"]).HHINCOME.transform(lambda x: x.rolling(3, min_periods=2).mean())
df["rolling_avg6_foodstmp"] = df.groupby(["FOODSTMP"]).HHINCOME.transform(lambda x: x.rolling(6, min_periods=2).mean())
df["rolling_avg9_foodstmp"] = df.groupby(["FOODSTMP"]).HHINCOME.transform(lambda x: x.rolling(9, min_periods=2).mean())
df["rolling_std3_foodstmp"] = df.groupby(["FOODSTMP"]).HHINCOME.transform(lambda x: x.rolling(3, min_periods=2).std())
df["rolling_std6_foodstmp"] = df.groupby(["FOODSTMP"]).HHINCOME.transform(lambda x: x.rolling(6, min_periods=2).std())
df["rolling_std9_foodstmp"] = df.groupby(["FOODSTMP"]).HHINCOME.transform(lambda x: x.rolling(9, min_periods=2).std())

df["mean_atelunch_year"] = df.groupby(["METFIPS", "year"]).ATELUNCH.transform("mean")
df["std_atelunch_year"] = df.groupby(["METFIPS", "year"]).ATELUNCH.transform("std")
df["max_atelunch_year"] = df.groupby(["METFIPS", "year"]).ATELUNCH.transform("max")
df["min_atelunch_year"] = df.groupby(["METFIPS", "year"]).ATELUNCH.transform("min")
df["median_atelunch_year"] = df.groupby(["METFIPS", "year"]).ATELUNCH.transform("median")

df["mean_lunchsub_year"] = df.groupby(["METFIPS", "year"]).LUNCHSUB.transform("mean")
df["std_lunchsub_year"] = df.groupby(["METFIPS", "year"]).LUNCHSUB.transform("std")
df["max_lunchsub_year"] = df.groupby(["METFIPS", "year"]).LUNCHSUB.transform("max")
df["min_lunchsub_year"] = df.groupby(["METFIPS", "year"]).LUNCHSUB.transform("min")
df["median_lunchsub_year"] = df.groupby(["METFIPS", "year"]).LUNCHSUB.transform("median")

df["mean_frelunch"] = df.groupby(["METFIPS", "year"]).FRELUNCH.transform("mean")
df["std_frelunch_year"] = df.groupby(["METFIPS", "year"]).FRELUNCH.transform("std")
df["max_frelunch_year"] = df.groupby(["METFIPS", "year"]).FRELUNCH.transform("max")
df["min_frelunch_year"] = df.groupby(["METFIPS", "year"]).FRELUNCH.transform("min")
df["median_frelunch_year"] = df.groupby(["METFIPS", "year"]).FRELUNCH.transform("median")

df["mean_stampval"] = df.groupby(["METFIPS", "year"]).STAMPVAL.transform("mean")
df["std_stampval_year"] = df.groupby(["METFIPS", "year"]).STAMPVAL.transform("std")
df["max_stampval_year"] = df.groupby(["METFIPS", "year"]).STAMPVAL.transform("max")
df["min_stampval_year"] = df.groupby(["METFIPS", "year"]).STAMPVAL.transform("min")
df["median_stampval_year"] = df.groupby(["METFIPS", "year"]).STAMPVAL.transform("median")

df["rolling_avg3_stampval"] = df.groupby(["STAMPVAL"]).HHINCOME.transform(lambda x: x.rolling(3, min_periods=2).mean())
df["rolling_avg6_stampval"] = df.groupby(["STAMPVAL"]).HHINCOME.transform(lambda x: x.rolling(6, min_periods=2).mean())
df["rolling_avg9_stampval"] = df.groupby(["STAMPVAL"]).HHINCOME.transform(lambda x: x.rolling(9, min_periods=2).mean())
df["rolling_std3_stampval"] = df.groupby(["STAMPVAL"]).HHINCOME.transform(lambda x: x.rolling(3, min_periods=2).std())
df["rolling_std6_stampval"] = df.groupby(["STAMPVAL"]).HHINCOME.transform(lambda x: x.rolling(6, min_periods=2).std())
df["rolling_std9_stampval"] = df.groupby(["STAMPVAL"]).HHINCOME.transform(lambda x: x.rolling(9, min_periods=2).std())

df["mean_faminc"] = df.groupby(["METFIPS", "year"]).FAMINC.transform("mean")
df["std_faminc_year"] = df.groupby(["METFIPS", "year"]).FAMINC.transform("std")
df["max_faminc_year"] = df.groupby(["METFIPS", "year"]).FAMINC.transform("max")
df["min_faminc_year"] = df.groupby(["METFIPS", "year"]).FAMINC.transform("min")
df["median_faminc_year"] = df.groupby(["METFIPS", "year"]).FAMINC.transform("median")

df["rolling_avg3_faminc"] = df.groupby(["METFIPS"]).FAMINC.transform(lambda x: x.rolling(3, min_periods=2).mean())
df["rolling_avg6_faminc"] = df.groupby(["METFIPS"]).FAMINC.transform(lambda x: x.rolling(6, min_periods=2).mean())
df["rolling_avg9_faminc"] = df.groupby(["METFIPS"]).FAMINC.transform(lambda x: x.rolling(9, min_periods=2).mean())
df["rolling_std3_faminc"] = df.groupby(["METFIPS"]).FAMINC.transform(lambda x: x.rolling(3, min_periods=2).std())
df["rolling_std6_faminc"] = df.groupby(["METFIPS"]).FAMINC.transform(lambda x: x.rolling(6, min_periods=2).std())
df["rolling_std9_faminc"] = df.groupby(["METFIPS"]).FAMINC.transform(lambda x: x.rolling(9, min_periods=2).std())

df["mean_nfams"] = df.groupby(["METFIPS", "year"]).NFAMS.transform("mean")
df["std_nfams_year"] = df.groupby(["METFIPS", "year"]).NFAMS.transform("std")
df["max_nfams_year"] = df.groupby(["METFIPS", "year"]).NFAMS.transform("max")
df["min_nfams_year"] = df.groupby(["METFIPS", "year"]).NFAMS.transform("min")
df["median_nfams_year"] = df.groupby(["METFIPS", "year"]).NFAMS.transform("median")

df["mean_ncouples"] = df.groupby(["METFIPS", "year"]).NCOUPLES.transform("mean")
df["std_ncouples_year"] = df.groupby(["METFIPS", "year"]).NCOUPLES.transform("std")
df["max_ncouples_year"] = df.groupby(["METFIPS", "year"]).NCOUPLES.transform("max")
df["min_ncouples_year"] = df.groupby(["METFIPS", "year"]).NCOUPLES.transform("min")
df["median_ncouples_year"] = df.groupby(["METFIPS", "year"]).NCOUPLES.transform("median")

df["mean_nmothers"] = df.groupby(["METFIPS", "year"]).NMOTHERS.transform("mean")
df["std_nmothers_year"] = df.groupby(["METFIPS", "year"]).NMOTHERS.transform("std")
df["max_nmothers_year"] = df.groupby(["METFIPS", "year"]).NMOTHERS.transform("max")
df["min_nmothers_year"] = df.groupby(["METFIPS", "year"]).NMOTHERS.transform("min")
df["median_nmothers_year"] = df.groupby(["METFIPS", "year"]).NMOTHERS.transform("median")

df["mean_nfathers"] = df.groupby(["METFIPS", "year"]).NFATHERS.transform("mean")
df["std_nfathers_year"] = df.groupby(["METFIPS", "year"]).NFATHERS.transform("std")
df["max_nfathers_year"] = df.groupby(["METFIPS", "year"]).NFATHERS.transform("max")
df["min_nfathers_year"] = df.groupby(["METFIPS", "year"]).NFATHERS.transform("min")
df["median_nfathers_year"] = df.groupby(["METFIPS", "year"]).NFATHERS.transform("median")

id_df = pd.DataFrame([(x, y) for x in list(set(df.YEAR)) for y in list(set(df.g))],
                     columns = ["YEAR", "g"])
id_df["game_id"] = np.array(range(len(id_df))) + 1

df = df.merge(id_df, how = "inner", on = ["YEAR", "g"])

df.to_csv("pre_model_data/df_2009_2015_feat_engineered.csv")