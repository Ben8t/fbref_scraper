import argparse
from lxml import etree, html
import pandas as pd
import re
import requests
from parser import match_parser, fixture_parser
from utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse fbref /matchs page")
    parser.add_argument("--date", help="The match date")
    parser.add_argument("--page", help="matches/ or fixtures/")
    parser.add_argument("--fixture_url", help="fixture url")
    parser.add_argument("--data_dir", help="Directory to store downloaded data", default="data")
    args = parser.parse_args()

    if not is_date_format(args.date):
        raise Exception(f"The --date parameter '{args.date}' is not in 'yyyy-mm-dd' format")
    
    date = args.date  # date = "2023-01-03"
    
    if args.page == "matches/":
        url = f"https://fbref.com/en/matchs/{date}"
        parsed_data = match_parser(url)
        parsed_data.to_csv(f"data/matchs_{date.replace('-','')}.csv", index=False)

    if args.page == "fixtures/" and args.fixture_url is not None:
        url = args.fixture_url
        parsed_data, league = fixture_parser(url)
        parsed_data.to_csv(f'data/fixtures_{league.lower().replace(" ","_")}.csv', index=False)
