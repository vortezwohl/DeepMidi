import torch

base_tensor = torch.zeros(120, dtype=torch.int8)


def encode(note: int) -> torch.Tensor:
    t =  base_tensor.detach().clone()
    t[note] = 1
    return t


def decode(note: torch.Tensor) -> int:
    idx = 0
    for d in note:
        if d:
            return idx
        idx += 1
    return -1
