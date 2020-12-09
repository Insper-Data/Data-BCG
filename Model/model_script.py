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
def get_datapath(message):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title=message)

db = get_datapath(message="Select file")

# Importing the database
db = pd.read_csv("pre_model_data/df_2009_2015_feat_engineered3.csv")

# Removing useless variables
db = (db >>
      select(-_["Unnamed: 0":"date", "tm":"pts", "metarea":"norm_arrests", "norm_pts", "norm_gmsc", "norm_hhtenure":"norm_nfathers"]))

# " + ".join(db.columns) # -> makes writing the formula easier

y, X = patsy.dmatrices("gmsc ~ age + norm_pts_lag \
                        + won_last \
                        + norm_arrests_lag \
                        + lag_rolling_avg3_arrests \
                        + lag_rolling_std3_arrests + time_played_lag", data=db)

# Time-consistent train and test split

tscv = TimeSeriesSplit()
print(tscv)

for train_index, test_index in tscv.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]


# Random Forest Model

## Defining the Model
rf = RandomForestRegressor(n_estimators=500, random_state=1234, n_jobs=4)

## Fitting
rf.fit(X_train, y_train.ravel())

## Analyzing the model's performance
y_hat_rf = rf.predict(X_test)
RMSE_rf = np.sqrt(mean_squared_error(y_hat_rf, y_test))
np.round(RMSE_rf, 2)
r2_rf = r2_score(y_test, y_hat_rf)
np.round(r2_rf, 2)

explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_train)

#Boruta
feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1)

# find all relevant features - 5 features should be selected
feat_selector.fit(X, y.ravel())

# check selected features - first 5 features are selected
feat_selector.support_

# check ranking of features
feat_selector.ranking_

# call transform() on X to filter it down to selected features
X_filtered = feat_selector.transform(X)

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
