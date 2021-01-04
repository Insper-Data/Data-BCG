import pandas as pd
import numpy as np
from datetime import datetime
from siuba import *
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection._split import _BaseKFold, indexable, _num_samples
from sklearn.utils.validation import _deprecate_positional_args
import tkinter as tk
from tkinter import filedialog
import shap
from boruta import BorutaPy
import pickle
import lightgbm as lgb
import optuna

# # Function that identifies the database's filepath
# def get_datapath(message):
#     root = tk.Tk()
#     root.withdraw()
#     return filedialog.askopenfilename(title=message)
# db = pd.read_csv(get_datapath(message="Select file"))

BORUTA = False
TUNING = False

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

# Saving feature names for later use
feature_names = X.columns

# Trasforming X into an array
X = X.values

if BORUTA:
    rf = RandomForestRegressor(n_estimators=200, random_state=1234, n_jobs=-1, max_depth=10)

    # Boruta
    feat_selector = BorutaPy(rf, n_estimators="auto", verbose=2, random_state=1, perc=70)
    feat_selector.fit(X, y)

    # Selected vars
    boruta_vars = feature_names[feat_selector.support_].to_list()

    # Removed vars
    removed_vars = [var for var in feature_names if var not in selected_vars]

    # Saving Boruta vars
    filename="boruta_perc_70"
    outfile = open(filename,'wb')
    pickle.dump(boruta_vars, outfile)
    outfile.close()

# #########################################
# # LightGBM

if not BORUTA:
    # Reading Boruta vars
    infile = open("boruta_perc_70", "rb")
    boruta_vars = pickle.load(infile)

if TUNING:
    cv = TimeSeriesSplit()

    ## Objective Function
    def objective(trial, cv=cv, cv_fold_func=np.average):
        params = {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting': 'rf',
            'lambda_l1': trial.suggest_loguniform('lambda_l1', 1e-8, 10.0),
            'lambda_l2': trial.suggest_loguniform('lambda_l2', 1e-8, 10.0),
            'num_leaves': trial.suggest_int('num_leaves', 2, 200),
            'feature_fraction': trial.suggest_uniform('feature_fraction', 0.4, 1.0),
            'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.4, 1.0),
            'bagging_freq': trial.suggest_int('bagging_freq', 1, 7),
            'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
            'max_depth': trial.suggest_int('max_depth', 5, 15),
            'learning_rate': trial.suggest_uniform('learning_rate', 0.01, 0.10)}

        # ffitting and returning RMSE scores
        rmse_list = []
        for i, (train_idx, test_idx) in enumerate(tscv.split(X)):
            train_x, valid_x = X[train_idx], X[test_idx]
            train_y, valid_y = y[train_idx], y[test_idx]

            train_data = lgb.Dataset(train_x, label=train_y)

            model = lgb.train(params, train_data)
            pred = model.predict(valid_x)
            rmse = np.sqrt(mean_squared_error(pred, valid_y))
            rmse_list.append(rmse)

        print("Trial done: RMSE values on folds: {}".format(rmse_list))
        return cv_fold_func(rmse_list)

    ## Optuna results
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=80)
    print("Number of finished trials:", len(study.trials))
    print("Best trial:", study.best_trial.params)
    best_params = study.best_trial.params

    # Building parameter dictionary
    fixed_params = {'objective': 'regression',
                    'metric': 'rmse',
                    'boosting': 'gbdt',
                    'num_threads': 4}

    best_params = {**best_params, **fixed_params}

    ## Saving best params
    filename="best_params"
    outfile = open(filename,"wb")
    pickle.dump(best_params, outfile)
    outfile.close()

if not TUNING:
    # Reading best_params
    infile = open("best_params", "rb")
    best_params = pickle.load(infile)


# Fitting lgbm on tuned parameters
# Creating datasets
X_boruta = X_copy[boruta_vars]
X_boruta = X_boruta.values

# Time series split
tscv = TimeSeriesSplit()
for train_index, test_index in tscv.split(X_boruta):
    X_train, X_test = X_boruta[train_index], X_boruta[test_index]
    y_train, y_test = y[train_index], y[test_index]


# Training and eval sets
lgb_train = lgb.Dataset(X_train, y_train, feature_name=boruta_vars, categorical_feature=["birthplace_cat"])
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

# Training model with best params
lgbm_model = lgb.train(best_params, lgb_train, 250, valid_sets=lgb_eval,
                 early_stopping_rounds=50, verbose_eval=20)

# predicting on test data
y_pred_lgb_test = lgbm_model.predict(X_test, num_iteration=lgbm_model.best_iteration)

# Model performance on test data
RMSE_lgb_boruta_test = np.sqrt(mean_squared_error(y_pred_lgb_test, y_test))
r2_rf_boruta_test = r2_score(y_test, y_pred_lgb_test)

# predict train
y_pred_lgb_train = lgbm_model.predict(X_train, num_iteration=lgbm_model.best_iteration)

# Model performance on training data
RMSE_lgb_boruta_train = np.sqrt(mean_squared_error(y_pred_lgb_train, y_train))
r2_rf_boruta_train = r2_score(y_train, y_pred_lgb_train)

# # Analyzing model performance over time
# X_boruta["game_id"] = X_copy["game_id"]
# X_boruta["year"] = X_copy["year"]
#
# # Experimental (nunca usei esse isin)
#
# valid_game_ids = (X_boruta >>
#     count(_.game_id) >>
#     filter(_.n >= 30)).game_id
#
# X_boruta = X_boruta[X_boruta.game_id.isin(valid_game_ids)]
#
# ## Se não funcionar
#
# # valid_game_ids = (X_boruta >>
# #     count(_.game_id) >>
# #     filter(_.n >= 30))
# #
# # X_boruta = (X_boruta >>
# #                 semi_join(valid_game_ids, on="game_id"))
#
# def train_test(X, y, id):
#     train_index = X.game_id <= id
#     test_id = sorted(list(set(X[X.game_id > id].game_id)))[0]
#     test_index = X.game_id == test_id
#     X_train = X[train_index].reset_index().drop(["game_id", "index", "year"], axis="columns")
#     X_train = X_train.values
#     y_train = y[train_index]
#     X_test = X[test_index].reset_index().drop(["game_id", "index", "year"], axis="columns").values
#     y_test = y[test_index]
#     return X_train, y_train, X_test, y_test
#
# dic = {}
#
# for year in sorted(list(set(X_boruta.year))):
#     for id in sorted(list(set(X_boruta.game_id)))[:len(set(X_boruta.game_id)) - 1]:
#         X_train, y_train, X_test, y_test = train_test(X_boruta.loc[X_boruta.year == year, :], y, id)
#
#         # Train and test
#         lgb_train = lgb.Dataset(X_train, y_train, feature_name=selected_vars,
#                                 categorical_feature=["state_cat", "birthplace_cat"])
#
#         # Train
#         lgbm_model = lgb.train(params, lgb_train)
#
#         # predict test
#         y_pred_lgb_test = lgbm_model.predict(X_test, num_iteration=lgbm_model.best_iteration)
#
#         # Model performance on test data
#         RMSE_lgb_boruta_test = np.sqrt(mean_squared_error(y_pred_lgb_test, y_test))
#         r2_rf_boruta_test = r2_score(y_test, y_pred_lgb_test)
#
#         # predict train
#         y_pred_lgb_train = lgbm_model.predict(X_train, num_iteration=lgbm_model.best_iteration)
#
#         # Model performance on training data
#         RMSE_lgb_boruta_train = np.sqrt(mean_squared_error(y_pred_lgb_train, y_train))
#         r2_rf_boruta_train = r2_score(y_train, y_pred_lgb_train)
#
#         dic[str(id)] = (RMSE_lgb_boruta_test, r2_rf_boruta_test, RMSE_lgb_boruta_train, r2_rf_boruta_train, year)
#         print(id)
#
# # # Saving lgbm dict results with pickle
# filename="lgbm_dict_gameid"
# outfile = open(filename,'wb')
# pickle.dump(dic, outfile)
# outfile.close()
# n_ids = X_boruta >> count(_.game_id)
#
