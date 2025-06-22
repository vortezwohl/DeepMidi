def encode(note: str) -> int:
    note, octave = note.split('_', 1)
    octave = int(octave)
    note_offset = 0
    note_code = 1
    if len(note) == 2:
        match note[1]:
            case 'b':
                note_offset = -1
            case '#':
                note_offset = 1
    match note[0]:
        case 'c':
            note_code = 0
        case 'd':
            note_code = 2
        case 'e':
            note_code = 4
        case 'f':
            note_code = 5
        case 'g':
            note_code = 7
        case 'a':
            note_code = 9
        case 'b':
            note_code = 11
    return note_code + 12 * octave + note_offset + 1


def decode(midi_note: int, use_flat_key: bool = False) -> str:
    octave = midi_note // 12
    note_value = midi_note % 12
    note_names_sharp = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
    note_names_flat = 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'
    note_names = note_names_flat if use_flat_key else note_names_sharp
    return f"{note_names[note_value]}_{octave}"


# todo debug
if __name__ == '__main__':
    code = encode('C#_0')
    note = decode(code, use_flat_key=False)
    print(code, note)
