import pandas as pd
import numpy as np
import os
from sklearn import preprocessing
import tkinter as tk
from tkinter import filedialog
from siuba import *
from datetime import datetime

##### Functions

# Function that identifies the database's filepath
def get_datapath(message):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=message)

# Function that turns a string of minutes into seconds
def min_to_sec(string):
    ls = string.split(sep=":")
    min = int(ls[0])
    sec = int(ls[1])
    return min * 60 + sec

## adding variables to ucr arrest database

ucr = pd.read_csv(get_datapath("Selecione a base da UCR")).dropna()
ucr["norm_arrests"] = preprocessing.scale(ucr["arrests"])
ucr["mean_arrests_year"] = ucr.groupby(["metfips", "YEAR"]).arrests.transform("mean")
ucr["std_arrests_year"] = ucr.groupby(["metfips", "YEAR"]).arrests.transform("std")
ucr["max_arrests_year"] = ucr.groupby(["metfips", "YEAR"]).arrests.transform("max")
ucr["min_arrests_year"] = ucr.groupby(["metfips", "YEAR"]).arrests.transform("min")
ucr["median_arrests_year"] = ucr.groupby(["metfips", "YEAR"]).arrests.transform("median")
ucr["rolling_avg3_arrests"] = ucr.groupby(["metfips"]).arrests.transform(lambda x: x.rolling(3, min_periods=2).mean())
ucr["rolling_avg6_arrests"] = ucr.groupby(["metfips"]).arrests.transform(lambda x: x.rolling(6, min_periods=2).mean())
ucr["rolling_avg9_arrests"] = ucr.groupby(["metfips"]).arrests.transform(lambda x: x.rolling(9, min_periods=2).mean())
ucr["rolling_std3_arrests"] = ucr.groupby(["metfips"]).arrests.transform(lambda x: x.rolling(3, min_periods=2).std())
ucr["rolling_std6_arrests"] = ucr.groupby(["metfips"]).arrests.transform(lambda x: x.rolling(6, min_periods=2).std())
ucr["rolling_std9_arrests"] = ucr.groupby(["metfips"]).arrests.transform(lambda x: x.rolling(9, min_periods=2).std())

## adding variables to nba database

nba = pd.read_csv(get_datapath("Selecione a base da NBA")).iloc[:, 1:]
nba = nba.drop(["metarea"], axis=1)
nba = nba.dropna(subset=["metfips"])
nba["MONTH"] = nba.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d").month)
nba["YEAR"] = nba.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d").year)

# points

nba["norm_pts"] = preprocessing.scale(nba["pts"])

nba["lag_point_rolling3_avg"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
nba["lag_point_rolling6_avg"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
nba["lag_point_rolling9_avg"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

nba["lag_point_rolling3_max"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
nba["lag_point_rolling6_max"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
nba["lag_point_rolling9_max"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

nba["lag_point_rolling3_min"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
nba["lag_point_rolling6_min"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
nba["lag_point_rolling9_min"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

nba["lag_point_rolling3_std"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
nba["lag_point_rolling6_std"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
nba["lag_point_rolling9_std"] = nba.groupby(["id"]).pts.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# gmsc

nba["lag_gmsc_rolling3_avg"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
nba["lag_gmsc_rolling6_avg"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
nba["lag_gmsc_rolling9_avg"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

nba["lag_gmsc_rolling3_max"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
nba["lag_gmsc_rolling6_max"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
nba["lag_gmsc_rolling9_max"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

nba["lag_gmsc_rolling3_min"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
nba["lag_gmsc_rolling6_min"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
nba["lag_gmsc_rolling9_min"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

nba["lag_gmsc_rolling3_std"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
nba["lag_gmsc_rolling6_std"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
nba["lag_gmsc_rolling9_std"] = nba.groupby(["id"]).gmsc.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# Time played

nba["seconds_played"] = nba.mp.apply(lambda x: min_to_sec(x))

nba["lag_time_played_rolling3_avg"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).mean())
nba["lag_time_played_rolling6_avg"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).mean())
nba["lag_time_played_rolling9_avg"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).mean())

nba["lag_time_played_rolling3_max"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).max())
nba["lag_time_played_rolling6_max"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).max())
nba["lag_time_played_rolling9_max"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).max())

nba["lag_time_played_rolling3_min"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).min())
nba["lag_time_played_rolling6_min"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).min())
nba["lag_time_played_rolling9_min"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).min())

nba["lag_time_played_rolling3_std"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(3, min_periods=2).std())
nba["lag_time_played_rolling6_std"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(6, min_periods=2).std())
nba["lag_time_played_rolling9_std"] = nba.groupby(["id"]).seconds_played.shift().transform(lambda x: x.rolling(9, min_periods=2).std())

# age

nba["age"] = nba.age.apply(lambda x: int(x.split(sep="-")[0]))

# writing *.csv files

nba.to_csv("C:/Users/USER/Downloads/nba.csv")
ucr.to_csv("C:/Users/USER/Downloads/ucr.csv")