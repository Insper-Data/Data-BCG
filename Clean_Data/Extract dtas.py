import os
import tkinter as tk
from tkinter import filedialog
import re

def get_filepath(message):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=message)

dtas_path = get_filepath("Selecione a pasta que contém as bases desejadas")
end_path = get_filepath("Selecione a pasta para a qual as bases serão transferidas")

for pasta in os.listdir(dtas_path):
    stata_path = os.path.join(dtas_path, str(pasta), "DS0001")
    dir_files = os.listdir(stata_path)
    stata_name = [file for file in dir_files if re.match(".*dta$", file)][0]
    file_wd = os.path.join(stata_path, stata_name)

    file_name = os.path.basename(file_wd)

    os.rename(file_wd, os.path.join(end_path, file_name))