import torch
from utils import _prepare_data, _update_loss_dict, _update_performance_dict, _print_epoch_results
from models.model import Model
from criterion.criterion import Criterion
from criterion.metrics import accuracy
from data.data import get_dataloader, get_dataset
from train import model_train



def main(config, epochs=1, batch_size=32,
         metrics=None, validation_data=True): # TODO later change to false!
    """
    :param config:
    # either dict or string. If string will use configuration that exists. If dict will build the model
    :param epochs:
    :param batch_size:
    :param metrics:
    :return:
    """
    if isinstance(config, str):
        # TODO get model
        pass
    else:
        # TODO build model
        pass

    model_config = config['model']
    task_config = config['mtl']
    net = Model(task_config, model_config)

    # TODO need
    criterion = Criterion(task_config)
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-04)

    train_dataset = get_dataset(task_config, "train")
    test_dataset = get_dataset(task_config, "test")

    train_dataloader = get_dataloader(train_dataset, batch_size)
    test_dataloader = get_dataloader(test_dataset, batch_size)

    if validation_data:
        val_dataset = get_dataset(task_config, "val")
        val_dataloader = get_dataloader(val_dataset, batch_size)
    # train loop

    print("Train loop started...")

    for i, epoch in enumerate(range(epochs)):
        print(f"Epoch {i+1}") # TODO beautify this with verbose later
        model_eval = model_train(task_config, net, criterion, optimizer, batch_size, train_dataloader, val_dataloader)

    print("Test loop started...")
    model_eval.eval()
    perfomance_dict = {"Seg": [], "Class": [], "BB": []}
    test_accuracy = 0
    with torch.no_grad():
        for i, mini_batch in enumerate(test_dataloader):

            mini_batch = _prepare_data(mini_batch, task_config)
            inputs = mini_batch["image"]

            task_targets = {task: mini_batch[task] for task in task_config["Tasks"].keys()}
            test_output = model_eval(inputs)
            test_accuracy += accuracy(task_targets['Class'], test_output['Class'])
            loss = criterion(test_output, task_targets)

            loss_epoch_dict = _update_performance_dict(loss_epoch_dict, loss, test_output,mini_batch,task_config)

    _print_epoch_results(perfomance_dict, config)
    print(f'Test Accuracy: {test_accuracy/(i+1)}')

if __name__ == '__main__':
    config = {
        'model': [64, 128, 256, 512],
        'mtl': {
            "Model": 'mtl model', # TODO why do we need this?
            "Tasks":{
                "Class":2,
                "Segmen":1,
                "BB":4
            },
            "Loss Lambda":{ "Class":1,"Segmen":1,"BB":1}
        }
    }


    main(config=config, epochs=1, batch_size=32)

