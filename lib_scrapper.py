import re

from requests import get
from bs4 import BeautifulSoup

# WARNING: Do NOT edit the regexes below or add any other regexes.
# The functions HEAVILY depend on the order of the regexes.
# Keep in mind.
REDDIT_URLS_REGEXES = (
    r"https://www.reddit.com/r/[^/]+/comments/[^/]+/[^/]+/[^/]+",
    # i.redd.it
    r"https://i.redd.it/[^/]+",
    # Reddit videos
    r"https://v.redd.it/[^/]+",
    # Reddit.com
    r"https://www.reddit.com/r/[^/]+/comments/[^/]+/[^/]+",
)

REDDIT_COMMENTS_REGEX = r"https://www.reddit.com/r/[^/]+/*"
IMGUR_REGEX = r"https://i.imgur.com/[^/]+"



def url_filter(url: str):
    for regex in REDDIT_URLS_REGEXES:
        if re.match(regex, url):
            return True
    return False


def remove_duplicates(urls: tuple):
    return tuple(set(urls))


def get_image_urls_reddit(urls: tuple[str], even_reddit_comments: bool = False):
    reddit_regex = REDDIT_URLS_REGEXES[:-1]  # From the first element to the second-from-the-last element
    valid_urls = []
    for url in urls:
        for regex in reddit_regex:
            if re.match(regex, url):
                valid_urls.append(url)
                break

    _final_urls = []
    for url in valid_urls:
        print(f"Checking {url}")
        if re.match(REDDIT_COMMENTS_REGEX, url) and even_reddit_comments:
            _final_urls.append(get_image_from_reddit_comments(url))
        else:
            _final_urls.append(url)

    return _final_urls

def get_image_from_reddit_comments(url: str, save: bool = False):
    time_to_wait = 5
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.159 Safari/537.36 "
    }
    r = get(url, headers=headers, timeout=time_to_wait)
    _i_reddit = REDDIT_URLS_REGEXES[1]
    soup = BeautifulSoup(r.text, "html.parser")
    del r
    # Save the html for debugging
    if save:
        with open("reddit.html", "w") as f:
            f.write(soup.prettify())
    images = soup.find_all("a", {"target": "_blank"})
    for image in images:
        im = image["href"]
        if re.match(_i_reddit, im):
            return im


def get_image_urls(urls: tuple[str], even_reddit_comments: bool = False):
    # Sort the urls into reddit and non-reddit
    reddit_urls = []
    non_reddit_urls = []
    for url in urls:
        if re.match(REDDIT_URLS_REGEXES[0], url):
            reddit_urls.append(url)
        elif re.match(IMGUR_REGEX, url):
            non_reddit_urls.append(url)

    # Get the images from reddit
    reddit_urls_ = get_image_urls_reddit(reddit_urls, even_reddit_comments)
    # Return the rest
    return reddit_urls_.extend(non_reddit_urls)
