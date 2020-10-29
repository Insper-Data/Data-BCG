import requests
import pandas as pd
import countries_and_states
from bs4 import BeautifulSoup
import re

def get_players_id():

    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
               "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    player_ids = pd.DataFrame()

    for letter in letters:
        url_data = requests.get("https://www.basketball-reference.com/players/{}/".format(letter)).text
        soup_id = BeautifulSoup(url_data, "lxml")
        rows = soup_id.findAll("tr")[1:]
        player_names_i = [row.findAll("th")[0].get_text() for row in rows]
        ids_i = [row.findAll("th")[0].attrs["data-append-csv"] for row in rows]
        dict_i = {"Player": player_names_i, "id": ids_i}
        df_i = pd.DataFrame(dict_i)
        player_ids = player_ids.append(df_i)

    return player_ids


def get_season_data(year):

    url_data = requests.get("https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)).text
    soup_season = BeautifulSoup(url_data, "lxml")
    header = [th.get_text() for th in soup_season.findAll("tr")[0].findAll("th")]
    header = header[1:]
    rows = soup_season.findAll("tr")[1:]
    player_stats = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
    stats = pd.DataFrame(player_stats, columns=header)
    stats.dropna(inplace=True)
    stats = stats.applymap(lambda x: pd.to_numeric(x, errors='ignore', downcast='float'))

    return stats


def get_game_data(year):

    ids_df = get_players_id()
    game_data_df = pd.DataFrame()
    iter = 1

    url_header = requests.get("https://www.basketball-reference.com/players/a/{}/gamelog/{}/".format("beshode01", 1980)).text
    soup_header = BeautifulSoup(url_header, "lxml")
    header = [th.get_text() for th in soup_header.findAll("tr")]
    header = header[9].split("\n")
    header.pop(0)
    header.pop(0)
    header.pop(4)
    header.pop(5)
    header.pop(26)
    header.insert(0, "id")

    for id in ids_df["id"]:

        url_data = requests.get("https://www.basketball-reference.com/players/a/{}/gamelog/{}/".format(id, year)).text
        soup_game = BeautifulSoup(url_data, "lxml")

        rows = soup_game.findAll("tr", id=lambda x: x and x.startswith("pgl_basic"))
        player_stats = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
        df_i = pd.DataFrame(columns=header)

        for lista in player_stats:
            lista.pop(4)
            lista.pop(5)
            lista.insert(0, id)
            stats_df = pd.DataFrame(lista).T
            stats_df.columns = header
            df_i = df_i.append(stats_df)

        game_data_df = game_data_df.append(df_i)
        print("id {}/{} done, ID = {}".format(iter, len(ids_df), id))
        iter += 1

    game_data_df = game_data_df.rename(str.lower(), axis = "columns")
    return game_data_df


def get_birthplaces(all_countries=True):

    df = pd.DataFrame()

    for country in countries_and_states.countries.Code:
        if country == "US":
            for state in countries_and_states.us_states.Code:
                try:
                    link_i = "https://www.basketball-reference.com/friv/birthplaces.fcgi?country={}&state={}".format(country, state)
                    url_data = requests.get("https://www.basketball-reference.com/friv/birthplaces.fcgi?country={}&state={}".format(country, state)).text
                    soup = BeautifulSoup(url_data, "lxml")
                    rows = soup.findAll("tr")[1:]
                    player_birthplace = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
                    df_i = pd.DataFrame(player_birthplace)
                    df_i = df_i[[0, 28]].rename(columns={0: "player", 28: "birthplace"})
                    df_i.dropna(inplace=True)
                    df_i.insert(1, "state", state)
                    df_i.insert(2, "country_iso2", country)
                    df = df.append(df_i)
                    print("{}, {}, succesful".format(country, state))
                except:
                    print("there was a problem or no players for {}".format(state))
        else:
            if all_countries:
                try:
                    link_i = "https://www.basketball-reference.com/friv/birthplaces.fcgi?country={}&state={}".format(country, state)
                    url_data = requests.get("https://www.basketball-reference.com/friv/birthplaces.fcgi?country={}&state=".format(country)).text
                    soup = BeautifulSoup(url_data, "lxml")
                    rows = soup.findAll("tr")[1:]
                    player_birthplace = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
                    df_i = pd.DataFrame(player_birthplace)
                    df_i = df_i[[0, 28]].rename(columns={0: "player", 28: "birthplace"})
                    df_i.dropna(inplace=True)
                    df_i.insert(1, "state", state)
                    df_i.insert(2, "country_iso2", country)
                    df = df.append(df_i)
                    print("{}, succesful".format(country))
                except:
                    print("there was a problem or no players for {}".format(country))
    return df


def get_high_school_cities():

    df = pd.DataFrame()

    for state in countries_and_states.us_states.Code:
        url_data = requests.get("https://www.basketball-reference.com/friv/high_schools.fcgi?state={}".format(state)).text
        soup = BeautifulSoup(url_data, "lxml")
        rows = soup.findAll("tr")[1:]
        player_school = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))]
        df_i = pd.DataFrame(player_school)
        df_i = df_i[[0, 2]].rename(columns={0: "player", 2: "hs_city"})
        df_i.dropna(inplace=True)
        df_i.insert(1, "state", state)
        df = df.append(df_i)
        print("{}, succesful".format(state))

    return df


def get_aggregated_season_data(initial_year=2010, final_year=2020):
    """
    Get season data from each player from several years
    """

    desired_years = range(initial_year, final_year + 1)

    columns = [x for x in list(get_season_data(2018).columns)]
    columns.append("GMSC")
    columns.append("YEAR")

    seasons_data = pd.DataFrame(columns=columns)

    for year in desired_years:

        print("Running year {}...".format(year))

        df = pd.DataFrame(get_season_data(year))

        df["GMSC"] = (df.PTS + 0.4 * df.FG - 0.7 * df.FGA -
                      0.4 * (df.FTA - df.FT) + 0.7 * df.ORB +
                      0.3 * df.DRB + df.STL + 0.7 * df.AST +
                      0.7 * df.BLK - 0.4 * df.PF - df.TOV)

        df["YEAR"] = year

        seasons_data = seasons_data.append(df)

    return seasons_data.rename(str.lower, axis = "columns")
