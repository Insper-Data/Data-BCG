import pandas as pd
import os

cwd = os.getcwd()
project_wd = os.path.dirname(cwd)
download_wd = os.path.join(project_wd, "Download_Data")
data_wd = os.path.join(download_wd, "Data")
countries_wd = os.path.join(data_wd, "all_Countries.csv")
us_states_wd = os.path.join(data_wd, "us_States.csv")
fips_states_wd = os.path.join(data_wd, "fips_state.csv")

countries = pd.read_csv(countries_wd)
us_states = pd.read_csv(us_states_wd)
state_codes = pd.read_csv(fips_states_wd)

