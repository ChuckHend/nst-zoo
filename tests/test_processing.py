from nst_zoo.config import NSTConfig
from nst_zoo.image_processing import BaseProcessor
from torchvision import transforms
import torch
from PIL import Image


def test_preprocessing_postprocessing():
    """
    Test that postprocessing effectively reverses preprocessing

    Notes
    -----
    atol=1e-07 is the closest i can get for some reason
    https://discuss.pytorch.org/t/simple-way-to-inverse-transform-normalization/4821/16
    """

    fp = "nst_zoo/data/content/neckarfront_andreas_praefcke.jpg"
    bp = BaseProcessor()
    input_image = transforms.ToTensor()(Image.open(fp))
    preprocessed = bp.preprocess(input_image)
    postprocessed = bp.postprocess(preprocessed)

    assert torch.allclose(input_image, postprocessed, atol=1e-07)

