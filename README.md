#Twitter Scrape

Simple scrapping program that provides API for reading user tweets or tweets with a specific hashtag.  
Developed as a home project for an interview.

#### Table of contents:

* [Running in docker](#running-in-docker)
* [Running test](#running-tests)
* [API usage](#api-usage)
	* [Get tweets by a hashtag](#get-tweets-by-a-hashtag)
	* [Get user tweets](#get-user-tweets)
* [License](#license)

Running in docker
------------------------------

1. Install docker and [docker-compose](https://docs.docker.com/compose/install/) for your host OS
Make sure you have at least following:

```bash
$ docker --version
Docker version 17.12.0-ce, build c97c6d6

$ docker-compose --version
docker-compose version 1.18.0, build 8dd22a9

```

2. Go to `provisioning` folder and create your desired local configuration based on `docker-compose.yml.local`

```bash
$ cp docker-compose.yml.local docker-compose.yml
$ docker-compose up

```

3. Once everything is up and running, you should be able to list running containers:
```bash
$ docker ps
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS                  PORTS                    NAMES
135d583ccb16        provisioning_twitter_scrape   "/mnt/start_server.sh"   1 second ago        Up Less than a second   0.0.0.0:5000->8888/tcp   provisioning_twitter_scrape_1
```

4. To get inside specific container and figure out how things work:

```bash
$ docker exec -ti "provisioning_twitter_scrape_1" "/bin/bash"
root@2cb919129b6b:/mnt/src# ls
Procfile  README.md  main.py  scrapper.py	tests

```

Running tests
------------------------------
Regression testing against running application.  
Only Python 3.6+ is supported.

1. Set up environment

```bash
$ export HOST=localhost
$ export PORT=5000
```

2. Go to `tests` folder and run `test_twitter_scrape.py`.


```bash
$ python3 test_twitter_scrape.py

test_response (__main__.TestTweetsByHashtag) ... ok
test_response (__main__.TestUserTweets) ... ok

----------------------------------------------------------------------
Ran 2 tests in 8.248s

OK
```

API usage
------------------------------

### Get tweets by a hashtag

Get the list of tweets with the given hashtag.
Optional parameters:
    - limit: integer, specifies the number of tweets to retriev=e

**Example request:**

```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/hashtags/python?limit=15
```
**Example response:**

```bash
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
```

### Get user tweets


Get the list of tweets that user has on his feed in json format.
Optional parameters:
    - limit: integer, specifies the number of tweets to retrieve

**Example request:**

```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/users/raymondh?limit=30
```

**Example response:**

```bash
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
```

LICENSE
------------------------------

MIT
