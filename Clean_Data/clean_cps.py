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

# Lendo códigos Fips dos estados
state_fips_wd = os.path.join(project_wd, "Download_Data/Data/fips_state.csv")
state_fips = pd.read_csv(state_fips_wd)
state_fips.drop(columns="state", inplace=True)
state_fips.rename(columns={"fips_code": "STATEFIP", "post_code": "state"}, inplace=True)

# Lendo dataframe com anos desejados apenas
textfilereader = pd.read_csv("raw_data/cps.csv", iterator=True, index_col=[0])
df = textfilereader.get_chunk(5000)

# descobrindo colunas com apenas Nas
percent_missing = df.isnull().sum() * 100 / len(df)
missing_value_df = pd.DataFrame({'column_name': df.columns, 'percent_missing': percent_missing})
missing_value_df = missing_value_df[missing_value_df["percent_missing"]==100]
missing_cols = list(missing_value_df["column_name"])

# Removendo anos indesejados
anos = list(range(2000, 2016))
dask_df = dd.read_csv("raw_data/cps.csv", assume_missing=True)
dask_df = dask_df[dask_df.YEAR.isin(anos)]

# Removendo colunas com apenas Nas
dask_df = dask_df.drop(missing_cols, axis=1)

# Corrigindo Income pela inflação
dask_df["HHINCOME"] = dask_df["HHINCOME"] * dask_df["CPI99"]
dask_df["FAMINC"] = dask_df["FAMINC"] * dask_df["CPI99"]

# Dando join com estado
dask_df = dd.merge(dask_df, state_fips, how="left", on="STATEFIP")

# Salvando dataframe
dask_df.to_csv("cleaned_data/cps_2000_2016_cleaned.csv", single_file=True, index=False)
