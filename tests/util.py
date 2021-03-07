from PIL import Image
from nst_zoo.image_processing import BaseProcessor
from torchvision import transforms


def get_content_img():
    return Image.open("nst_zoo/data/content/neckarfront_andreas_praefcke.jpg")


def get_style_img():
    return Image.open("nst_zoo/data/style/vangogh_starry_night.jpg")


def get_preprocessed_content():
    bp = BaseProcessor()
    return bp.preprocess(transforms.ToTensor()(get_content_img()))


def get_preprocessed_style():
    bp = BaseProcessor()
    return bp.preprocess(transforms.ToTensor()(get_style_img()))
