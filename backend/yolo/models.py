import torch
from torch import nn
from torchvision.models import yolov5


class CustomYOLOv5(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.model = yolov5(num_classes=num_classes)

    def forward(self, x):
        return self.model(x)

def load_weights(model, weights_path):
    state_dict = torch.load(weights_path, map_location=torch.device('cpu'))
    model.load_state_dict(state_dict['model'])