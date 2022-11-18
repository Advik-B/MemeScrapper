import multiprocessing as mp
from os import listdir
from os.path import abspath
from shutil import rmtree

import psutil

from lib_utility import fs_check, process, remove, download, console, SAVE_PATH, OUTPUT_PATH, load_urls


def main():
    urls = load_urls("data.json")
    fs_check(SAVE_PATH)
    fs_check(OUTPUT_PATH)
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
    images = listdir(SAVE_PATH)
    with mp.Pool() as pool_2:
        pool_2.map(process, images, chunksize=per_process_ram)
        pool_2.close()
        pool_2.join()

    console.print("\n\n[bold blue]Done processing images![/]\n\n")

    images = listdir(SAVE_PATH)
    with mp.Pool() as pool_3:
        pool_3.map(remove, images, chunksize=per_process_ram)
        pool_3.close()
        pool_3.join()

    rmtree(SAVE_PATH, ignore_errors=True)
    console.print("\n\n[bold blue]Done removing images![/]\n\n")
    console.print("[bold green]Done, check the output folder![/]")
    console.print(f"[i yellow]{abspath(OUTPUT_PATH)}[/]")


if __name__ == "__main__":
    main()
