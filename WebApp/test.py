import urllib.request

import csv

from bs4 import BeautifulSoup

DOWNLOAD_URL = 'https://www.eia.gov/petroleum/gasdiesel/'

def download_page(url):
    return urllib.request.urlopen(url)

def getGas(html):
    

    soup = BeautifulSoup(html)
    gas_table_soup = soup.find('table', attrs={'class': 'simpletable'})

    for gas_row in gas_table_soup.find('tr')[3]:
        avg_gas = gas_row.find('td')[3].string
        print(avg_gas)

url = DOWNLOAD_URL
html = download_page(url)
print(getGas(html))