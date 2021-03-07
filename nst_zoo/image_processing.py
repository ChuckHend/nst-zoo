from .config import CUDA

from typing import Union

import torch
from torchvision import transforms
from torchvision.utils import save_image
from torch.autograd import Variable
from PIL import Image


class BaseProcessor:
    """
    Handle preprocessing/postprocessing in accordance with model-zoo ImageNet subset

    Notes
    -----
    Oddly enough, the image scale size seems to have a large effect on the output
    """
    preprocessing_steps = [
        transforms.Scale(256),  # arbitrarily chosen
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ]

    postprocessing_steps = [
        transforms.Normalize(
            mean=[-0.485 / 0.229, -0.456 / 0.224, -0.406 / 0.225],
            std=[1 / 0.229, 1 / 0.224, 1 / 0.225]
        )
    ]

    def preprocess(self, img: Union[str, torch.Tensor, Variable]) -> Variable:
        if isinstance(img, str):
            img = transforms.ToTensor()(Image.open(img))

        tensor = Variable(
            transforms.Compose(self.preprocessing_steps)(img).unsqueeze(0)
        )

        if torch.cuda.is_available():
            return tensor.cuda(device=CUDA)
        return tensor

    def postprocess(self, img: Variable) -> Variable:
        return transforms.Compose(self.postprocessing_steps)(img)

    def save(self, img, fp, postprocess=True):
        if postprocess:
            img = self.postprocess(img)
        save_image(img, fp)


def noise_of_same_type(tensor):
    if torch.cuda.is_available():
        return Variable(
            torch.randn(size=tensor.size(), dtype=tensor.dtype, device=CUDA),
            requires_grad=True
        )
    return Variable(
        torch.randn(size=tensor.size(), dtype=tensor.dtype),
        requires_grad=True
    )