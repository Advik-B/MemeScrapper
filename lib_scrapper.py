import json
import re
from requests import get

REDDIT_URLS_REGEXES = (
    r"https://www.reddit.com/r/[^/]+/comments/[^/]+/[^/]+/[^/]+",
    # redd.it
    r"https://redd.it/[^/]+",
    # i.redd.it
    r"https://i.redd.it/[^/]+",
    # i.imgur.com
    r"https://i.imgur.com/[^/]+",
    # Reddit videos
    r"https://v.redd.it/[^/]+",
    # Reddit.com
    r"https://www.reddit.com/r/[^/]+/comments/[^/]+/[^/]+",
)

def load_urls_(filename):
    with open(filename) as f:
        data = json.load(f)

    data = data[0]
    windows = data["windows"]["3"]
    urls = []
    for _, v in windows.items():
        urls.append(v["url"])
    del data, windows, v
    urls = set(urls)
    urls = tuple(urls)
    return urls

def url_filter(url: str):
    for regex in REDDIT_URLS_REGEXES:
        if re.match(regex, url):
            return True
    return False

def remove_duplicates(urls: tuple):
    return tuple(set(urls))

def test():
    urls = load_urls_("memes.json")
    first_len = len(urls)
    urls = remove_duplicates(urls)
    urls = filter(url_filter, urls)
    urls = tuple(urls)
    filt_len = len(urls)
    print(f"Filtered {first_len - filt_len} urls out of {first_len} urls")


if __name__ == "__main__":
    test()
