import torch
from torch.utils.data import DataLoader, TensorDataset


def auto_regression_preprocess(tensor_list: list[torch.Tensor], n_gram: int):
    vocab_size = tensor_list[0].shape[0]
    token_indices = [torch.argmax(oh, dim=0).item() for oh in tensor_list]
    x_list = []
    y_list = []
    for i in range(len(token_indices) - (n_gram - 1)):
        input_tokens = token_indices[i:i + (n_gram - 1)]
        target_token = token_indices[i + (n_gram - 1)]
        input_one_hot = torch.zeros(n_gram - 1, vocab_size, dtype=torch.int8)
        for j, token in enumerate(input_tokens):
            input_one_hot[j, token] = 1
        target_one_hot = torch.zeros(vocab_size, dtype=torch.int8)
        target_one_hot[target_token] = 1
        x_list.append(input_one_hot)
        y_list.append(target_one_hot)
    x = torch.stack(x_list)
    y = torch.stack(y_list)
    return x, y


def get_auto_regression_dataset_loaders(x: torch.Tensor, y: torch.Tensor, train_ratio: float = 0.95, batch_size: int = 16) -> tuple[DataLoader, DataLoader]:
    dataset_size = len(y)
    train_size = int(train_ratio * dataset_size)
    train_dataset = TensorDataset(x[:train_size], y[:train_size])
    valid_dataset = TensorDataset(x[train_size:], y[train_size:])
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=True)
    return train_loader, valid_loader
