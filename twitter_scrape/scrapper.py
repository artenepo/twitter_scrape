from typing import AnyStr, Generator, List, Dict

from bs4 import BeautifulSoup
import requests

from parser import parse_tweet_container

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7,it;q=0.6,la;q=0.5',
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/64.0.3282.186 Safari/537.36'),
    'x-requested-with': 'XMLHttpRequest',
    'x-twitter-active-user': 'yes'
}


def get_tweet_stream(url: AnyStr) -> Generator:
    """A generator that produces tweets"""

    response = requests.get(url, headers=headers, params={'max_position': ''})

    while True:
        response.raise_for_status()

        json_response = response.json()
        if json_response['min_position'] is None:
            break

        soup = BeautifulSoup(json_response['items_html'], 'html.parser')
        stream_items = soup.find_all('li', {'data-item-type': 'tweet'},
                                     class_='stream-item')

        for tweet in stream_items:
            if tweet.find('div', class_='account'):
                # skip account container
                continue

            yield parse_tweet_container(tweet)

        if not json_response['has_more_items']:
            break

        last_tweet_id = stream_items[-1]['data-item-id']

        response = requests.get(url, headers=headers,
                                params={'max_position': last_tweet_id})


def get_tweets(url: AnyStr, limit: int) -> List[Dict]:
    results = []
    for tweet in get_tweet_stream(url):
        results.append(tweet)
        if len(results) == limit:
            break

    return results
