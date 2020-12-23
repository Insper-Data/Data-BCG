import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import pickle
from siuba import *
from datetime import datetime as dt

# Opening SHAP results with pickle
infile = open("lgbm_dict", "rb")
lgbm_dict = pickle.load(infile)

asdas=pickle.load(infile)


df_r2 = pd.DataFrame(columns=["game_id", "year", "r2_test", "r2_train"])
df_RMSE = pd.DataFrame(columns=["game_id", "year", "test", "train"])

for name, values in lgbm_dict.items():
        r2 = pd.DataFrame({"game_id": [name], "year": [values[4]], "r2_test": [values[1]], "r2_train":[values[3]]})
        df_r2 = df_r2.append(r2)

        RMSE = pd.DataFrame({"game_id": [name], "year": [values[4]], "test": [values[0]], "train": [values[2]]})
        df_RMSE = df_RMSE.append(RMSE)

# R2
r2_melted = df_r2[df_r2.r2_test > 0].melt(id_vars="game_id") >> arrange(_.date)
sn.lineplot(data = r2_melted, x = "game_id", y = "value", hue = "variable")

r2_melted.to_csv("C:/Users/USER/Downloads/r2_results.csv")

# RMSE
RMSE_melted = df_RMSE.melt(id_vars="game_id") >> arrange(_.date)
sn.lineplot(data = RMSE_melted, x = "game_id", y = "value", hue = "variable")

RMSE_melted.to_csv("C:/Users/USER/Downloads/RMSE_results.csv")