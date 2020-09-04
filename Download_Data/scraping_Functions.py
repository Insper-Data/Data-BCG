import requests
import pandas as pd
import countries_and_states
import lxml
from bs4 import BeautifulSoup

def get_season_data(year):

    url_data = requests.get("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)).text
    soup_season= BeautifulSoup(url_data, "lxml")
    header = [th.get_text() for th in soup_season.findAll("tr")[0].findAll("th")]
    header = header[1:]
    rows = soup_season.findAll("tr")[1:]
    player_stats = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
    stats = pd.DataFrame(player_stats, columns=header)
    stats.dropna(inplace=True)
    return stats


def get_birthplaces(all_countries=True):

    df = pd.DataFrame()

    for country in countries_and_states.countries.Code:
        if country == "US":
            for state in countries_and_states.us_states.Code:
                try:
                    url_data = requests.get("https://www.basketball-reference.com/friv/birthplaces.fcgi?country={}&state={}".format(country, state)).text
                    soup = BeautifulSoup(url_data, "lxml")
                    rows = soup.findAll("tr")[1:]
                    player_birthplace = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
                    df_i = pd.DataFrame(player_birthplace)
                    df_i = df_i[[0, 28]].rename(columns={0: "Player", 28: "Birthplace"})
                    df_i.dropna(inplace=True)
                    df = df.append(df_i)
                    print("{}, {}, succesful".format(country, state))
                except:
                    print("there was a problem or no players for {}".format(state))
        else:
            if all_countries:
                try:
                    url_data = requests.get("https://www.basketball-reference.com/friv/birthplaces.fcgi?country={}&state=".format(country)).text
                    soup = BeautifulSoup(url_data, "lxml")
                    rows = soup.findAll("tr")[1:]
                    player_birthplace = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
                    df_i = pd.DataFrame(player_birthplace)
                    df_i = df_i[[0, 28]].rename(columns={0: "Player", 28: "Birthplace"})
                    df_i.dropna(inplace=True)
                    df = df.append(df_i)
                    print("{}, succesful".format(country))
                except:
                    print("there was a problem or no players for {}".format(country))
    return df

