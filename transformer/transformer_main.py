import argparse
from trainer import *
from helpers import *
from inference import *


from data_loader import *


def transformer_main(

        epoch: int = 1000,
        training_length=180,
        forecast_window=90,
        train_csv="train_dataset.csv",
        test_csv="test_dataset.csv",
        path_to_save_model="save_model/",
        path_to_save_loss="save_loss/",
        path_to_save_predictions="save_predictions/",
        device="cpu"
):
    train_dataset = SensorDataset(csv_name=train_csv, root_dir="source/", training_length=training_length,
                                  forecast_window=forecast_window)
    train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=False)

    test_dataset = SensorDataset(csv_name=test_csv, root_dir="source/", training_length=training_length,
                                 forecast_window=forecast_window)
    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False)

    # Train with teacher forcing
    best_model = transformer(train_dataloader, epoch, path_to_save_model, path_to_save_loss,
                             path_to_save_predictions, device)
    inference(path_to_save_predictions, forecast_window, test_dataloader, device, path_to_save_model, best_model)


if __name__ == "__main__":
    clean_directory()
    parser = argparse.ArgumentParser()
    parser.add_argument("--epoch", type=int, default=1000)
    parser.add_argument("--path_to_save_model", type=str, default="save_model/")
    parser.add_argument("--path_to_save_loss", type=str, default="save_loss/")
    parser.add_argument("--path_to_save_predictions", type=str, default="save_predictions/")
    parser.add_argument("--device", type=str, default="cpu")
    args = parser.parse_args()

    transformer_main(
        epoch=args.epoch,
        path_to_save_model=args.path_to_save_model,
        path_to_save_loss=args.path_to_save_loss,
        path_to_save_predictions=args.path_to_save_predictions,
        device=args.device,
    )
