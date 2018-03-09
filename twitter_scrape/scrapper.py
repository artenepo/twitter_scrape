#!/usr/bin/env python3

import logging
from random import random
import re
import time

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

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

url_pattern = re.compile('( http|http| ftp|ftp| https|https):\/\/')


def url_repl(sre):
    """Add space at the begging of the given URL.

    Argument sre is the result of re.match() and re.search()"""

    return ' ' + sre.group(0)


def parse_container(container):
    """Parse data and return a dictionary.

    Argument container is an instance of bs4.element.Tag type.
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#tag
    """

    date = container.find('a', class_='tweet-timestamp')['title']
    actions = []
    for i in container.find_all('span',
                                {'data-tweet-stat-count': True},
                                class_='ProfileTweet-actionCount'):
        actions.append(int(i['data-tweet-stat-count']))

    replies, retweets, likes, *_ = actions

    text_container = container.find('div',
                                    class_='js-tweet-text-container')
    hashtags = []
    for h in text_container.find_all('a', class_='twitter-hashtag'):
        hashtags.append(h.text)

    # raw_tweet_text usually does'nt contain a space before urls
    raw_tweet_text = text_container.text.strip('\n')
    tweet_text = re.sub(url_pattern, url_repl, raw_tweet_text)

    user_full_name = container.find('strong', class_='fullname').text

    user_data = container.find('a', class_='account-group')
    user_id = int(user_data['data-user-id'])
    user_href = user_data['href']

    tweet = {'date': date, 'replies': replies, 'retweets': retweets,
             'likes': likes, 'hashtags': hashtags,
             'text': tweet_text,
             'account': {'id': user_id, 'href': user_href,
                         'fullname': user_full_name}}
    return tweet


def user_tweets(user, pages_limit=10, wait=None):
    """A generator that produces tweets of a given user.

    Optional argument wait sets the waiting time between the requests to mask
    the work of the crapper; if it is the default None, the random.random
    function will be used.
    """

    headers['referer'] = f'https://twitter.com/{user}'

    url = (f'https://twitter.com/i/profiles/show/{user}/timeline/tweets?'
           'include_available_features=1&include_entities=1'
           '&reset_error_state=false')

    r = requests.get(url, headers=headers, params={'max_position': ''})

    while pages_limit:
        json_response = r.json()
        if not r.status_code == 200:
            if r.status_code >= 400:
                raise ValueError(f'{user} doesn\'t exist or unavailable.')

            logger.error('\nURL: %s\nResponse: %r' % (r.url, json_response))
            raise Exception(f'Unexpected status code received (%s)' %
                            r.status_code)
        try:
            if json_response['min_position'] is None:
                break
        except KeyError:
            logger.error('\nURL: %s\nResponse: %r' % (r.url, json_response))
            break

        soup = BeautifulSoup(json_response['items_html'], 'html.parser')
        containers = soup.find_all('li', {'data-item-type': 'tweet'},
                                   class_='stream-item')

        last_tweet_id = containers[-1]['data-item-id']

        for container in containers:
            if container.find('div', class_='account'):
                # not a tweet found
                continue
            yield parse_container(container)

        pages_limit -= 1

        if not json_response['has_more_items'] or not pages_limit:
            break

        if wait is None:
            time.sleep(random())
        elif wait != 0:
            time.sleep(wait)

        r = requests.get(url, headers=headers,
                         params={'max_position': last_tweet_id})

        logger.debug(f'max_position: {last_tweet_id}')


def tweets_by_hashtag(tag, pages_limit=10, wait=None):
    """A generator that produces tweets with a given hashtag.

    Optional argument wait sets the waiting time between the requests to mask
    the work of the crapper; if it is the default None, the random.random
    function will be used.
    """

    url = ('https://twitter.com/i/search/timeline?'
           'vertical=default&src=hash&composed_count=0&'
           'include_available_features=1&include_entities=1&'
           'include_new_items_bar=true&interval=240000')

    headers['referer'] = f'https://twitter.com/hashtag/{tag}?src=hash'
    hashtag = f'#{tag}'
    r = requests.get(url, headers=headers, params={'q': hashtag,
                                                   'latent_count': 0})
    while pages_limit:
        json_response = r.json()

        if not r.status_code == 200:
            logger.error('\nURL: %s\nResponse: %r' % (r.url, json_response))
            raise Exception(f'Unexpected status code received (%s)' %
                            r.status_code)

        new_latent_count = json_response['new_latent_count']
        max_position = json_response.get('max_position', '')

        soup = BeautifulSoup(json_response['items_html'], 'html.parser')
        containers = soup.find_all('li', {'data-item-type': 'tweet'},
                                   class_='stream-item')
        for container in containers:
            if container.find('div', class_='account'):
                # not a tweet found
                continue

            yield parse_container(container)

        pages_limit -= 1

        if not json_response['has_more_items'] or not pages_limit:
            break

        if wait is None:
            time.sleep(random())
        elif wait != 0:
            time.sleep(wait)

        r = requests.get(url, headers=headers,
                         params={'latent_count': new_latent_count,
                                 'min_position': max_position,
                                 'q': hashtag})

        logger.debug(f'latent_count: {new_latent_count}')