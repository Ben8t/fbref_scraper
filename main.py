import argparse
from lxml import etree, html
import pandas as pd
import re
import requests

from utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse fbref /matchs page")
    parser.add_argument("--date", help="The match date")
    args = parser.parse_args()

    if not is_date_format(args.date):
        raise Exception(f"The --date parameter '{args.date}' is not in 'yyyy-mm-dd' format")
    
    # date = "2023-01-03"
    date = args.date
    

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
