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
import shap
from sklearn.model_selection import cross_val_score
import boruta

# Function that identifies the database's filepath
# def get_datapath(message):
#     root = tk.Tk()
#     root.withdraw()
#     return filedialog.askopenfilename(title=message)

# Importing the database
db = pd.read_csv("pre_model_data/df_2009_2015_feat_engineered5.csv")

# Removing useless variables
db = (db >>
      select(-_["Unnamed: 0":"date", "tm":"pts", "metarea":"norm_arrests", "norm_pts", "norm_gmsc", "norm_hhtenure":"norm_nfathers"]))

# " + ".join(db.columns) # -> makes writing the formula easier

y, X = patsy.dmatrices("gmsc ~ age + lag_point_rolling3_avg \
                        + won_last \
                        + rolling_avg3_arrests \
                        + rolling_std3_arrests + lag_time_played_lag", data=db)

# X_trn, X_tst, y_trn, y_tst = train_test_split(X, y, test_size=0.7, random_state=1234)
#
# # Random Forest Model
#
# ## Defining the Model
# rf = RandomForestRegressor(n_estimators=500, random_state=1234, n_jobs=4)
#
# ## Fitting
# rf.fit(X_trn, y_trn.ravel())
#
# ## Analyzing the model's performance
# y_hat_rf = rf.predict(X_tst)
# RMSE_rf = np.sqrt(mean_squared_error(y_hat_rf, y_tst))
# np.round(RMSE_rf, 2)
# r2_rf = r2_score(y_tst, y_hat_rf)
# np.round(r2_rf, 2)
#
# explainer = shap.TreeExplainer(rf)
# shap_values = explainer.shap_values(X_trn)
#
# #Boruta
# feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1)
#
# # find all relevant features - 5 features should be selected
# feat_selector.fit(X, y.ravel())
#
# # check selected features - first 5 features are selected
# feat_selector.support_
#
# # check ranking of features
# feat_selector.ranking_
#
# # call transform() on X to filter it down to selected features
# X_filtered = feat_selector.transform(X)

#########################################

# # Gradient Boosted Decision-Trees
#
# ## Defining the Model
# boost = GradientBoostingRegressor(learning_rate=0.3, random_state=1234)
#
# ## Fitting
# boost.fit(X_trn, y_trn.ravel())
#
# ## Analyzing the model's performance
# y_hat_boost = boost.predict(X_tst)
# RMSE_boost = np.sqrt(mean_squared_error(y_tst, y_hat_boost))
# np.round(RMSE_boost, 2)
# r2_boost = r2_score(y_tst, y_hat_boost)
# np.round(r2_boost, 2)