import os
import sys
from time import sleep
import tqdm
import pandas as pd
import numpy
import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
"""
Модуль для парсинга данных с сайта `https://sofifa.com/` с помощью библиотек `Selenium` и `bs4`. 
"""


def init():
    """
    Функция для инициализации парсера и создания необходимых папок для данных, полученных с сайта `https://sofifa.com/`. Создает папки `players`, `teams`, `leagues`, `national` в рабочей директории. 
    """
    try:
        os.mkdir('players')
        os.mkdir('teams')
        os.mkdir('leagues')
        os.mkdir('national')
    except FileExistsError:
        print("Путь уже существует")


def fetch_data_teams(game: str, data: dict, header=True) -> None:
    """
    Функция для сбора данных о футбольных клубах с сайта `https://sofifa.com/`. Параметр `game` обозначает игру (например, `FIFA20`), которая является ключом в словаре `data`. Параметр `data` - это словарь, у которого ключами являются названия игр вида `FIFA20`, а значениями - кортежи с максимальным количеством команд, доступных на сайте для данной игры (это число, кратное 60 - показывающее максимальное количество объектов на веб-странице для данной `game`), и ссылкой для данной `game`. Функция записывает в файл "FIFA\\teams\\Teams-{game}.csv" (в режиме `append`) данные, полученные с веб-страницы. 
    """
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)
    for i in tqdm.tqdm(range(0, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
            sleep(10)
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")

        try:
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        data = driver.find_element(
            By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        countries, hrefs = [], []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(
                By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            country = bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[
                                        1].get_attribute('outerHTML')).find('img')['title']
            countries.append(country)
            hrefs.append(href)

        table['href'] = hrefs
        table['country'] = countries

        table.to_csv(
            f"FIFA\\teams\\Teams-{game}.csv", index=False, mode='a', header=header)
        header = False
    driver.close()


def fetch_data_leagues(game: str, data: dict, header=True) -> None:
    """
    Функция для сбора данных о футбольных лигах с сайта `https://sofifa.com/`. Параметр `game` обозначает игру (например, `FIFA20`), которая является ключом в словаре `data`. Параметр `data` - это словарь, у которого ключами являются названия игр вида `FIFA20`, а значениями - кортежи с максимальным количеством лиг, доступных на сайте для данной игры (это число, кратное 60 - показывающее максимальное количество объектов на веб-странице для данной `game`), и ссылкой для данной `game`. Функция записывает в файл "FIFA\\leagues\\Leagues-{game}.csv" (в режиме `append`) данные, полученные с веб-страницы. 
    """
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)
    for i in tqdm.tqdm(range(0, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
            sleep(10)
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")

        try:
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        data = driver.find_element(
            By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        countries, hrefs = [], []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(
                By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            country = bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[
                                        1].get_attribute('outerHTML')).find('img')['title']
            countries.append(country)
            hrefs.append(href)

        table['href'] = hrefs
        table['country'] = countries

        table.to_csv(f"FIFA\leagues\\Leagues.csv",
                     index=False, mode='a', header=header)
        header = False
    driver.close()


def fetch_data_national(game: str, data: dict, header=True) -> None:
    """
    Функция для сбора данных о национальных сборных с сайта `https://sofifa.com/`. Параметр `game` обозначает игру (например, `FIFA20`), которая является ключом в словаре `data`. Параметр `data` - это словарь, у которого ключами являются названия игр вида `FIFA20`, а значениями - кортежи с максимальным количеством национальных сборных, доступных на сайте для данной игры (это число, кратное 60 - показывающее максимальное количество объектов на веб-странице для данной `game`), и ссылкой для данной `game`. Функция записывает в файл "FIFA\\national\\National-{game}.csv" (в режиме `append`) данные, полученные с веб-страницы. 
    """
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)
    for i in tqdm.tqdm(range(0, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
            sleep(10)
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        try:
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        data = driver.find_element(
            By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        hrefs = []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(
                By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            hrefs.append(href)

        table['href'] = hrefs

        table.to_csv(
            f"FIFA\\national\\National-{game}.csv", index=False, mode='a', header=header)
        header = False
    driver.close()


def fetch_data_players(game, data, header=True):
    """
    Функция для сбора данных о футбольных игроках с сайта `https://sofifa.com/`. Параметр `game` обозначает игру (например, `FIFA20`), которая является ключом в словаре `data`. Параметр `data` - это словарь, у которого ключами являются названия игр вида `FIFA20`, а значениями - кортежи с максимальным количеством игроков, доступных на сайте для данной игры (это число, кратное 60 - показывающее максимальное количество объектов на веб-странице для данной `game`), и ссылкой для данной `game`. Функция записывает в файл "FIFA\\players\\Players-{game}.csv" (в режиме `append`) данные, полученные с веб-страницы. 
    """
    page = data[game][0]
    url = data[game][1]
    options = webdriver.EdgeOptions()
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Edge(options)

    for i in tqdm.tqdm(range(0, page + 60, 60)):
        try:
            driver.get(f"{url}{i}")
            sleep(10)
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            driver.get(f"{url}{i}")
        except TimeoutException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except:
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        try:
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]
        except NoSuchElementException as er:
            print(er)
            sleep(60)
            driver.refresh()
            table = driver.find_element(
                By.CSS_SELECTOR, 'article').get_attribute('outerHTML')
            table = pd.read_html(table)[0]

        data = driver.find_element(
            By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')
        countries, hrefs = [], []
        for el in range(len(data)):
            href = 'https://sofifa.com' + bs4.BeautifulSoup(data[el].find_elements(
                By.CSS_SELECTOR, 'td')[1].get_attribute('outerHTML')).find('a')['href']
            country = bs4.BeautifulSoup(data[el].find_elements(By.CSS_SELECTOR, 'td')[
                                        1].get_attribute('outerHTML')).find('img')['title']
            countries.append(country)
            hrefs.append(href)

        table['href'] = hrefs
        table['country'] = countries

        table.to_csv(
            f"FIFA\\players\\Players-{game}.csv", index=False, mode='a', header=header)
        header = False
    driver.close()
