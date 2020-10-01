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

db_path = get_filepath("Selecione a pasta que contém as bases desejadas")

for pasta in os.listdir(db_path):

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

    filename = db.YEAR[0]
    db.to_csv(os.path.join(db_path, str(filename) + ".csv"))