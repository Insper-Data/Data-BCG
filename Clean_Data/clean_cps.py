import pandas as pd
import os
# Para carregar um dataframe tão grande devemos utilizar o a capacidade
# de processamento paralelo do computador. Para isso podemos utilizar
# o pacote Dask que implementa essa funcionalidade utilizando a mesma
# sintaxe do Pandas. Para instalar deve se utilizar "pip3 install dask[complete]"
from dask import dataframe as dd

# Configurando path do projeto
cwd = os.getcwd()
project_wd = os.path.dirname(cwd)

# Setting up pandas parameters
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 100)

# Lendo códigos Fips dos estados
state_fips_wd = os.path.join(project_wd, "Download_Data/Data/fips_state.csv")
state_fips = pd.read_csv(state_fips_wd)
state_fips.drop(columns="state", inplace=True)
state_fips.rename(columns={"fips_code": "STATEFIP", "post_code": "state"}, inplace=True)

# Criando dataframe em branco para armazenar resultados
df_final = pd.DataFrame()
df_final = dd.from_pandas(df_final, npartitions=100)

# Armazenando número do chunk
n_chunk = 1

# Loop para processar chunks
for chunk in pd.read_csv("raw_data/cps.csv", chunksize=100000):
    if n_chunk <= 68:
        df_i = chunk

        # Removing columns with unwanted variables
        df_i.drop(columns=["ASECWTH", "MISH", "NUMPREC", "METAREA", "ASECFLAG", "REGION", "HEATSUB", "HEATVAL"], inplace=True)

        # Removing columns without data
        df_i.dropna(axis=1, inplace=True)

        # Deixando colunas de household income e family income em dólares de 1999
        df_i["HHINCOME"] = df_i["HHINCOME"] * df_i["CPI99"]
        df_i["FAMINC"] = df_i["FAMINC"] * df_i["CPI99"]

        # Removendo multiplicador da inflação
        df_i.drop(columns="CPI99", axis=1, inplace=True)

        # Juntando códigos dos estados com o dataframe do cps
        df_i = df_i.merge(state_fips, how="left", on="STATEFIP")
        df_final = df_final.append(df_i)
        print("Chunk {} out of {} succesfully processed!".format(n_chunk, 98))
        n_chunk += 1
    else:
        break

df_final.to_csv("cleaned_data/cleaned_cps.csv", single_file=True)