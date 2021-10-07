from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import json
import torch
import torchvision.transforms as T
from torchvision.io import read_image
import torch.nn as nn
from torchvision.models import resnet50

device = 'cuda' if torch.cuda.is_available() else 'cpu'


class Predictor(nn.Module):

    def __init__(self):
        super().__init__()
        self.resnet50 = resnet50(pretrained=True, progress=True).eval()
        self.transforms = nn.Sequential(
            T.Resize([256, ]),  # We use single int value inside a list due to torchscript type restrictions
            T.CenterCrop(224),
            T.ConvertImageDtype(torch.float),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            x = self.transforms(x)
            y_pred = self.resnet50(x)
            return y_pred.argsort(dim=1, descending=True)[0, :5]

class ClassPredictor:
    def __init__(self, img_path):
        self.predictor = Predictor().to(device)
        self.scripted_predictor = torch.jit.script(self.predictor).to(device)
        self.img = read_image(str(Path('media') / img_path))
        # img = T.ToPILImage()(self.img.to('cpu'))
        # plt.imshow(np.asarray(img))
        # plt.show()
        self.img = torch.unsqueeze(self.img, 0).to(device)

    def getTag(self):
        self.res = self.predictor(self.img)
        self.res_scripted = self.scripted_predictor(self.img)

        with open(Path('main/otherFunctions/assets') / 'imagenet_class_index.json', 'r') as labels_file:
        # with open('assets/imagenet_class_index.json', 'r') as labels_file:
            labels = json.load(labels_file)

        res = []
        for i, (pred, pred_scripted) in enumerate(zip(self.res, self.res_scripted)):
            assert pred == pred_scripted
            res.append(labels[str(pred.item())][1])
            print(f"class Prediction for img: {labels[str(pred.item())][1]}")
        return res


if __name__ == '__main__':
    class_predictor = ClassPredictor('dog1.jpg')
    tag = class_predictor.getTag()

