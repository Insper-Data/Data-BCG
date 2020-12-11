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
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
import boruta


# Function that identifies the database's filepath
# def get_datapath(message):
#     root = tk.Tk()
#     root.withdraw()
#     return filedialog.askopenfilename(title=message)

# db = pd.read_csv(get_datapath(message="Select file"))

# Importing the database
db = pd.read_csv("pre_model_data/df_2009_2015_feat_engineered9.csv")

# Removing useless variables
db = (db >>
      select(-_["age", "Unnamed: 0":"date", "tm":"pts", "county_fips":"norm_tm_pts",
              "norm_arrests":"median_arrests_year", "norm_hhtenure":"norm_nfathers"]))

# " + ".join(db.columns) # -> makes writing the formula easier

y, X = patsy.dmatrices("gmsc ~ month + year \
                        + lag_age \
                        + lag_gmsc \
                        + state \
                        + birthplace + lag_norm_opp_3p + lag_norm_opp_ast + lag_norm_opp_stl + lag_norm_opp_blk \
                        + lag_norm_tm_3p + lag_norm_tm_ast + lag_norm_tm_stl + lag_norm_tm_blk \
                        + lag_arrests + lag_mean_arrests_year + lag_rolling_avg3_arrests + lag_pts + lag_point_rolling3_avg \
                        + lag_point_rolling6_avg + lag_point_rolling9_avg + lag_point_rolling3_max + lag_point_rolling6_max \
                        + lag_point_rolling9_max + lag_point_rolling3_min + lag_point_rolling6_min + lag_point_rolling9_min \
                        + lag_point_rolling3_std + lag_point_rolling6_std + lag_point_rolling9_std \
                        + lag_gmsc_rolling3_avg + lag_gmsc_rolling6_avg + lag_gmsc_rolling9_avg \
                        + lag_gmsc_rolling3_max + lag_gmsc_rolling6_max + lag_gmsc_rolling9_max \
                        + lag_gmsc_rolling3_min + lag_gmsc_rolling6_min + lag_gmsc_rolling9_min \
                        + lag_gmsc_rolling3_std + lag_gmsc_rolling6_std + lag_gmsc_rolling9_std \
                        + lag_time_played_rolling3_avg + lag_time_played_rolling6_avg + lag_time_played_rolling9_avg \
                        + lag_time_played_rolling3_max + lag_time_played_rolling6_max + lag_time_played_rolling9_max \
                        + lag_time_played_rolling3_min + lag_time_played_rolling6_min + lag_time_played_rolling9_min \
                        + lag_time_played_rolling3_std + lag_time_played_rolling6_std + lag_time_played_rolling9_std \
                        + lag_time_played \
                        + lag_norm_hhtenure + lag_norm_ownershp + lag_norm_hhincome + lag_norm_pubhous \
                        + lag_norm_rentsub + lag_norm_foodstmp + lag_norm_atelunch + lag_norm_lunchsub \
                        + lag_norm_frelunch + lag_norm_stampval + lag_norm_faminc + lag_norm_nfams + lag_norm_ncouples \
                        + lag_norm_nmothers + lag_norm_nfathers", data=db)


# # Time-consistent train and test split
# tscv = TimeSeriesSplit()
# print(tscv)
#
# for train_index, test_index in tscv.split(X):
#     print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]
#
#
# # Random Forest Model
#
# ## Defining the Model
# rf = RandomForestRegressor(n_estimators=500, random_state=1234, n_jobs=4)
#
# ## Fitting
# rf.fit(X_train, y_train.ravel())
#
# ## Analyzing the model's performance
# y_hat_rf = rf.predict(X_test)
# RMSE_rf = np.sqrt(mean_squared_error(y_hat_rf, y_test))
# np.round(RMSE_rf, 2)
# r2_rf = r2_score(y_test, y_hat_rf)
# np.round(r2_rf, 2)
#
# explainer = shap.TreeExplainer(rf)
# shap_values = explainer.shap_values(X_train)
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
# boost.fit(X_train, y_train.ravel())
#
# ## Analyzing the model's performance
# y_hat_boost = boost.predict(X_test)
# RMSE_boost = np.sqrt(mean_squared_error(y_test, y_hat_boost))
# np.round(RMSE_boost, 2)
# r2_boost = r2_score(y_test, y_hat_boost)
# np.round(r2_boost, 2)

# LightGBM
# Creating dataset
# lgb_train = lgb.Dataset(X_train, y_train.ravel())
# lgb_eval = lgb.Dataset(X_test, y_test.ravel(), reference=lgb_train)
#
# # specify your configurations as a dict
# params = {
#    'boosting_type': 'gbdt',
#    'objective': 'regression',
#    'metric': {'l2', 'l1'},
#    'num_leaves': 31,
#    'learning_rate': 0.05,
#    'feature_fraction': 0.9,
#    'bagging_fraction': 0.8,
#    'bagging_freq': 5,
#    'verbose': 0,
#    'num_threads': 4
# }
#
# print('Starting training...')
# # train
# gbm = lgb.train(params,
#                lgb_train,
#                num_boost_round=20,
#                valid_sets=lgb_eval,
#                early_stopping_rounds=5)
#
# print('Saving model...')
# # save model to file
# gbm.save_model('model.txt')
#
# print('Starting predicting...')
# # predict
# y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
# # eval
# print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)
