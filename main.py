import json
import multiprocessing as mp
from os import listdir, remove as rm, makedirs as mkdir
from os.path import join as pjoin, exists, isdir, isfile, abspath
from shutil import rmtree
from sys import argv

import psutil


filename: str = "data.json"
try:
    filename = argv[1]
except IndexError:
    pass

_ls = listdir(".")

# Get the data from the local file
with open(filename) as f:
    data = json.load(f)

# Filter the data we need
data = data[0]
windows = data["windows"]["3"]

urls = []
for _, v in windows.items():
    urls.append(v["url"])
del data, windows, v
# Convert the urls to a set to remove duplicates
urls = set(urls)
# Convert the urls to a tuple to make it immutable
urls = tuple(urls)
# print(*urls, sep="\n") # DEBUG: Print the urls
save_path = "cache"
output_path = "output"


def fs_check(path):
    if exists(path):
        if isdir(path):
            rmtree(path)
            mkdir(path)
        elif isfile(path):
            remove(path)
            mkdir(path)
    else:
        mkdir(path)




if __name__ == "__main__":
    fs_check(save_path)
    fs_check(output_path)
    cpu_count = mp.cpu_count()
    # to run at a time
    per_process = max(len(urls) // cpu_count, 1)
    ram = psutil.virtual_memory().available
    print(f"Available RAM: {ram // 1024 // 1024} MB")
    # Divide the available ram by 3 to get the amount of ram
    # to use per process
    per_ram = ram // cpu_count
    if per_ram // 1024 // 1024 < 0:
        raise MemoryError("Not enough (free) RAM to run this program!")

    per_process_ram = per_ram // per_process
    print(f"Using {per_ram // 1024 // 1024} MB overall")
    print(f"Using {per_process_ram // 1024 // 1024} MB per process")
    with mp.Pool() as pool_1:
        pool_1.map(download, urls, chunksize=per_process_ram)
        pool_1.close()
        pool_1.join()
    console.print("\n\n[bold blue]Downloaded all images[/]\n\n")
    images = listdir(save_path)
    with mp.Pool() as pool_2:
        pool_2.map(process, images, chunksize=per_process_ram)
        pool_2.close()
        pool_2.join()

    console.print("\n\n[bold blue]Done processing images![/]\n\n")

    images = listdir(save_path)
    with mp.Pool() as pool_3:
        pool_3.map(remove, images, chunksize=per_process_ram)
        pool_3.close()
        pool_3.join()

    rmtree(save_path, ignore_errors=True)
    console.print("\n\n[bold blue]Done removing images![/]\n\n")
    console.print("[bold green]Done, check the output folder![/]")
    console.print(f"[i yellow]{abspath(output_path)}[/]")
