#!/usr/bin/env python3

import os
import logging

from flask import Flask, request, jsonify, abort

from scrapper import user_tweets, tweets_by_hashtag

DEBUG = os.environ.get('DEBUG', 0)
logging.basicConfig(
    format='[%(asctime)-15s] %(name)-5s %(levelname)-8s %(message)s'
    )

app = Flask(__name__)

app.config['DEBUG'] = DEBUG


DEFAULT_PAGES_LIMIT = int(os.environ.get('DEFAULT_PAGES_LIMIT', 10))


@app.errorhandler(500)
def server_arror(e):
    """Custom error message"""

    message = 'An error occurred, the Twitter API may have changed'
    msg = {'message': message}
    return jsonify(msg), 500


@app.errorhandler(404)
def not_found(e):
    """Custom error message"""

    message = 'The requested url was not found on the server'
    if e.args:
        message = e.args
    msg = {'message': message}
    return jsonify(msg), 404


@app.route('/users/<user_name>')
def get_user_tweets(user_name):
    """Get the list of tweets that user has on his feed in json format.
    Optional parameters:
        - pages_limit: integer, specifies the number of pages to scrape.
        - wait: integer, specifies the custom amount of time to wait
            between each request to the Twitter. The default is a random
            number in the interval [0, 1.0]

    Example request:
        GET http://localhost:5000/users/Twitter?pages_limit=1
    Example response:
        [{"account": {"fullname": "Twitter",
                      "href": "/Twitter",
                      "id": 783214},
          "date": "2:54 PM - 8 Mar 2018",
          "hashtags": ["#InternationalWomensDay"],
          "likes": 287,
          "replies": 17,
          "retweets": 70,
          "text": "Powerful voices. Inspiring women.\n\n#InternationalWomensDay
                   https://twitter.com/i/moments/971870564246634496"},
          ...
        ]
    """
    try:
        pages_limit = int(request.args.get('pages_limit', DEFAULT_PAGES_LIMIT))
    except ValueError:
        pages_limit = DEFAULT_PAGES_LIMIT

    wait = request.args.get('wait')
    if wait is not None:
        try:
            wait = int(wait)
        except ValueError:
            wait = None

    try:
        tweets = user_tweets(user_name, pages_limit=pages_limit, wait=wait)
    except ValueError as e:
        app.logger.info(e.args)
        abort(404, e.args)
    except Exception:
        msg = (f'user_name: {user_name}, '
               f'pages_limit: {pages_limit}, '
               f'wait: {wait}')
        app.logger.exception(msg)
        abort(500)
    return jsonify(list(tweets))


@app.route('/hashtags/<tag>')
def get_tweets_by_hashtag(tag):
    """Get the list of tweets with the given hashtag.
    Optional parameters:
        - pages_limit: integer, specifies the number of pages to scrape.
        - wait: integer, specifies the custom amount of time to wait
            between each request to the Twitter. The default is a random
            number in the interval [0, 1.0]

    Example request:
        GET http://localhost:5000/hashtags/Python?pages_limit=3&wait=0
    Example response:
        [{"account": {"fullname": "Raymond Hettinger",
                      "href": "/raymondh",
                      "id": 14159138},
          "date": "12:57 PM - 7 Mar 2018",
          "hashtags": ["#python"],
          "likes": 169,
          "replies": 13,
          "retweets": 27,
          "text": "Historically, bash filename pattern matching was known
                   as \"globbing\".  Hence, the #python module
                   called \"glob\".\n\n
                   >>> print(glob.glob('*.py')\n\n
                   If the function were being added today, it would probably
                   be called os.path.expand_wildcards('*.py') which would be
                   less arcane."},
         ...
        ]
    """

    try:
        pages_limit = int(request.args.get('pages_limit', DEFAULT_PAGES_LIMIT))
    except ValueError:
        pages_limit = DEFAULT_PAGES_LIMIT

    wait = request.args.get('wait')
    if wait is not None:
        try:
            wait = int(wait)
        except ValueError:
            wait = None

    try:
        tweets = tweets_by_hashtag(tag, pages_limit=pages_limit,
                                   wait=wait)
    except Exception:
        msg = (f'tag: {tag}, '
               f'pages_limit: {pages_limit}, '
               f'wait: {wait}')
        app.logger.exception(msg)
        abort(500)
    return jsonify(list(tweets))


if __name__ == '__main__':
    app.run()
