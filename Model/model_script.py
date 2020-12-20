import pandas as pd
import numpy as np
from siuba import *
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
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

# Saving feature names for later use
feature_names = X.columns

# Trasnforming features to numpy array
X = X.to_numpy()

# Time-consistent train and test split
tscv = TimeSeriesSplit()
for train_index, test_index in tscv.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

# Creating random forest model
rf = RandomForestRegressor(n_estimators=200, random_state=1234, n_jobs=-1, max_depth=10)

# Fitting rf model on training data
rf.fit(X_train, y_train)

# Predicting on test data
y_hat_rf = rf.predict(X_test)

# Model performance
RMSE_rf = np.sqrt(mean_squared_error(y_hat_rf, y_test))
np.round(RMSE_rf, 2)
r2_rf = r2_score(y_test, y_hat_rf)
np.round(r2_rf, 2)

# Boruta
feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1, perc=1)
feat_selector.fit(X, y)

# Selected vars
selected_vars = X.columns[feat_selector.support_].to_list()

# Removed vars
removed_vars = [var for var in X.columns.values if var not in selected_vars]

# Selecting boruta vars to retrain model
X_boruta = db[selected_vars].values

for train_index, test_index in tscv.split(X_boruta):
    X_train, X_test = X_boruta[train_index], X_boruta[test_index]
    y_train, y_test = y[train_index], y[test_index]

# Refitting model based on boruta vars
rf.fit(X_train, y_train)

# Analyzing model performance with boruta vars
y_hat_rf = rf.predict(X_test)
RMSE_rf_boruta = np.sqrt(mean_squared_error(y_hat_rf, y_test))
np.round(RMSE_rf_boruta, 2)
r2_rf_boruta = r2_score(y_test, y_hat_rf)
np.round(r2_rf_boruta, 2)

# SHAP
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_train)

# Making dataframe of shapley values
shap_df = pd.DataFrame(data=shap_values, columns=selected_vars)
shap_df = shap_df.mean(axis="rows").abs().sort_values(ascending=False)

# # Visualizing SHAP results
# shap.summary_plot(shap_values, X_train, plot_type="bar", feature_names=selected_vars)
# shap.summary_plot(shap_values, X_train, feature_names=selected_vars)

# Saving SHAP results with pickle
# filename="shap_result_perc_99"
# outfile = open(filename,'wb')
# pickle.dump(shap_values, outfile)
# outfile.close()

# # Opening SHAP results with pickle
# infile = open("shap_result", "rb")
# shap_values = pickle.load(infile)

#########################################

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
