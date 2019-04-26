from typing import AnyStr

from flask import Flask, request, jsonify
from requests import HTTPError

from constants import DEFAULT_LIMIT, TWITTER_USER_URL, TWITTER_SEARCH_URL
from scrapper import get_tweets

app = Flask(__name__)


def get_limit():
    limit = request.args.get('limit')
    if limit and limit.isdigit():
        return int(limit)
    else:
        return DEFAULT_LIMIT


@app.route('/users/<string:user_name>')
def get_user_tweets(user_name: AnyStr):
    """Get the list of tweets that user has on his feed in json format.
    Optional parameters:
        - pages_limit: integer, specifies the number of pages to scrape.
        - wait: integer, specifies the custom amount of time to wait
            between each request to the Twitter. The default is a random
            number in the interval [0, 1.0]

    Example request:
        GET http://localhost:5000/users/raymondh?limit=5
    Example response:
        [{
            account: {
                fullname: "Raymond Hettinger",
                href: "/raymondh",
                id: 14159138
            },
            date: "2019-04-06T10:52:00+07:00",
            hashtags: [
                "#Python"
            ],
            likes: 36,
            replies: 0,
            retweets: 14,
            text: "How to do you usually write your #Python tests?"
        },
          ...
        ]
    """
    limit = get_limit()
    url = TWITTER_USER_URL.format(user=user_name)
    try:
        results = get_tweets(url, limit)
    except HTTPError as e:
        error = e.response.json()
        return jsonify({'error': error['message']})

    return jsonify({'results': results})


@app.route('/hashtags/<string:tag>')
def get_tweets_by_hashtag(tag: AnyStr):
    """Get the list of tweets with the given hashtag.
    Optional parameters:
        - pages_limit: integer, specifies the number of pages to scrape.
        - wait: integer, specifies the custom amount of time to wait
            between each request to the Twitter. The default is a random
            number in the interval [0, 1.0]

    Example request:
        GET http://localhost:5000/hashtags/python?limit=5
    Example response:
        [{
            "account": {
                "fullname": "Hugo de Vos",
                "href": "/Ottotos",
                "id": 1026921204
            },
            "date": "2019-04-23T06:02:00+07:00",
            "hashtags": [
                "#python"
            ],
            "likes": 11,
            "replies": 0,
            "retweets": 7,
            "text": "I found a funny, unreadable, unpractical but working  way to
                    do conditional string formatting in #python ?
                    pic.twitter.com/RjUp4XQC4h"
            },
            ...
        ]
    """

    limit = get_limit()
    url = TWITTER_SEARCH_URL.format(tag=tag)
    try:
        results = get_tweets(url, limit)
    except HTTPError as e:
        error = e.response.json()
        return jsonify({'error': error['message']})

    return jsonify({'results': results})


if __name__ == '__main__':
    app.run()
