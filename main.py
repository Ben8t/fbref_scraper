import argparse
from lxml import etree, html
import pandas as pd
import re
import requests

from utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse fbref /matchs page")
    parser.add_argument("--date", help="The match date")
    parser.add_argument("--page", help="matchs/ or fixtures/")
    parser.add_argument("--fixture_url", help="fixture url")
    args = parser.parse_args()

    if not is_date_format(args.date):
        raise Exception(f"The --date parameter '{args.date}' is not in 'yyyy-mm-dd' format")
    
    # date = "2023-01-03"
    date = args.date
    
    if args.page == "matchs/":

        url = f"https://fbref.com/en/matchs/{date}"

        response = requests.get(url)
        tree = html.fromstring(response.content)
        items = tree.xpath('//div[@class="table_wrapper tabbed"]')

        results = []
        for item in items:
            league = item.find("span").text.replace('"','').replace('>','')
            table = etree.fromstring(etree.tostring(item)).xpath("//table")[0]
            df = pd.read_html(etree.tostring(table))[0].assign(league=league, date=date)
            results.append(df)

        final_data = snake_case_column_names(pd.concat(results))
        final_data.to_csv(f"data/matchs_{date.replace('-','')}.csv", index=False)

    if args.page == "fixtures/" and args.fixture_url is not None:
        url = args.fixture_url
        response = requests.get(url)
        tree = html.fromstring(response.content)
        league = url.split("/")[-1].replace("-Scores-and-Fixtures","").replace("-"," ")
        table = etree.fromstring(etree.tostring(tree.xpath('//*[@class="table_wrapper tabbed"]')[0])).xpath("//table")[0]
        final_data = pd.read_html(etree.tostring(table))[0].assign(league=league)
        final_data = snake_case_column_names(final_data)
        final_data.to_csv(f'data/fixtures_{league.lower().replace(" ","_")}.csv', index=False)