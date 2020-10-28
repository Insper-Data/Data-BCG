import os
import tkinter as tk
from tkinter import filedialog
from siuba import *
import re
import pandas as pd

agencies_data = pd.read_csv("https://raw.githubusercontent.com/jacobkap/crimedatatool_helper/master/data/crosswalk.csv")
agencies_data = (agencies_data >>
                 select(_.ori, _.fips_state_county_code) >>
                 mutate(fips_state_county_code = _.fips_state_county_code.astype(str)))
fips_data = pd.read_csv("https://raw.githubusercontent.com/Insper-Data/Data_BCG/master/Download_Data/Data/fips_data.csv")
fips_data = (fips_data >>
             select(_.county_fips, _.metfips) >>
             mutate(county_fips = _.county_fips.astype(str)))

######## Getting File Directory
def get_filepath(message):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=message)

def clean_arrests():
    db_path = get_filepath("Selecione a pasta que contém as bases desejadas")
    files = [file for file in os.listdir(db_path) if re.match(".*dta$", file)]

    for pasta in files:

        print("Carregando pasta " + pasta)

        file_wd = os.path.join(db_path, pasta)

        data = pd.read_stata(file_wd, chunksize=100000)

        db = pd.DataFrame()

        for df in data:

            df = (df >>
             select(_["ORI", "YEAR", "SUB",
                   "OFFENSE":"JN", "ZERO"]) >>
             filter(_.ZERO == "Not used") >>
             select(-_.ZERO))

            df = df.merge(agencies_data, how="inner", left_on="ORI", right_on="ori")
            df = df.merge(fips_data, how="inner", left_on="fips_state_county_code", right_on="county_fips")
            df = df.drop(columns=["ORI", "ori", "fips_state_county_code", "county_fips"])

            db = db.append(df)

        filename = db.YEAR.iloc[0]
        db.to_csv(os.path.join(db_path, str(filename) + ".csv"))

def clean_offenses():
    db_path = get_filepath("Selecione a pasta que contém as bases desejadas")
    files = [file for file in os.listdir(db_path) if re.match(".*dta$", file)]

    for pasta in files:

        print("Carregando pasta " + pasta)

        file_wd = os.path.join(db_path, pasta)

        data = pd.read_stata(file_wd, chunksize=10000)

        db = pd.DataFrame()

        for df in data:

            db = db.append(df)

        filename = db.V6.iloc[0]
        db.to_csv(os.path.join(db_path, str(filename) + ".csv"))
        os.remove(file_wd)

def clean_homicides():
    db_path = get_filepath("Selecione a pasta que contém as bases desejadas")
    files = [file for file in os.listdir(db_path) if re.match(".*dta$", file)]

    for pasta in files:

        print("Carregando pasta " + pasta)

        file_wd = os.path.join(db_path, pasta)

        data = pd.read_stata(file_wd, chunksize=10000)

        db = pd.DataFrame()

        for df in data:

            db = db.append(df)

        filename = db.V6.iloc[0]
        db.to_csv(os.path.join(db_path, str(filename) + ".csv"))
        os.remove(file_wd)

def clean_police():
    db_path = get_filepath("Selecione a pasta que contém as bases desejadas")
    files = [file for file in os.listdir(db_path) if re.match(".*dta$", file)]

    for pasta in files:

        print("Carregando pasta " + pasta)

        file_wd = os.path.join(db_path, pasta)

        data = pd.read_stata(file_wd, chunksize=10000)

        db = pd.DataFrame()

        for df in data:

            db = db.append(df)

        filename = db.V6.iloc[0]
        db.to_csv(os.path.join(db_path, str(filename) + ".csv"))
        os.remove(file_wd)
