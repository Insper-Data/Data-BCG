import pandas as pd
import numpy as np
from datetime import datetime
from siuba import *
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
import tkinter as tk
from tkinter import filedialog
import shap
from boruta import BorutaPy
import pickle
import lightgbm as lgb

# # Function that identifies the database's filepath
# def get_datapath(message):
#     root = tk.Tk()
#     root.withdraw()
#     return filedialog.askopenfilename(title=message)
# db = pd.read_csv(get_datapath(message="Select file"))

# Importing the database
db = pd.read_csv("pre_model_data/df_2009_2015_feat_engineered9.csv")

# # Removing useless variables
db = (db >>
      select(-_["age","hs_city", "county_name", "Unnamed: 0":"g", "tm":"pts", "county_fips":"norm_tm_pts",
              "norm_arrests":"median_arrests_year", "norm_hhtenure":"norm_nfathers", "norm_pts":"norm_gmsc"]))

# Initializing label encoder
le = LabelEncoder()
db["state_cat"] = le.fit_transform(db["state"])
db["birthplace_cat"] = le.fit_transform(db["birthplace"])

# Removing na's, city and state columns
db.dropna(axis="rows", inplace=True)
db.drop(["state","birthplace"],axis="columns", inplace=True)

# Separating X and Y
y = db["gmsc"].ravel()
X = db.drop("gmsc", axis="columns")
X_copy = X[:]
X.drop("date", axis="columns", inplace=True)

# Saving feature names for later use
feature_names = X.columns

# Transforming in to array
X = X.values

# Time-consistent train and test split
tscv = TimeSeriesSplit()
for train_index, test_index in tscv.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

# # Creating random forest model
# rf = RandomForestRegressor(n_estimators=200, random_state=1234, n_jobs=-1, max_depth=10)
#
# # Fitting rf model on training data
# rf.fit(X_train, y_train)
#
# # Predicting on test data
# y_hat_rf = rf.predict(X_test)
#
# # Model performance
# RMSE_rf = np.sqrt(mean_squared_error(y_hat_rf, y_test))
# r2_rf = r2_score(y_test, y_hat_rf)
#
# # Boruta
# feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1, perc=1)
# feat_selector.fit(X, y)
#
# # Selected vars
# selected_vars = feature_names[feat_selector.support_].to_list()
#
# # Removed vars
# removed_vars = [var for var in feature_names if var not in selected_vars]
#
# # Selecting boruta vars to retrain model
# X_boruta = db[selected_vars].values
#
# for train_index, test_index in tscv.split(X_boruta):
#     X_train, X_test = X_boruta[train_index], X_boruta[test_index]
#     y_train, y_test = y[train_index], y[test_index]
#
# # Refitting model based on boruta vars
# rf.fit(X_train, y_train)
#
# # Analyzing model performance with boruta vars
# y_hat_rf = rf.predict(X_test)
# RMSE_rf_boruta = np.sqrt(mean_squared_error(y_hat_rf, y_test))
# r2_rf_boruta = r2_score(y_test, y_hat_rf)
#
# # SHAP
# explainer = shap.TreeExplainer(rf)
# shap_values = explainer.shap_values(X_train)
#
# # Making dataframe of shapley values
# shap_df = pd.DataFrame(data=shap_values, columns=selected_vars)
# shap_df = shap_df.mean(axis="rows").abs().sort_values(ascending=False)
#
# # # Visualizing SHAP results
# # shap.summary_plot(shap_values, X_train, plot_type="bar", feature_names=selected_vars)
# # shap.summary_plot(shap_values, X_train, feature_names=selected_vars)
#
# # Saving SHAP results with pickle
# filename="shap_result_perc_1"
# outfile = open(filename,'wb')
# pickle.dump(shap_values, outfile)
# outfile.close()

# # Opening SHAP results with pickle
# infile = open("shap_result", "rb")
# shap_values = pickle.load(infile)

#########################################
# LightGBM

# Creating datasets
# Train and test
lgb_train = lgb.Dataset(X_train, y_train, feature_name=feature_names.tolist(),
                        categorical_feature=["state_cat", "birthplace_cat"])

# specify your configurations as a dict
params = {
   'boosting': 'rf',
   'objective': 'regression',
   'metric': 'rmse',
   'num_leaves': 31,
   'learning_rate': 0.05,
   'feature_fraction': 0.9,
   'bagging_fraction': 0.8,
   'bagging_freq': 5,
   'verbose': 1,
   'num_threads': 4,
    'num_boost_round': 100
}

# Initializing regressor
lgbmreg = lgb.LGBMRegressor(boosting_type="rf", objective="regression", max_iterations=1000, num_leaves=31,
                            min_data_in_leaf=27, max_depth=-1, learning_rate=0.015, feature_fraction=0.9,
                            bagging_freq=1, bagging_fraction=0.9, bagging_seed=11, metric="rmse", verbosity=-1,
                            nthread=4, num_boost_round=100)

# Train
lgbm_model = lgb.train(params, lgb_train)

# predict
y_pred_lgb = lgbm_model.predict(X_test, num_iteration=lgbm_model.best_iteration)

# Model performance
RMSE_lgb = np.sqrt(mean_squared_error(y_pred_lgb, y_test))
r2_rf = r2_score(y_test, y_pred_lgb)

# Boruta
feat_selector = BorutaPy(lgbmreg, n_estimators='auto', verbose=2, random_state=1, perc=90)
feat_selector.fit(X, y)

# Selected vars
selected_vars = feature_names[feat_selector.support_].to_list()

# Selecting boruta vars to retrain model
X_boruta = db[selected_vars]

for train_index, test_index in tscv.split(X_boruta):
    X_train, X_test = X_boruta.values[train_index], X_boruta.values[test_index]
    y_train, y_test = y[train_index], y[test_index]

# Train and test
lgb_train = lgb.Dataset(X_train, y_train, feature_name=selected_vars,
                        categorical_feature=["state_cat", "birthplace_cat"])

# Train
lgbm_model = lgb.train(params, lgb_train)

# predict test
y_pred_lgb_test = lgbm_model.predict(X_test, num_iteration=lgbm_model.best_iteration)

# Model performance on test data
RMSE_lgb_boruta_test = np.sqrt(mean_squared_error(y_pred_lgb_test, y_test))
r2_rf_boruta_test = r2_score(y_test, y_pred_lgb_test)

# predict train
y_pred_lgb_train = lgbm_model.predict(X_train, num_iteration=lgbm_model.best_iteration)

# Model performance on training data
RMSE_lgb_boruta_train = np.sqrt(mean_squared_error(y_pred_lgb_train, y_train))
r2_rf_boruta_train = r2_score(y_train, y_pred_lgb_train)

# Analyzing model performance over time

X_boruta["parsed_date"] = [datetime.strptime(date, "%Y-%m-%d") for date in X_copy.date]


def train_test(X, y, date):
    train_index = X.parsed_date <= date
    test_date = sorted(list(set(X[X.parsed_date > date].parsed_date)))[0]
    test_index = X.parsed_date == test_date
    X_train = X[train_index].reset_index().drop(["parsed_date", "index"], axis="columns")
    X_train = X_train.values
    y_train = y[train_index]
    X_test = X[test_index].reset_index().drop(["parsed_date", "index"], axis="columns").values
    y_test = y[test_index]
    return X_train, y_train, X_test, y_test

dic = {}

for date in sorted(list(set(X_boruta.parsed_date)))[:len(set(X_boruta.parsed_date)) - 1]:
    X_train, y_train, X_test, y_test = train_test(X_boruta, y, date)

    # Train and test
    lgb_train = lgb.Dataset(X_train, y_train, feature_name=selected_vars,
                            categorical_feature=["state_cat", "birthplace_cat"])

    # Train
    lgbm_model = lgb.train(params, lgb_train)

    # predict test
    y_pred_lgb_test = lgbm_model.predict(X_test, num_iteration=lgbm_model.best_iteration)

    # Model performance on test data
    RMSE_lgb_boruta_test = np.sqrt(mean_squared_error(y_pred_lgb_test, y_test))
    r2_rf_boruta_test = r2_score(y_test, y_pred_lgb_test)

    # predict train
    y_pred_lgb_train = lgbm_model.predict(X_train, num_iteration=lgbm_model.best_iteration)

    # Model performance on training data
    RMSE_lgb_boruta_train = np.sqrt(mean_squared_error(y_pred_lgb_train, y_train))
    r2_rf_boruta_train = r2_score(y_train, y_pred_lgb_train)

    dic[str(date)] = (RMSE_lgb_boruta_test, r2_rf_boruta_test, RMSE_lgb_boruta_train, r2_rf_boruta_train)
    print(date)

# Saving lgbm dict results with pickle
filename="lgbm_dict"
outfile = open(filename,'wb')
pickle.dump(dic, outfile)
outfile.close()
