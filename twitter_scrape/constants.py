import os

DEFAULT_LIMIT = int(os.environ.get('DEFAULT_LIMIT', 25))

TWITTER_USER_URL = (
    'https://twitter.com/i/profiles/show/{user}/timeline/tweets?'
    'include_available_features=1&include_entities=1&reset_error_state=false'
)
TWITTER_SEARCH_URL = (
    'https://twitter.com/i/search/timeline?vertical=default&src=hash&'
    'composed_count=0&include_available_features=1&include_entities=1&'
    'include_new_items_bar=true&interval=240000&q=%23{tag}'
)
