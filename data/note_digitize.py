def encode(note: str) -> int:
    note, octave = note.lower().split('_', 1)
    octave = int(octave)
    note_offset = 0
    codebook = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
    if len(note) == 2:
        match note[1]:
            case 'b':
                note_offset = -1
            case '#':
                note_offset = 1
    return codebook.get(note[0], 0) + 12 * octave + note_offset


def decode(note: int, use_flat_key: bool = False) -> str:
    if note < 0:
        return 'Unknown'
    octave = note // 12
    note_value = note % 12
    note_names_sharp = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
    note_names_flat = 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'
    note_names = note_names_flat if use_flat_key else note_names_sharp
    return f"{note_names[note_value]}_{octave}"
