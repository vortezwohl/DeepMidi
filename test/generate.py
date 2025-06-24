import random

import torch
from deeplotx import AutoRegression

from data.note_digitize import encode as d_encode, decode as d_decode
from data.note_vectorize import encode as v_encode

ngram = 5
dtype = torch.float16
model = AutoRegression(feature_dim=120, hidden_dim=512, recursive_layers=8, model_name=f'../train/DATA8192-EPOCH321-GRAM5', dtype=dtype)
model.eval()


def _generate(notes: list[str], top_k: int) -> str:
    notes = torch.stack([v_encode(d_encode(x)) for x in notes], dim=0)
    next_note_distribution = torch.softmax(model.predict(notes), dim=-1).squeeze(0)
    next_note = torch.multinomial(next_note_distribution, num_samples=top_k).tolist()
    next_note = random.sample(next_note, 1)[0]
    return d_decode(next_note)


def generate(notes: list[str], top_k: int, max_notes: int) -> str:
    generated_notes = notes
    for _ in range(max_notes):
        new_note = _generate(notes=generated_notes[- ngram + 1:], top_k=top_k)
        generated_notes.append(new_note)
        yield new_note


if __name__ == '__main__':
    from test.sound import play_midi_with_pygame, generate_midi_file
    midi_file = './test_data_output/tmp.mid'
    note_seq = ['C_5', 'E_5', 'A_5', 'C_6']
    print('Input notes:', ', '.join(note_seq))
    print('Generated notes:', end=' ')
    # for note in generate(note_seq, 4, 100):
    #     print(note, end=', ')
    gen_notes = list(generate(note_seq, 2, 512))
    print(', '.join(gen_notes))
    generate_midi_file([d_encode(x) for x in note_seq + gen_notes], midi_file)
    play_midi_with_pygame(midi_file)
