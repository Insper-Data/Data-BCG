import pandas as pd
import os
# Para carregar um dataframe tão grande devemos utilizar o a capacidade
# de processamento paralelo do computador. Para isso podemos utilizar
# o pacote Dask que implementa essa funcionalidade utilizando a mesma
# sintaxe do Pandas. Para instalar deve-se utilizar "pip3 install dask[complete]"
from dask import dataframe as dd
from dask.diagnostics import ProgressBar
ProgressBar().register()

# Configurando path do projeto
cwd = os.getcwd()
project_wd = os.path.dirname(cwd)

# Lendo dataframe com anos desejados apenas
textfilereader = pd.read_csv("raw_data/cps.csv", iterator=True, index_col=[0])
df = textfilereader.get_chunk(5000)

# descobrindo colunas com apenas Nas
percent_missing = df.isnull().sum() * 100 / len(df)
missing_value_df = pd.DataFrame({'column_name': df.columns, 'percent_missing': percent_missing})
missing_value_df = missing_value_df[missing_value_df["percent_missing"]==100]
missing_cols = list(missing_value_df["column_name"])

# Removendo anos indesejados
dask_df = dd.read_csv("raw_data/cps.csv", assume_missing=True)

# Removendo colunas com apenas Nas
dask_df = dask_df.drop(missing_cols, axis=1)

# Computando
dask_df = dask_df.compute()

# Corrigindo Income pela inflação
dask_df["HHINCOME"] = dask_df["HHINCOME"] * dask_df["CPI99"]
dask_df["FAMINC"] = dask_df["FAMINC"] * dask_df["CPI99"]

# Salvando dataframe
dask_df.to_csv("cleaned_data/cps_cleaned.csv")

# Separando por anos
anos_80_99 = list(range(1980, 1999))
cps_80_99 = dask_df[dask_df.YEAR.isin(anos_80_99)]

anos_20_16 = list(range(2000, 2016))
cps_20_16 = dask_df[dask_df.YEAR.isin(anos_20_16)]

# Salvando dataframes
cps_80_99.to_csv("cleaned_data/cps_1980_1999_cleaned.csv")
cps_20_16.to_csv("cleaned_data/cps_2000_2016_cleaned.csv")