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
downloads = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Downloads")
os.chdir(downloads)


file = open('data\\Players_url.json')
urls = json.load(file)
file.close()

file = open('data\\Players_ranges.json')
ranges = json.load(file)
file.close()

urls.reverse()
ranges.reverse()

players = {
    f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}



file = open('data\\Teams_url.json')
urls = json.load(file)
file.close()

file = open('data\\Teams_ranges.json')
ranges = json.load(file)

urls.reverse()
ranges.reverse()

teams = {f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}



file = open('data\\Leagues_url.json')
urls = json.load(file)
file.close()

file = open('data\\Leagues_ranges.json')
ranges = json.load(file)
file.close()

urls.reverse()
ranges.reverse()

leagues = {f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}



file = open('data\\National_url.json')
urls = json.load(file)
file.close()

file = open('data\\National_ranges.json')
ranges = json.load(file)
file.close()

urls.reverse()
ranges.reverse()

national = {f'FIFA{i}': (j, k) for i, j, k in 
    zip(range(7, 24 + 1), ranges, urls)
}



def init():
    try:
        os.mkdir('FIFA')
        os.chdir('FIFA')
        os.mkdir('players')
        os.mkdir('teams')
        os.mkdir('leagues')
        os.mkdir('national')
    except FileExistsError:
        print("Путь уже существует")
    finally:
        os.chdir('FIFA')



def fetch_data_teams(game, data = teams, header=True):
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)
    for i in tqdm.tqdm(range(60, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")

        try:
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]


        data = driver.find_element(By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        countries, hrefs = [], []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            country = bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('img')['title']
            countries.append(country)
            hrefs.append(href)

        table['href'] = hrefs
        table['country'] = countries
        
        table.to_csv(f"teams\\Teams-{game}.csv", index=False, mode='a', header=header)
        header = False
        sleep(10)



def fetch_data_leagues(game, data=leagues, header=True):
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)
    for i in tqdm.tqdm(range(60, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")

        try:
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        data = driver.find_element(By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        countries, hrefs = [], []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            country = bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('img')['title']
            countries.append(country)
            hrefs.append(href)

        table['href'] = hrefs
        table['country'] = countries
        
        table.to_csv(f"leagues\\Leagues-{game}.csv", index=False, mode='a', header=header)
        header = False
        sleep(10)



def fetch_data_national(game, data=national, header=True):
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)
    for i in tqdm.tqdm(range(60, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        try:
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        data = driver.find_element(By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        hrefs = []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            hrefs.append(href)

        table['href'] = hrefs
        
        table.to_csv(f"national\\National-{game}.csv", index=False, mode='a', header=header)
        header = False
        sleep(10)



def fetch_data_players(game, data = players, header=True):
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)
    
    for i in tqdm.tqdm(range(60, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]


        try:
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        data = driver.find_element(By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        countries, hrefs = [], []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            country = bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('img')['title']
            countries.append(country)
            hrefs.append(href)

        table['href'] = hrefs
        table['country'] = countries
        
        table.to_csv(f"players\\Players-{game}.csv", index=False, mode='a', header=header)
        header = False
        sleep(10)
    


def main():
    init()
    for game in teams:
        fetch_data_teams(game)
    for game in leagues:
        fetch_data_leagues(game)
    for game in national:
        fetch_data_national(game)
    for game in players:
            fetch_data_players(game)



main()
