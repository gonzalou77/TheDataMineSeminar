"""
Module for TDM 30100 project 6.
"""

import pandas as pd
from pathlib import Path
import os
import pandas as pd
import plotly.express as px
import requests
import lxml.html
from fuzzywuzzy import fuzz


def find_longest_timegap(datetime_series: pd.Series) -> float:
    """
    Given a `pandas` series, output the largest time gap between 
    consecutive datetimes, in hours.
    """
    # convert column to datetime
    datetime_series = pd.to_datetime(datetime_series)
    
    # sort from least recent to most recent
    datetime_series = datetime_series.sort_values(ascending=True)
    
    # create series of consecutive time differences
    time_diff = (datetime_series.diff(-1).dt.total_seconds().abs().max()) / 3600
    return time_diff

    
def space_in_dir(directory: str) -> None:
    """
    Given a directory, return the amount of space the files in the directory,
    recursively, take up.
    """
    root_directory = Path(directory)
    root_sum = (sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()))
    return root_sum
    
    

def event_plotter(event: str) -> pd.DataFrame:
    """
    Given the name of an event, create a plot for each of the Gold, Silver, and Bronze medals.
    The plots contain the count of the type of medal on the y-axis, the country on the x-axis
    and the average age in text on each bar.
    
    Plots should be output in Jupyter, as well as saved to the executor's $HOME directory as
    bronze.jpeg, silver.jpeg, and gold.jpeg. The dataframe with the data should be returned.
    """
    dat = pd.read_csv("/anvil/projects/tdm/data/olympics/athlete_events.csv")
    dat = dat.loc[dat['Event'] == event,]
    dat = dat.loc[dat['Medal'].notna(), ]
    counts = dat.groupby(["Medal", "NOC"]).count()['ID'].reset_index()
    dat = dat.groupby(["Medal", "NOC"]).mean()['Age'].reset_index()
    dat = pd.merge(dat, counts, how="inner", on=['Medal', 'NOC'])
    dat.rename(columns={"ID":"Count"}, inplace=True)
    gold = px.bar(dat.loc[dat['Medal']=="Gold",], x='NOC', y='Count', text="Age", title="Gold")
    gold.write_image(f"{os.getenv('HOME')}/gold.jpeg")
    silver = px.bar(dat.loc[dat['Medal']=="Silver",], x='NOC', y='Count', text="Age", title="Silver")
    silver.write_image(f"{os.getenv('HOME')}/silver.jpeg")
    bronze = px.bar(dat.loc[dat['Medal']=="Bronze",], x='NOC', y='Count', text="Age", title="Bronze")
    bronze.write_image(f"{os.getenv('HOME')}/bronze.jpeg")
    
    gold.show()
    silver.show()
    bronze.show()
    return dat


def player_info(name: str) -> str:
    """
    Given the name of a soccer player, `player_info` 
    will scrape fbref.com and present some statistics.
    """
    result = ""
    
    # get first two letters of last name
    last_last_name = name.split(" ")[len(name.split(" "))-1]
    players_page = f'https://fbref.com/en/players/{last_last_name[0:2]}/'
    resp = requests.get(players_page)
    if resp.status_code != 200:
        raise ValueError(f"Failed to scrape {players_page}")
    
    tree = lxml.html.fromstring(resp.text)
    elements = tree.xpath("//div[starts-with(@id, 'all_')]/div[@class='section_content']/p/a")
    for e in elements:
        if fuzz.ratio(name.lower(), e.get("href").split("/")[-1].replace("-", " ").lower()) > 90:
            player_url = f'https://fbref.com/en/players/{e.get("href").split("/")[-2]}/'
            
    if not player_url:
        raise ValueError(f"Could not find player {name}.")
        
    player = lxml.html.fromstring(requests.get(player_url).text)
    
    # get the actual player name
    name = player.xpath("//div[@id='info']/div[@id='meta']//h1/span")[0].text
    result+=f"Name: {name}\n"
    
    # get the birthday
    bday = player.xpath("//div[@id='info']/div[@id='meta']//span[@data-birth]")[0].text.strip()
    result+=f"Birthday: {bday}\n"
    
    # get total points
    gls = player.xpath("//table[@id='stats_standard_dom_lg']//tr[@id='stats']/td[@data-stat='goals']")
    total = 0
    for g in gls:
        total += int(g.text)
    result+=f"Total goals: {total}"
        
    return result