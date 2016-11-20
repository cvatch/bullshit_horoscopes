import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import datetime
import time
import json


def fetch_horoscope(date):
    base_url = 'https://www.novinky.cz/horoskop/?{}'
    date_arg = urlencode({'date': date})

    r = requests.get(base_url.format(date_arg))
    return r.text

def parse_page(text):
    soup = BeautifulSoup(text)
    zodiac = soup.find(id='zodiacContent')

    headings = (h.text for h in zodiac.find_all('h4'))
    paragraphs = (p.text for p in zodiac.find_all('p'))
    return {h: p for h, p in zip(headings, paragraphs)}


def get_horoscope(date):
    page = fetch_horoscope(date)
    parsed = parse_page(page)
    return parsed


def get_all_horoscopes(start, numdays):
    base = start
    # base = datetime.datetime.today()
    date_list = ((base - datetime.timedelta(days=x)).strftime("%d.%m.%Y")
                 for x
                 in range(0, numdays))
    all_dates = {}
    try:
        for date in date_list:
            print("Getting {}".format(date))

            all_dates[date] = get_horoscope(date)
            time.sleep(1)
    except Exception as e:
        print("Interrupted. saving what I have")
        print(e)

    print("Dumping horoscopes")
    with open('horoscopes_{}_{}.json'.format(base, numdays), 'w') as f:
        json.dump(all_dates, f)
    print("Dumped")

if __name__ == '__main__':
    start = datetime.datetime(2014, 10, 30)
    stop = 180
    get_all_horoscopes(start, stop)
