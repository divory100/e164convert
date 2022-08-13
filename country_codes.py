#!/usr/bin/env python3
"""
Scrapes and formats (into dict) international country calling codes from Wikipedia
"""
import re
import requests

from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_country_calling_codes"

def fetch_codes() -> dict:
    """Fetch raw data from wikipeda"""
    html = requests.get(URL).text
    return format_codes(html)

def format_codes(html: str) -> dict:
    """Format <ul> containing phone codes from raw html into a dictionary"""
    soup = BeautifulSoup(html, "html.parser")

    ul = soup.find_all("ul")
    li = [[x.text for x in list(l.descendants)] for l in ul]
    return li

if __name__ == "__main__":
    print(fetch_codes())