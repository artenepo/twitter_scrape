#### Table of contents:

* [Running in docker (local dev)](#running-in-docker-local-dev)
* [Running test](#running-tests)
* [API usage](#api-usage)
	* [Get tweets by a hashtag](#get-tweets-by-a-hashtag)
	* [Get user tweets](#get-user-tweets)
* [License](#license)

Running in docker (local dev)
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
Only Python 3.6+ is supported

1. Set up environment

```bash
$ export HOST=localhost
$ export PORT=5000
```

2. Go to `twitter_scrape/tests` folder and run `test_twitter_scrape.py`.


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
    - pages_limit: integer, specifies the number of pages to scrape.
    - wait: integer, specifies the custom amount of time to wait
        between each request to the Twitter. The default is a random
        number in the interval [0, 1.0]

**Example request:**

```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/hashtags/Python?pages_limit=3&wait=0

```
**Example response:**

```bash
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
```

### Get user tweets


Get the list of tweets that user has on his feed in json format.
Optional parameters:
    - pages_limit: integer, specifies the number of pages to scrape.
    - wait: integer, specifies the custom amount of time to wait
        between each request to the Twitter. The default is a random
        number in the interval [0, 1.0]

**Example request:**

```bash
curl -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:5000/users/Twitter?pages_limit=3&wait=0

```

**Example response:**

```bash
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
```

LICENSE
------------------------------

MIT
