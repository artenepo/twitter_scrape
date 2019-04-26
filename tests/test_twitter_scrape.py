#!/usr/bin/env python3

import os
import json
from json.decoder import JSONDecodeError
import unittest
import urllib.request


HOST = os.environ['HOST'].rstrip('/')
PORT = os.environ['PORT']
BASE_URL = 'http://%s:%s' % (HOST, PORT)
TEST_USER = 'raymondh'
TEST_TAG = 'python'
LIMIT = 30


class TestUserTweets(unittest.TestCase):

    def setUp(self):
        url = f'{BASE_URL}/users/{TEST_USER}?limit={LIMIT}'

        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req) as response:
            data = response.read()
            self.tweets = json.loads(data)
            self.status_code = response.getcode()
            self.content_type = response.getheader('Content-Type')

            try:
                self.response = json.loads(data)
            except JSONDecodeError:
                self.response = None

        self.test_passed = False

    def test_response(self):
        self.assertEqual(200, self.status_code)
        self.assertEqual('application/json', self.content_type)
        self.assertNotIn('error', self.response, msg='Error received: {}'.format(self.response.get('error')))
        self.assertIn('results', self.response)

        tweets = self.response['results']
        self.assertIsInstance(tweets, list)
        self.assertTrue(tweets, msg='Empty list received')

        tweets_have_hashtags = False
        for tweet in tweets:
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

        self.assertEqual(len(tweets), LIMIT,
                         msg=('Limit doesn\'t work. '
                              f'Expected {LIMIT} '
                              f'but got {len(tweets)} tweets'))

        self.test_passed = True

    def tearDown(self):
        if not self.test_passed:
            print(repr(self.response))


class TestTweetsByHashTag(TestUserTweets):

    def setUp(self):
        url = f'{BASE_URL}/hashtags/{TEST_TAG}?limit={LIMIT}'
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req) as response:
            data = response.read()
            self.tweets = json.loads(data)
            self.status_code = response.getcode()
            self.content_type = response.getheader('Content-Type')

            try:
                self.response = json.loads(data)
            except JSONDecodeError:
                self.response = None

        self.test_passed = False


if __name__ == '__main__':
    unittest.main()
