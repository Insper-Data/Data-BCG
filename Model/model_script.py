import pandas as pd
import numpy as np
from siuba import *
import statsmodels.api as sm
import statsmodels.formula.api as smf
import patsy
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import tkinter as tk
from tkinter import filedialog

# Function that identifies the database's filepath
def get_datapath(message):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=message)

# Importing the database
db = pd.read_csv(get_datapath("Selecione a base de dados"))

# Removing useless variables
db = (db >>
      select(-_["player":"date", "tm":"pts", "state":"YEAR"], _.norm_pts))

# " + ".join(db.columns) # -> makes writing the formula easier

y, X = patsy.dmatrices('gmsc ~ age + lag_point_rolling3_avg \
                        + lag_point_rolling6_avg + lag_point_rolling9_avg + lag_point_rolling3_min \
                        + lag_point_rolling6_min + lag_point_rolling9_min + lag_point_rolling3_std \
                        + lag_point_rolling6_std + lag_point_rolling9_std + lag_gmsc_rolling3_avg \
                        + lag_gmsc_rolling6_avg + lag_gmsc_rolling9_avg + lag_gmsc_rolling3_min \
                        + lag_gmsc_rolling6_min + lag_gmsc_rolling9_min + lag_gmsc_rolling3_std \
                        + lag_gmsc_rolling6_std + lag_gmsc_rolling9_std + seconds_played \
                        + lag_time_played_rolling3_avg + lag_time_played_rolling6_avg \
                        + lag_time_played_rolling9_avg + lag_time_played_rolling3_min \
                        + lag_time_played_rolling6_min + lag_time_played_rolling9_min \
                        + lag_time_played_rolling3_std + lag_time_played_rolling6_std \
                        + lag_time_played_rolling9_std + ASECFLAG + ASECWTH + MISH \
                        + NUMPREC + HHTENURE + GQ + HHINTYPE + CPI99 + REGION + STATEFIP \
                        + METRO + METAREA + OWNERSHP + HHINCOME + PUBHOUS + RENTSUB \
                        + FOODSTMP + STAMPNO + STAMPMO + ATELUNCH + LUNCHSUB + FRELUNCH \
                        + STAMPVAL + FAMINC + UNITSSTR + NFAMS + NCOUPLES + NMOTHERS \
                        + NFATHERS + HRHHID + HSEQ + HHRESPLN + M0_9 + M10_12 + M13_14 \
                        + M15 + M16 + M17 + M18 + M19 + M20 + M21 + M22 + M23 + M24 \
                        + M25_29 + M30_34 + M35_39 + M40_44 + M45_49 + M50_54 + M55_59 \
                        + M60_64 + M65 + F0_9 + F10_12 + F13_14 + F15 + F16 + F17 + F18 \
                        + F19 + F20 + F21 + F22 + F23 + F24 + F25_29 + F30_34 + F35_39 \
                        + F40_44 + F45_49 + F50_54 + F55_59 + F60_64 + F65 + AW + AB \
                        + AI + AA + JW + JB + JI + JA + AH + AN + JH + JN + arrests \
                        + norm_arrests + mean_arrests_year + std_arrests_year + min_arrests_year \
                        + median_arrests_year + rolling_avg3_arrests + rolling_avg6_arrests \
                        + rolling_avg9_arrests + rolling_std3_arrests + rolling_std6_arrests \
                        + rolling_std9_arrests' , data = db)

X_trn, X_tst, y_trn, y_tst = train_test_split(X, y, test_size=0.7, random_state=1234)

# Random Forest Model

## Defining the Model
rf = RandomForestRegressor(n_estimators=500, random_state=1234)

## Fitting
rf.fit(X_trn, y_trn.ravel())

## Analyzing the model's performance
y_hat_rf = rf.predict(X_tst)
RMSE_rf = np.sqrt(mean_squared_error(y_hat_rf, y_tst))
np.round(RMSE_rf, 2)
r2_rf = r2_score(y_tst, y_hat_rf)
np.round(r2_rf, 2)

#########################################

# Gradient Boosted Decision-Trees

## Defining the Model
boost = GradientBoostingRegressor(learning_rate=0.3, random_state=1234)

## Fitting
boost.fit(X_trn, y_trn.ravel())

## Analyzing the model's performance
y_hat_boost = boost.predict(X_tst)
RMSE_boost = np.sqrt(mean_squared_error(y_tst, y_hat_boost))
np.round(RMSE_boost, 2)
r2_boost = r2_score(y_tst, y_hat_boost)
np.round(r2_boost, 2)