import json
from os import remove as rm, makedirs as mkdir
from os.path import join as pjoin, exists, isdir, isfile
from shutil import rmtree

import requests
from PIL import Image
from rich.console import Console
from rich.traceback import install

console = Console()
install(show_locals=True, extra_lines=5)

SAVE_PATH = "cache"
OUTPUT_PATH = "output"


def download(url: str):
    r = requests.get(url, stream=True)
    filename_: str = url.split("/")[-1]
    console.print(f"[green]Downloading[/] [yellow]{filename_}[/] ({url})")
    with open(pjoin(SAVE_PATH, filename_), "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def process(image: str):
    image_ = image
    sav_ = pjoin(OUTPUT_PATH, image_.replace("jpg", "PNG"))
    image = pjoin(SAVE_PATH, image)
    console.print(f"[cyan]Processing[/] [yellow]{image}[/] -> [yellow]{sav_}[/]")
    img = Image.open(image)
    img = img.convert("RGB")
    img.save(sav_, "PNG")
    img.close()
    del img, image, image_


def remove(image: str):
    image = pjoin(SAVE_PATH, image)
    console.print(f"[magenta]Removing[/] [yellow]{image}[/]")
    rm(image)


def load_urls(filename):
    with open(filename) as f:
        data = json.load(f)

    data = data[0]
    windows = data["windows"]["3"]
    urls = []
    for _, v in windows.items():
        urls.append(v["url"])
    del data, windows, v
    urls = set(urls)
    return tuple(urls)


def fs_check(path):
    """
    Filesystem check
    checks if the path exists and if it is a directory or a file
    if it is a file, it will be deleted
    if it is a directory, it will be deleted
    if it does not exist, it will be created
    :param path:
    :return: None
    """
    if exists(path):
        if isdir(path):
            rmtree(path)
            mkdir(path)
        elif isfile(path):
            remove(path)
            mkdir(path)
    else:
        mkdir(path)
