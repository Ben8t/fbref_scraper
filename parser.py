from lxml import etree, html
import pandas as pd
import re
import requests
from utils import *

def match_parser(match_url: str) -> pd.DataFrame:
    response = requests.get(match_url)
    tree = html.fromstring(response.content)
    items = tree.xpath('//div[@class="table_wrapper tabbed"]')

    results = []
    for item in items:
        league = item.find("span").text.replace('"','').replace('>','')
        table = etree.fromstring(etree.tostring(item)).xpath("//table")[0]
        df = pd.read_html(etree.tostring(table))[0].assign(league=league, date=date)
        results.append(df)

    final_data = snake_case_column_names(pd.concat(results))
    return final_data


def fixture_parser(fixture_url: str) -> pd.DataFrame:
    response = requests.get(fixture_url)
    tree = html.fromstring(response.content)
    league = fixture_url.split("/")[-1].replace("-Scores-and-Fixtures","").replace("-"," ")
    table = etree.fromstring(etree.tostring(tree.xpath('//*[@class="table_wrapper tabbed"]')[0])).xpath("//table")[0]
    final_data = pd.read_html(etree.tostring(table))[0].assign(league=league)
    final_data = snake_case_column_names(final_data)
    return final_data, league