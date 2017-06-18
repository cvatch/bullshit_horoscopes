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
    return zodiac.text

    # headings = (h.text for h in zodiac.find_all('h4'))
    # paragraphs = (p.text for p in zodiac.find_all('p'))
    # return {h: p for h, p in zip(headings, paragraphs)}


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
            time.sleep(0.5)
    except Exception as e:
        print("Interrupted. saving what I have @ {}".format(date))
        print(e)

    return all_dates

if __name__ == '__main__':
    stop = datetime.datetime(2014, 1, 9)
    start = datetime.datetime.today()
    diff = (start - stop).days
    try:
        all_dates = get_all_horoscopes(start, diff)
    except Exception as e:
        print("Something is wrong")
        print(e)
    print("Dumping horoscopes")
    with open('horoscopes_{}_{}.json'.format(start, stop), 'w') as f:
        json.dump(all_dates, f)
    print("Dumped")
