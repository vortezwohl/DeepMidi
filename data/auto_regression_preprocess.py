import torch


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
