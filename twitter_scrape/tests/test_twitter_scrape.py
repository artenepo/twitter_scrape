#!/usr/bin/env python3

import os
import json
from json.decoder import JSONDecodeError
import unittest
import urllib.request


HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/64.0.3282.186 Safari/537.36'),
    'Connection': 'keep-alive',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br'
}

HOST = os.environ['HOST'].rstrip('/')
PORT = os.environ['PORT']
BASE_URL = 'http://%s:%s' % (HOST, PORT)
TEST_USER = 'raymondh'
TEST_TAG = 'Python'
PAGES_LIMIT = 3
MIN_TWEETS_PER_PAGE = 12


class TestUserTweets(unittest.TestCase):

    def setUp(self):
        url = f'{BASE_URL}/users/{TEST_USER}?pages_limit={PAGES_LIMIT}'

        req = urllib.request.Request(url, headers=HEADERS, method='GET')
        with urllib.request.urlopen(req) as response:
            data = response.read()
            self.tweets = json.loads(data)
            self.status_code = response.getcode()
            self.content_type = response.getheader('Content-Type')

            try:
                self.tweets = json.loads(data)
            except JSONDecodeError as e:
                self.tweets = None

        self.test_passed = False

    def test_response(self):
        self.assertEqual(200, self.status_code)
        self.assertEqual('application/json', self.content_type)
        self.assertIsInstance(self.tweets, list)
        self.assertTrue(self.tweets, msg='Empty list received')

        tweets_have_hashtags = False
        for tweet in self.tweets:
            self.assertIsInstance(tweet, dict)
            self.assertIn('text', tweet)
            self.assertIsInstance(tweet['text'], str)

            self.assertIn('retweets', tweet)
            self.assertIsInstance(tweet['retweets'], int)

            self.assertIn('likes', tweet)
            self.assertIsInstance(tweet['likes'], int)

            self.assertIn('replies', tweet)
            self.assertIsInstance(tweet['replies'], int)

            self.assertIn('date', tweet)
            self.assertIsInstance(tweet['date'], str)

            self.assertIn('hashtags', tweet)
            self.assertIsInstance(tweet['hashtags'], list)
            for hashtag in tweet['hashtags']:
                self.assertIsInstance(hashtag, str)
                tweets_have_hashtags = True

            self.assertIn('account', tweet)
            self.assertIsInstance(tweet['account'], dict)

            self.assertIn('id', tweet['account'])
            self.assertIsInstance(tweet['account']['id'], int)

            self.assertIn('href', tweet['account'])
            self.assertIsInstance(tweet['account']['href'], str)

            self.assertIn('fullname', tweet['account'])
            self.assertIsInstance(tweet['account']['fullname'], str)
        self.assertTrue(tweets_have_hashtags,
                        msg='None of the tweets has hashtags')

        expected_expected = MIN_TWEETS_PER_PAGE * PAGES_LIMIT
        actual_amount = len(self.tweets)
        self.assertTrue(actual_amount >= expected_expected,
                        msg=('Pagination doesn\'t work. '
                             f'Expected {expected_expected} '
                             f'but got {actual_amount} tweets'))

        self.test_passed = True

    def tearDown(self):
        if not self.test_passed:
            print(repr(self.tweets))


class TestTweetsByHashtag(TestUserTweets):

    def setUp(self):
        url = f'{BASE_URL}/hashtags/{TEST_TAG}'
        req = urllib.request.Request(url, headers=HEADERS, method='GET')
        with urllib.request.urlopen(req) as response:
            data = response.read()
            self.tweets = json.loads(data)
            self.status_code = response.getcode()
            self.content_type = response.getheader('Content-Type')

            try:
                self.tweets = json.loads(data)
            except JSONDecodeError as e:
                self.tweets = None

        self.test_passed = False


if __name__ == '__main__':
    unittest.main()
