import pandas as pd
import matplotlib.pyplot as mpl
import seaborn as sn
import pickle

# Opening SHAP results with pickle
infile = open("lgbm_dict", "rb")
lgbm_dict = pickle.load(infile)


df_r2 = pd.DataFrame(columns=["date", "r2_test", "r2_train"])
df_RMSE = pd.DataFrame(columns=["date", "test", "train"])

for name, values in lgbm_dict.items():
        r2 = pd.DataFrame({"date": [name], "r2_test": [values[1]], "r2_train":[values[3]]})
        df_r2 = df_r2.append(r2)

sn.lineplot(data=df_r2, x="date", y="r2_test")