import os
import hashlib
import requests

CACHE_DIR = "cache/thumbs"
MAX_CACHE = 200

os.makedirs(CACHE_DIR, exist_ok=True)


def clean_cache():

    files = sorted(
        [os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR)],
        key=os.path.getmtime
    )

    if len(files) <= MAX_CACHE:
        return

    to_delete = files[:len(files) - MAX_CACHE]

    for f in to_delete:
        try:
            os.remove(f)
        except:
            pass


def cache_thumb(url):

    name = hashlib.md5(url.encode()).hexdigest() + ".jpg"
    path = os.path.join(CACHE_DIR, name)

    if not os.path.exists(path):

        r = requests.get(url, timeout=5)

        with open(path, "wb") as f:
            f.write(r.content)

        clean_cache()

    return path