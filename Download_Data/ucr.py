from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time
import os
import tkinter as tk
from tkinter import filedialog

def get_filepath(message):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=message)

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

def crawler(link, download_wd):

    regex = re.compile(".*\.crdownload$")

    if not isinstance(link, str):
        return "Inserted link should be a string"

    class download_ucr_data():
        def __init__(self, link):
            self.driver = webdriver.Chrome()
            self.link = link

        def enter_page(self):
            # Open webpage
            self.driver.get(self.link)

        def click_download(self):
            # Click download button
            download_button = self.driver.find_element_by_xpath('//*[@id="quickDownload"]/div/button')
            download_button.click()
            self.driver.execute_script("window.scrollTo(0, 200)")

        def click_stata(self):
            # Click Stata button
            stata_button = self.driver.find_element_by_xpath('//*[@id="quickDownload"]/div/ul/li[4]/a')
            stata_button.click()

        def agree(self):
            # Agree terms and conditions
            agree_button = self.driver.find_element_by_xpath('//*[@id="termsOfUseModalWrapper"]/div/div/div[3]/a[1]')
            agree_button.click()

        def login(self):
            # Log into account
            email_input = self.driver.find_element_by_xpath('//*[@id="email"]')
            password_input = bot.driver.find_element_by_xpath('//*[@id="password"]')

            email_input.send_keys('gustavobsales@gmail.com')
            password_input.send_keys('wKqyAc5MchiihLEhE99r')

            log_in_button = self.driver.find_element_by_xpath('//*[@id="mainContent"]/div[1]/div[1]/form/input[4]')
            log_in_button.click()

        def close(self):
            # Close Chrome
            self.driver.close()

    size_downloads = len([files for files in os.listdir(download_wd) if not regex.match(files)])
    bot = download_ucr_data(link)
    bot.enter_page()
    bot.click_download()
    time.sleep(2)
    bot.click_stata()
    time.sleep(2)
    bot.agree()
    time.sleep(2)
    bot.login()

    while len([files for files in os.listdir(download_wd) if not regex.match(files)]) == size_downloads:
        time.sleep(3)

    bot.close()

def get_ucr_data(data_wanted="All"):
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
    download_wd = get_filepath("Selecione sua pasta de Downloads")

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
        [crawler(link, download_wd) for link in links.link.tolist()]
        return

    links = links[links.name == data_wanted]

    if data_wanted.lower() == "Arrests by Age, Sex, and Race, monthly reports".lower():
        [crawler(link, download_wd) for link in links.link.tolist()[19::]]
        return

    [crawler(link, download_wd) for link in links.link.tolist()]

    return