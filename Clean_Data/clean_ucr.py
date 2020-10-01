import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import re
from siuba import *

######## Getting File Directory
def get_filepath(message):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=message)

db_path = get_filepath("Selecione a pasta que contém a base desejada")

for year in os.listdir(db_path):

    stata_path = os.path.join(db_path, str(year), "DS0001")
    dir_files = os.listdir(stata_path)
    stata_name = [file for file in dir_files if re.match(".*dta$", file)][0]
    file_wd = os.path.join(stata_path, stata_name)

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

    db.to_csv(os.path.join(db_path, str(year) + ".csv"))