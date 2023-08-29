# fbref scraper

Python scraper for https://fbref.com as a CLI.

## Installation

`pip install -r requirements.txt`

> TODO: create a real Python module and real installable CLI.

## Example

There are actually two available "endpoints" to scrape data:

👉 `/matches`

```bash
python main.py --date 2023-01-01 --page matches/ --data_dir=/tmp/data
```

👉 `/fixtures`

```bash
python main.py --date 2023-01-01 --page fixtures/ --fixture_url=https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures --data_dir=/tmp/data
``````

The CLI has several common options:

* `--date`: provide a date (sometimes useful for specific pages) - format is `%YYYY-%MM-%DD`
* `--page`: the "endpoint", i.e. the page to scrape.
* `--data_dir`: the path where scraped data will be stored


