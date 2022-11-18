import json
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
    # i.imgur.com
    r"https://i.imgur.com/[^/]+",
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


def get_image_urls_reddit(urls: tuple, even_reddit_comments: bool = False):
    reddit_regex = REDDIT_URLS_REGEXES[:-2]  # From the first element to the second-from-the-last element
    reddit_comments_regex = REDDIT_URLS_REGEXES[0]
    valid_urls = []
    for url in urls:
        for regex in reddit_regex:
            if re.match(regex, url):
                valid_urls.append(url)
                break

    for url in valid_urls:
        if re.match(reddit_comments_regex, url):
            if even_reddit_comments:
                valid_urls.append(get_image_from_reddit_comments(url))
        else:
            valid_urls.append(url)



def get_image_from_reddit_comments(url: str):
    time_to_wait = 5
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    r = get(url, headers=headers, timeout=time_to_wait)
    _i_reddit = REDDIT_URLS_REGEXES[1]
    soup = BeautifulSoup(r.text, "html.parser")
    del r
    # Save the html for debugging
    with open("reddit.html", "w") as f:
        f.write(soup.prettify())
    images = soup.find_all("a", {"target": "_blank"})
    for image in images:
        im = image["href"]
        if re.match(_i_reddit, im):
            return im


def test():
    urls = load_urls_("memes.json")
    TEST_URL = "https://www.reddit.com/r/ProgrammerHumor/comments/yyakjv/everyone_go_home_turns_out_all_our_work_runs/"
    first_len = len(urls)
    urls = remove_duplicates(urls)
    urls = filter(url_filter, urls)
    urls = tuple(urls)
    filt_len = len(urls)
    print(f"Filtered {first_len - filt_len} urls out of {first_len} urls")
    get_image_urls_reddit(urls)

if __name__ == "__main__":
    test()
