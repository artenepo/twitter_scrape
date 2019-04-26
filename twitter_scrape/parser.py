import re
from datetime import datetime
from tzlocal import get_localzone
from typing import AnyStr, Dict, Tuple, List, Union
from bs4.element import Tag


url_pattern = re.compile(r'(( http|http| ftp|ftp| https|https)://)|(pic\.twitter\.com/)')
timezone = get_localzone()


def get_date(container: Tag) -> AnyStr:
    date_string = container.find('a', class_='tweet-timestamp')['title']
    date = datetime.strptime(date_string, '%I:%M %p - %d %b %Y')
    return timezone.localize(date).isoformat()


def get_account(container: Tag) -> Dict[AnyStr, AnyStr]:
    account = container.find('a', class_='account-group')
    account_id = int(account['data-user-id'])
    href = account['href']

    full_name = container.find('strong', class_='fullname').text

    return {'id': account_id, 'href': href, 'fullname': full_name}


def re_url_repl(sre) -> AnyStr:
    """Add space at the begging of the given URL.

    Argument sre is the result of re.match() and re.search()"""

    return ' ' + sre.group(0)


def get_body(container: Tag) -> Tuple[AnyStr, List[AnyStr]]:
    body = container.find('div', class_='js-tweet-text-container')
    hash_tags = []
    for h in body.find_all('a', class_='twitter-hashtag'):
        hash_tags.append(h.text)

    # raw_text usually doesn't contain a space before urls
    raw_text = body.text.strip('\n')
    text = url_pattern.sub(re_url_repl, raw_text)
    return text, hash_tags


def get_stat_count(container: Tag) -> Tuple[int, int, int]:
    replies, retweets, likes = 0, 0, 0

    for i in container.find_all('span', {'data-tweet-stat-count': True},
                                class_='ProfileTweet-actionCount'):
        count = int(i['data-tweet-stat-count'])
        if 'replies' in i.text:
            likes = count
        elif 'retweets' in i.text:
            retweets = count
        elif 'likes' in i.text:
            likes = count

    return replies, retweets, likes


def parse_tweet_container(container: Tag) -> Dict[AnyStr, Union[AnyStr, int]]:
    date = get_date(container)
    account = get_account(container)
    text, hashtags = get_body(container)
    replies, retweets, likes = get_stat_count(container)

    return {'date': date, 'account': account,
            'text': text, 'hashtags': hashtags,
            'replies': replies, 'retweets': retweets, 'likes': likes}
