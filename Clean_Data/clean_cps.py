import pandas as pd
import missingno as msn
import seaborn as sns

# Setting up pandas parameters
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 100)

# Importing dataframe
df_text_file_reader = pd.read_csv("raw_data/cps.csv", iterator=True)
df = df_text_file_reader.get_chunk(10000)

# Checking for null columns
missing_values = df.isnull().mean() * 100

# Removing columns without data
df.dropna(axis=1, inplace=True)

# Checking for null columns
missing_values = df.isnull().mean() * 100



