from typing import Optional, AnyStr, Any
import urllib3
import json

import lxml
from lxml import html
from bs4 import BeautifulSoup
import httpx
from fastapi import FastAPI





""" DATA RETRIEVAL
"""

global switch
switch = {
        "XCD": "https://www.eccb-centralbank.org/",
        "BSD": "https://www.centralbankbahamas.com/exchange_rates.php",
        "BBD": "http://www.centralbank.org.bb/",
        "JMD": "https://boj.org.jm/",
        "TTD": "https://www.central-bank.org.tt/",
        "BZD": "https://www.centralbank.org.bz/",
        "HTG": "http://www.mef.gouv.ht/index.php?page=Accueil",
        "SRD": "https://www.centralbank.org.bz/",
        "BMD": "https://www.exchangerates.org.uk/Bermuda-Dollar-BMD-currency-table.html",
        "KYD": "https://www.exchangerates.org.uk/Cayman-Islands-Dollar-KYD-currency-table.html"
    }

def fetch_from(pair: str):
    doc = httpx.get(switch[pair]).text
    soup = BeautifulSoup(doc, 'html5lib')

    if pair == "XCD":
        rates = soup.select("div.rate-list:nth-child(18) > div:nth-child(2)")
        quote = rates[0].string

    if pair == "BSD":
        rates = soup.select("ul.d-flex > li:nth-child(2) > div:nth-child(2) > span:nth-child(1)")
        quote = rates[0].string

    if pair == "BBD":
        rates = soup.select("#exchange_rate_notes > div:nth-child(4) > div:nth-child(2)")
        quote = rates[0].string

    if pair == "JMD":
        rates = soup.find(id="tablepress-1")
        rates = rates.find("tr", "row-2 even")
        rate = rates.find("td", "column-3")
        quote = rate.string

    if pair == "TTD":
        rates = soup.select(".borderless_tr > td:nth-child(1)")
        rate = str(rates[0].encode("utf-8"))

        quote_start = rate.find("</p>") + 4
        quote_end = quote_start + rate[quote_start:].find("<")
        quote = rate[quote_start:quote_end]

    if pair == "BZD":
        rates = soup.select("#currency-notes > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)")
        quote = rates[0].string

    if pair == "HTG":
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://www.mef.gouv.ht/index.php?page=Accueil')
        data_string = r.data.decode('utf-8', errors='ignore')
        tree = html.fromstring(data_string)
        quote = tree.xpath(
            '//table[@style="border-collapse:collapse; width:100%;height:75px; margin-top:50px; margin-bottom:30px; border-color: #CCC; margin-right:2px;"]//tr[3]//td[2]/text()')
        quote = quote[0]
    
    if pair == "SRD":
        rates = soup.select("#currency-notes > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)")
        quote = rates[0].string
    
    if pair == "BMD":
        rates = soup.select("tr.coltwo:nth-child(13) > td:nth-child(4) > strong:nth-child(1)")
        quote = rates[0].string

    if pair == "KYD":
        rates = soup.select("tr.coltwo:nth-child(13) > td:nth-child(4) > strong:nth-child(1)")
        quote = rates[0].string
    
    return(format(float(quote), '.5f'))

""" API ROUTES
"""

app = FastAPI(title="OneSea API", description="API serving exotic Forex trading pairs from the Caribbean region")

@app.get("/")
def root():
    return{"status": "Healthy"}

@app.get("/{pair}")
def getPair(pair: str):
    pair = pair.upper()
    return {
        "pair": f"{pair}/USD",
        "value": fetch_from(pair)
    }

""" TESTING
"""
if __name__ == "__main__":
    print(fetch_from("HTG"))
