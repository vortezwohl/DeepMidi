import time

import pygame
from midiutil import MIDIFile


def generate_midi_file(notes: list[int], midi_file: str):
    midi = MIDIFile(1)
    track = 0
    time_step = 0
    for value in notes:
        midi_note = value + 12
        midi.addNote(
            track=track,
            channel=0,
            pitch=midi_note,
            time=time_step,
            duration=1,
            volume=127
        )
        time_step += 0.25
    with open(midi_file, 'wb') as f:
        midi.writeFile(f)


def play_midi_with_pygame(midi_file: str):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(midi_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except pygame.error as e:
        print(e)
    finally:
        pygame.quit()
