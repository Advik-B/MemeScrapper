from rich.console import Console
from rich.traceback import install
import requests
from os.path import join as pjoin, exists, isdir, isfile, abspath
from PIL import Image

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
