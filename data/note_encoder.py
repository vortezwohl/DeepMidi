def encode(note: str) -> int:
    note, octave = note.split('_', 1)
    octave = int(octave)
    note_offset = 0
    note_code = 0
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
            note_code = 12
    return note_code + 12 * octave + note_offset


def decode(note: int, use_flat_key: bool = False) -> str:
    octave = note // 12
    note_value = note % 12
    note_names_sharp = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
    note_names_flat = 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'
    note_names = note_names_flat if use_flat_key else note_names_sharp
    return f"{note_names[note_value]}_{octave}"


# todo debug
if __name__ == '__main__':
    for _note in 'b'.upper():
        for octave in range(10):
            note = f'{_note}_{octave}'
            _tmp_note = note
            code = encode(_tmp_note)
            _decode = decode(code, use_flat_key=False)
            print('code', code, 'note', _tmp_note, 'decode', _decode, 'correct', _tmp_note == _decode)
