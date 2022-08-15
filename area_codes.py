#!/usr/bin/env python3
"""
Scrapes and formats (into dict) international country calling codes from Wikipedia
"""
import re

from bs4 import BeautifulSoup
import requests

URL = "https://en.wikipedia.org/wiki/List_of_country_calling_codes"

def get_codes() -> dict:
    """Fetch raw data from wikipeda then format using format_codes()"""
    html = requests.get(URL).content
    return format_codes(html)

def format_codes(html: str) -> dict:
    """Format <ul> containing phone codes from raw html into a dictionary"""
    soup = BeautifulSoup(html, "html.parser")

    li = soup.find_all("li")
    raw_codes = [x.text for x in li if re.search("^\+\d", x.text)]

    codes = {}

    #IMPORTANT: uses U+2013 ("–"), NOT U+002d ("-")
    for code in raw_codes:
        if "\n" in code:
            lines = [line.replace(":", "") for line in code.split("\n") if "–" in line]
            for line in lines:
                codes = add_code(line, codes)
        else:
            codes = add_code(code, codes)

    return codes

def add_code(code: str, codes: dict) -> dict:
    """Format and add code to the dictionary of codes"""
    parts = code.partition(" – ")
    num, area = parts[0].replace(" ", ""), parts[2].strip(" ") #U+00a0 (invisible space thing in strip() call)

    def keyadd(num, area, codes):
        if num in codes and codes[num] != area:
            codes[num] = f"{codes[num]}/{area}"
        else:
            codes[num] = area
        return codes

    if "/" in num:
        num = num.strip("+")
        variants = num.split("/")

        if len(variants[0]) > 3:
            prefix = f"+{variants[0][0]}"
            variants[0] = variants[0][-3:]
        else:
            prefix = "+"

        for v in variants:
            codes = keyadd(f"{prefix}{v}", area, codes)
    else:
        codes = keyadd(num, area, codes)

    return codes