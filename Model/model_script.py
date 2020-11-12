import pandas as pd
import numpy as np
from siuba import *
import statsmodels.api as sm
import statsmodels.formula.api as smf
import patsy
from sklearn.metrics import mean_squared_error
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
      select(-_["player":"pts", "X30":"MONTH"]))

# " + ".join(db.columns) -> makes writing the formula easier

y, X = patsy.dmatrices("gmsc ~ 0 + ASECFLAG + ASECWTH \
                            + MISH + NUMPREC + HHTENURE + GQ + HHINTYPE + CPI99 + REGION \
                            + STATEFIP + METRO + METAREA + OWNERSHP + HHINCOME + PUBHOUS \
                            + RENTSUB + FOODSTMP + STAMPNO + STAMPMO + ATELUNCH + LUNCHSUB \
                            + FRELUNCH + STAMPVAL + FAMINC + UNITSSTR + NFAMS + NCOUPLES \
                            + NMOTHERS + NFATHERS + HRHHID + HSEQ + HHRESPLN + arrests", data = db)

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

#########################################

# Gradient Boosted Decision-Trees

## Defining the Model
boost = GradientBoostingRegressor(learning_rate=0.3, random_state=1234)

## Fitting
boost.fit(X_trn, y_trn.ravel())

## Analyzing the model's performance
y_hat_boost = boost.predict(X_tst)
RMSE_boost = np.sqrt(mean_squared_error(y_hat_boost, y_tst))
np.round(RMSE_boost, 2)