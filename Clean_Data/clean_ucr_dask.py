import pandas as pd
import ssl
import os

from dask import dataframe as dd
from dask.diagnostics import ProgressBar

# Disabling ssl verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Reading agencys and fips_data dataframes
agencies_data = pd.read_csv("https://raw.githubusercontent.com/jacobkap/crimedatatool_helper/master/data/crosswalk.csv")
fips_data = pd.read_csv("https://raw.githubusercontent.com/Insper-Data/Data_BCG/master/Download_Data/Data/fips_data.csv")

# Creating geographic infos dataframe
agencies_data = agencies_data.drop_duplicates(subset="fips_state_county_code")
agencies_data = agencies_data[~agencies_data["fips_state_county_code"].str.contains("20NA")]
agencies_data["fips_state_county_code"] = agencies_data["fips_state_county_code"].astype(int)

fips_data = fips_data.drop_duplicates(subset="county_fips")

geo_df = pd.merge(agencies_data, fips_data, how="inner", left_on="fips_state_county_code", right_on="county_fips")
geo_df = geo_df[["ori", "city_ascii", "county_name", "county_fips", "metfips"]]


# # Checking dataframe by chunk
# textfilereader = pd.read_csv("raw_data/2000.csv", iterator=True)
# df = textfilereader.get_chunk(5000)
# df = df.drop(axis=1, columns=["Unnamed: 0", "Unnamed: 0.1"])

# Dask progress bar
ProgressBar().register()


years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]

for year in years:

    # Reading crime dataframes
    df = dd.read_csv("raw_data/{}.csv".format(year), assume_missing=True, dtype=object)

    # Clean Arrests
    df = df[["ORI", "YEAR", "SUB", "OFFENSE", "OCCUR", "M0_9", "M10_12", "M13_14", "M15", "M16",
             "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "M25_29", "M30_34", "M35_39", "M40_44",
             "M45_49", "M50_54", "M55_59", "M60_64", "M65", "F0_9", "F10_12", "F13_14", "F15", "F16",
             "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24", "F25_29", "F30_34", "F35_39", "F40_44",
             "F45_49", "F50_54", "F55_59", "F60_64", "F65", "AW", "AB", "AI", "AA", "JW", "JB", "JI", "JA", "AH", "AN", "JH", "JN"]]

    df = dd.merge(df, geo_df, how="inner", left_on="ORI", right_on="ori")
    df = df.drop(["ORI", "ori"], axis=1)
    df_final = df.compute()
    df_final.dropna(subset=["metfips"])
    city = df_final.pop("city_ascii")
    df_final.insert(1, "city_ascii", city)
    df_final.to_csv("cleaned_data/{}_cleaned.csv".format(year))
    print("year {} done!".format(year))
