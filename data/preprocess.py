import os
import random
import time

import requests
from music21 import converter, note, chord
from deeplotx.util import get_files
from vortezwohl.concurrent import ThreadPool


def download(url: str, filename: str, interval: int = 0) -> str:
    if os.path.exists(filename):
        return f'File "{filename}" already exists.'
    try:
        if interval > 0:
            time.sleep(random.randint(int(interval / 2 // 1), interval))
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return f'File from "{url}" is downloaded to "{filename}".'
    except requests.exceptions.RequestException as e:
        return f'File failed to download: {e}.'


def analyse_midi(filename: str, freq: bool = False, mode: str = 'note') -> tuple[str, list | None]:
    def convert_name(_note: str):
        return _note.replace('-flat', 'b').replace('-sharp', '#').replace('in octave', '').replace(' ', '')
    res = []
    try:
        s = converter.parse(filename)
        for e in s.flatten():
            match mode:
                case 'note':
                    if isinstance(e, note.Note):
                        if freq:
                            res.append((e.pitch.frequency, e.duration.quarterLength))
                        else:
                            res.append((convert_name(e.pitch.fullName), e.duration.quarterLength))
                case 'chord':
                    if isinstance(e, chord.Chord):
                        if freq:
                            pitches = '|'.join(str(p.frequency) for p in e.pitches)
                        else:
                            pitches = '|'.join(convert_name(p.fullName) for p in e.pitches)
                        res.append((pitches, e.duration.quarterLength))
        return filename, res
    except:
        return filename, None


def analyse_all_midi(path: str, freq: bool = False, mode: str = 'note') -> list:
    workers = ThreadPool(64)
    files = get_files(path)
    inputs = list(zip(files, [freq] * len(files), [mode] * len(files)))
    results = [x[2] for x in workers.gather([analyse_midi] * len(files), inputs)]
    return [x for x in results]
