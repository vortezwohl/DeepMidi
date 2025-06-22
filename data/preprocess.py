import os
import random
import time

import requests


def download(url: str, filename: str, interval: int = 0) -> str:
    if os.path.exists(filename):
        return f'File "{filename}" already exists.'
    try:
        if interval > 0:
            time.sleep(random.randint(0, interval))
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return f'File from "{url}" is downloaded to "{filename}".'
    except requests.exceptions.RequestException as e:
        return f'File failed to download: {e}.'
