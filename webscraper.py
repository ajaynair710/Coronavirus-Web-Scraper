import requests
import pandas
import time
import numpy as np
from bs4 import BeautifulSoup
from datetime import date
import schedule
import os
from os import environ
from secrets import *



def data_interval():
    #Use today's data to determine interval
    URL = 'https://www.worldometers.info/coronavirus/#countries'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Isolate table data showing covid19 data per country
    results = soup.find(id="main_table_countries_today")
    content = results.find_all('td')

    # convert data to a list
    data = []
    for item in content:
        data.append(item.text.strip())
        # print(item.text)

    # Determine interval when new row in table starts
    interval = data.index("USA") - data.index("World")
    print(f"Interval is {interval}")

    return interval

def scrape_table(table_ID):
    #Retrieve website HTML
    URL = 'https://www.worldometers.info/coronavirus/#countries'
    html_of_page = requests.get(URL)
    soup = BeautifulSoup(html_of_page.content, 'html.parser')

    #Isolate table data showing covid19 data per country
    table_container = soup.find(id=table_ID)
    table_content = table_container.find_all('td')

    #convert data to a list
    table_data = []
    for item in table_content:
        table_data.append(item.text.strip())

    #determine interval when new line in table starts
    interval = data_interval()

    #Populate lists for dictionary
    countries = table_data[::interval]
    total_cases = table_data[1::interval]
    new_cases = table_data[2::interval]
    total_deaths = table_data[3::interval]
    new_deaths = table_data[4::interval]

    #Add lists to covid19_table dictionary
    column_names = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths"]
    covid19_table = {
        "columns": column_names,
        "country": countries,
        "total_cases": total_cases,
        "new_cases": new_cases,
        "total_deaths": total_deaths,
        "new_deaths": new_deaths
        }
    return covid19_table

def Growth_factor(growth_today, growth_yesterday):
    #Gf = new cases for today / new cases for yesterday
    # Gf = N_i/N_i-1
    print(growth_today)
    print(growth_yesterday)
    # Check if variables are not empty
    if growth_today:
        if growth_yesterday:
            Gf = round(float(growth_today)/float(growth_yesterday),2)
        else:
            Gf = 0
    else:
        Gf = 0

    return Gf

def dict_index(dict,search_term):
    #returns position of search term in given dictionary
    return dict["country"].index(search_term)

