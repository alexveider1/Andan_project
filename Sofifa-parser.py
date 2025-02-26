import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import tqdm
import pandas as pd
import numpy
import bs4
import warnings
import json
warnings.filterwarnings("ignore")

from _funcs.parser import *

init()


file = open('FIFA\\params\\Players_url.json')
urls = json.load(file)
file.close()

file = open('FIFA\\params\\Players_ranges.json')
ranges = json.load(file)
file.close()

urls.reverse()
ranges.reverse()

players = {
    f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}



file = open('FIFA\\params\\Teams_url.json')
urls = json.load(file)
file.close()

file = open('FIFA\\params\\Teams_ranges.json')
ranges = json.load(file)

urls.reverse()
ranges.reverse()

teams = {f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}



file = open('FIFA\\params\\Leagues_url.json')
urls = json.load(file)
file.close()

file = open('FIFA\\params\\Leagues_ranges.json')
ranges = json.load(file)
file.close()

urls.reverse()
ranges.reverse()

leagues = {f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}



file = open('FIFA\\params\\National_url.json')
urls = json.load(file)
file.close()

file = open('FIFA\\params\\National_ranges.json')
ranges = json.load(file)
file.close()

urls.reverse()
ranges.reverse()

national = {f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}





def main():
    for game in teams:
        fetch_data_teams(game, teams)
    for game in leagues:
        fetch_data_leagues(game, leagues)
    for game in national:
        fetch_data_national(game, national)
    for game in players:
        fetch_data_players(game, players)


main()
