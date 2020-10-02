import os
import tkinter as tk
from tkinter import filedialog
from siuba import *
import re
import pandas as pd

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
             select(_["ORI", "YEAR", "MSA",
                    "SEQNO", "SUB", "CORE",
                   "OFFENSE":"JN", "ZERO"]) >>
             filter(_.ZERO == "Not used") >>
             select(-_.ZERO))

            db = db.append(df)

        filename = db.YEAR.iloc[0]
        db.to_csv(os.path.join(db_path, str(filename) + ".csv"))
        os.remove(file_wd)

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