from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def change_names(name):
    if name == 0:
        return "Arrests by Age, Sex, and Race, monthly reports"
    elif name == 1:
        return "Offenses Known and Clearances by Arrest"
    elif name == 2:
        return "Property Stolen and Recovered"
    elif name == 3:
        return "Supplementary Homicide Reports"
    elif name == 4:
        return "Police Employee (LEOKA) Data"

def get_ucr_links(data_wanted="All"):
    """
    O texto inserido deve ser uma das seguintes strings:
            Arrests by Age, Sex, and Race, monthly reports \n
            Offenses Known and Clearances by Arrest \n
            Property Stolen and Recovered \n
            Supplementary Homicide Reports \n
            Police Employee (LEOKA) Data \n
            All
    """

    if not isinstance(data_wanted, str):
        return (print("O texto inserido deve ser uma das seguintes strings:\n \
        Arrests by Age, Sex, and Race, monthly reports\n \
        Offenses Known and Clearances by Arrest\n \
        Property Stolen and Recovered\n \
        Supplementary Homicide Reports\n \
        Police Employee (LEOKA) Data\n \
        All"))

    if data_wanted == "help":
        return (print("O texto inserido deve ser uma das seguintes strings:\n \
                Arrests by Age, Sex, and Race, monthly reports\n \
                Offenses Known and Clearances by Arrest\n \
                Property Stolen and Recovered\n \
                Supplementary Homicide Reports\n \
                Police Employee (LEOKA) Data\n \
                All"))

    url_data =  requests.get("https://www.icpsr.umich.edu/web/pages/NACJD/guides/ucr.html").text
    soup_season = BeautifulSoup(url_data, "lxml")
    linkloc = soup_season.findAll('a', attrs={'href': re.compile("^https?://")})
    links = pd.DataFrame(columns=["year", "link"])

    for link in linkloc:
        link_text = link.findAll(text=True)
        try:
            first_letter = list(link_text[0])[0]
            if first_letter == "1" or first_letter == "2":
                df = pd.DataFrame([[link_text[0], link.get("href")]],
                                  columns=["year", "link"])
                links = links.append(df)
        except:
            continue

    links["year_lag"] = links.year.shift(1)
    links["boolean"] = links.year > links.year.shift(1)

    ls = []
    i = -1

    for bool in links.boolean:
        if bool == True:
            ls.append(i)
        else:
            i += 1
            ls.append(i)

    links["name"] = ls
    links = links.drop(["year_lag", "boolean"], axis=1)
    links.name = links.name.apply(lambda x: change_names(x))

    if data_wanted.lower() == "all":
        return links

    links = links[links.name == data_wanted]

    return links

get_ucr_links("Supplementary Homicide Reports")
get_ucr_links()

# Login e senha do site do UCR
# gustavobsales@gmail.com
# wKqyAc5MchiihLEhE99r


