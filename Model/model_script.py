import pandas as pd
import numpy as np
from siuba import *
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
import tkinter as tk
from tkinter import filedialog
import shap
from boruta import BorutaPy
import pickle

# # Function that identifies the database's filepath
# # def get_datapath(message):
# #     root = tk.Tk()
# #     root.withdraw()
# #     return filedialog.askopenfilename(title=message)
# # db = pd.read_csv(get_datapath(message="Select file"))

# Importing the database
db = pd.read_csv("pre_model_data/df_2009_2015_feat_engineered9.csv")

# # Removing useless variables
db = (db >>
      select(-_["age","hs_city", "county_name", "Unnamed: 0":"date", "tm":"pts", "county_fips":"norm_tm_pts",
              "norm_arrests":"median_arrests_year", "norm_hhtenure":"norm_nfathers", "norm_pts":"norm_gmsc"]))

# Removing na's
db.dropna(axis="rows", inplace=True)

# Separating X and Y
y = db["gmsc"].to_numpy()
X = db.drop("gmsc", axis="columns")

# Creating random forest model
rf = RandomForestRegressor(n_estimators=200, random_state=1234, n_jobs=-1, max_depth=10)

# Creating column transformer to separate categorical data and pipeline for rf
column_trans = make_column_transformer((OneHotEncoder(), ["state", "birthplace"]), remainder="passthrough")
column_trans.fit_transform(X)

# Saving feature names for later use
feature_names = column_trans.get_feature_names()

# Saving encoded features
X_enc = column_trans.fit_transform(X)

# Time-consistent train and test split
tscv = TimeSeriesSplit()
for train_index, test_index in tscv.split(X_enc):
    X_train, X_test = X_enc[train_index], X_enc[test_index]
    y_train, y_test = y[train_index], y[test_index]

# Fitting rf model on training data
rf.fit(X_train, y_train.ravel())

# Predicting on test data
y_hat_rf = rf.predict(X_test)

# Model performance
RMSE_rf = np.sqrt(mean_squared_error(y_hat_rf, y_test))
np.round(RMSE_rf, 2)
r2_rf = r2_score(y_test, y_hat_rf)
np.round(r2_rf, 2)


# # Boruta
# feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1, perc=0.99)
# feat_selector.fit(X, y.ravel())
# selected_vars = X.columns[feat_selector.support_].to_list()
#
# X_boruta = X[selected_vars]
# db_boruta = pd.merge(y, X_boruta, left_index=True, right_index=True)
# y, X_boruta = patsy.dmatrices("gmsc ~ state", data=db_boruta, return_type="matrix")
#
# for train_index, test_index in tscv.split(X):
#     print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = X_boruta[train_index], X_boruta[test_index]
#     y_train, y_test = y[train_index], y[test_index]

# # #
# # Defining the Model
# rf = RandomForestRegressor(n_estimators=200, random_state=1234, n_jobs=-1, max_depth=10)
# #
# # Fitting
# rf.fit(X_train, y_train.ravel())
# #
# # Analyzing the model's performance
# y_hat_rf = rf.predict(X_test)
# RMSE_rf_boruta = np.sqrt(mean_squared_error(y_hat_rf, y_test))
# np.round(RMSE_rf_boruta, 2)
# r2_rf_boruta = r2_score(y_test, y_hat_rf)
# np.round(r2_rf_boruta, 2)
#
# # SHAP
# explainer = shap.TreeExplainer(rf)
# shap_values = explainer.shap_values(X_train)
#
# # Visualizando resultados do SHAP
# shap.summary_plot(shap_values, X_train, plot_type="bar", feature_names=["", "Média Móvel Pontos (6 jogos)", "Média Móvel GMSC (9 jogos)",
#                                                                         "Média Móvel Tempo de Jogo (3 jogos)", "Tempo de Jogo"])
#
# shap.summary_plot(shap_values, X_train, feature_names=["", "Média Móvel Pontos (6 jogos)", "Média Móvel GMSC (9 jogos)",
#                                                                         "Média Móvel Tempo de Jogo (3 jogos)", "Tempo de Jogo"])
#
# # Salvando resultado do SHAP com pickle
# filename="shap_result"
# outfile = open(filename,'wb')
# pickle.dump(shap_values, outfile)
# outfile.close()

# # Abrindo resultado do SHAP com pickle
# infile = open("shap_result", "rb")
# shap_values = pickle.load(infile)

#########################################


# # Gradient Boosted Decision-Trees
#
# # Defining the Model
# boost = GradientBoostingRegressor(learning_rate=0.3, random_state=1234)
#
# # Fitting
# boost.fit(X_train, y_train.ravel())
#
# # Analyzing the model's performance
# y_hat_boost = boost.predict(X_test)
# RMSE_boost = np.sqrt(mean_squared_error(y_test, y_hat_boost))
# np.round(RMSE_boost, 2)
# r2_boost = r2_score(y_test, y_hat_boost)
# np.round(r2_boost, 2)
#
# # Boruta
# feat_selector = BorutaPy(boost, n_estimators='auto', verbose=2, random_state=1)
# feat_selector.fit(X, y.ravel())
# selected_vars = X.columns[feat_selector.support_].to_list()
# selected_vars_weak = X.columns[feat_selector.support_weak_].to_list()
#
# # Selecting olny boruta approved variables
# y_boruta, X_boruta = patsy.dmatrices("gmsc ~ + lag_point_rolling3_avg + lag_point_rolling6_avg + lag_point_rolling9_avg + lag_gmsc_rolling3_avg \
#                                      + lag_gmsc_rolling6_avg + lag_gmsc_rolling9_avg + lag_gmsc_rolling9_std + lag_time_played_rolling3_avg \
#                                      + lag_time_played_rolling6_avg + lag_time_played_rolling9_avg + lag_time_played", data=db, return_type="matrix")
#
# # Splitting training and test for boruta selction
# tscv = TimeSeriesSplit()
#
# for train_index, test_index in tscv.split(X):
#     print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = X_boruta[train_index], X_boruta[test_index]
#     y_train, y_test = y_boruta[train_index], y_boruta[test_index]
#
#
# # Fitting with Boruta selection
# boost = GradientBoostingRegressor(learning_rate=0.3, random_state=1234)
# boost.fit(X_train, y_train.ravel())
#
# # Analyzing the model's performance with boruta selection
# y_hat_boost = boost.predict(X_test)
# RMSE_boost = np.sqrt(mean_squared_error(y_test, y_hat_boost))
# np.round(RMSE_boost, 2)
# r2_boost = r2_score(y_test, y_hat_boost)
# np.round(r2_boost, 2)
#
# # SHAP with boruta selection
# explainer = shap.TreeExplainer(boost)
# shap_values = explainer.shap_values(X_train)
#
# # # Visualizando resultados do SHAP
# shap.summary_plot(shap_values, X_train, plot_type="bar", feature_names=['',  'Média Móvel Pontos (3 jogos)',
#     'Média Móvel Pontos (6 jogos)', 'Média Móvel Pontos (9 jogos)', 'Média Móvel GMSC (3 jogos)', 'Média Móvel GMSC (6 jogos)',
#     'Média Móvel GMSC (9 jogos)', 'Desvio Padrão GMSC (9 jogos)', 'Média Móvel Tempo de Jogo (3 jogos)', 'Média Móvel Tempo de Jogo (6 jogos)',
#     'Média Móvel Tempo de Jogo (9 jogos)', 'Tempo de Jogo'])
# shap.summary_plot(shap_values, X_train, feature_names=['',  'Média Móvel Pontos (3 jogos)',
#     'Média Móvel Pontos (6 jogos)', 'Média Móvel Pontos (9 jogos)', 'Média Móvel GMSC (3 jogos)', 'Média Móvel GMSC (6 jogos)',
#     'Média Móvel GMSC (9 jogos)', 'Desvio Padrão GMSC (9 jogos)', 'Média Móvel Tempo de Jogo (3 jogos)', 'Média Móvel Tempo de Jogo (6 jogos)',
#     'Média Móvel Tempo de Jogo (9 jogos)', 'Tempo de Jogo'])

## Salvando resultado do SHAP com pickle
# filename="boost_result"
# outfile = open(filename,'wb')
# pickle.dump(shap_values, outfile)
# outfile.close()

## Abrindo resultado do SHAP com pickle
# infile = open("boost_result", "rb")
# shap_values = pickle.load(infile)



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
