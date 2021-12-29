import torch
import torch.nn as nn

# testing git

def get_loss(task):
    
    if task == 'class':
        from criterion.loss_functions import CrossEntropyLoss
        return CrossEntropyLoss()

    elif task == 'segmen':
        from criterion.loss_functions import BCEWithLogitsLoss
        return BCEWithLogitsLoss()

    elif task == 'BB':
        from criterion.loss_functions import IoULoss
        return IoULoss()

    return

class Criterion(nn.Module):
    def __init__(self, config):
        super(Criterion, self).__init__()
        self.tasks = config["Tasks"].key()
        self.loss_fncts = torch.nn.ModuleDict({task: get_loss(task) for task in self.tasks})

    
    def forward(self, prediction, truth):
        out = {task: self.loss_fncts[task](prediction[task], truth[task]) for task in self.tasks}
        out['total'] = torch.sum(torch.stack([out[task] for task in self.tasks]))
        return out