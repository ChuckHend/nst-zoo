from torchvision import models
from torch import nn
import torch
from collections import Counter
from .config import CUDA


def validate_layers(model: nn.Module, layers:dict):
    """
    Assert all of the following things:

    1) Layers are provided as an argument
    2) All layers provided exist in model
    3) All layers have, at least, the maximum layer-index provided

    """
    if not layers:
        raise ValueError("You must specify which layers will be used for the loss.")

    layer_counts = Counter([type(module).__name__ for _, module in model.named_modules()])
    invalid_layers = set(layers.keys()).difference(layer_counts.keys())
    if invalid_layers:
        raise ValueError(f"{invalid_layers} not found in {type(model).__name__}")

    invalid_indices = [k for k, v in layer_counts.items() if k in layers.keys() and  max(layers[k]) - 1 > v]

    if invalid_indices:
        raise IndexError(f"{invalid_indices} indices are too large for {type(model).__name__} layers")


def _add_hooks_to_model(model: nn.Module, layers: dict) -> nn.Module:
    """
    Utility function

    """
    layer_counter = {k: 0 for k in layers.keys()}
    for _, module in model.named_modules():
        layer_name = type(module).__name__
        if layer_name in layers.keys():
            if layer_counter[layer_name] in layers[layer_name]:
                module.register_forward_hook(_hook)
            layer_counter[layer_name] += 1
    return model


def _hook(module, input, output):
    setattr(module, "_value_hook", output)


def _replace_max_with_avg(model):
    for i, named_module in enumerate(model.named_modules()):
        name, module = named_module
        if type(module).__name__ == "MaxPool2d":
            replacement = torch.nn.AvgPool2d(
                kernel_size=module.kernel_size,
                stride=module.stride,
                padding=module.padding,
            )
            attr, index = name.split('.')
            getattr(model, attr)[int(index)] = replacement
    return model


def _nst_pipeline(model, layers, pooling):
    """
    todo - replace pooling if kwarg
    """
    validate_layers(model, layers)
    if pooling=="avg":
        model = _replace_max_with_avg(model)

    model = _add_hooks_to_model(model, layers)
    for param in model.parameters():
        param.requires_grad = False
    if torch.cuda.is_available():
        model.cuda(device=CUDA)
    return model


def get_activations(model, image):
    """
    do a forward pass (ignore the output), then return the _value_hooks
    """
    _ = model(image)
    return [getattr(module, "_value_hook") for name, module in model.named_modules() if hasattr(module, "_value_hook")]


def alexnet(layers, pooling="avg"):
    return _nst_pipeline(models.alexnet(pretrained=True), layers, pooling)


def densenet121(layers, pooling="avg"):
    return _nst_pipeline(models.densenet121(pretrained=True), layers, pooling)


def densenet161(layers, pooling="avg"):
    return _nst_pipeline(models.densenet161(pretrained=True), layers, pooling)


def densenet169(layers, pooling="avg"):
    return _nst_pipeline(models.densenet169(pretrained=True), layers, pooling)


def densenet201(layers, pooling="avg"):
    return _nst_pipeline(models.densenet201(pretrained=True), layers, pooling)


def googlenet(layers, pooling="avg"):
    return _nst_pipeline(models.googlenet(pretrained=True), layers, pooling)


def inception_v3(layers, pooling="avg"):
    return _nst_pipeline(models.inception_v3(pretrained=True), layers, pooling)


def mnasnet0_5(layers, pooling="avg"):
    return _nst_pipeline(models.mnasnet0_5(pretrained=True), layers, pooling)


def mnasnet0_75(layers, pooling="avg"):
    return _nst_pipeline(models.mnasnet0_75(pretrained=True), layers, pooling)


def mnasnet1_0(layers, pooling="avg"):
    return _nst_pipeline(models.mnasnet1_0(pretrained=True), layers, pooling)


def mnasnet1_3(layers, pooling="avg"):
    return _nst_pipeline(models.mnasnet1_3(pretrained=True), layers, pooling)


def mobilenet_v2(layers, pooling="avg"):
    return _nst_pipeline(models.mobilenet_v2(pretrained=True), layers, pooling)


def resnet101(layers, pooling="avg"):
    return _nst_pipeline(models.resnet101(pretrained=True), layers, pooling)


def resnet152(layers, pooling="avg"):
    return _nst_pipeline(models.resnet152(pretrained=True), layers, pooling)


def resnet18(layers, pooling="avg"):
    return _nst_pipeline(models.resnet18(pretrained=True), layers, pooling)


def resnet34(layers, pooling="avg"):
    return _nst_pipeline(models.resnet34(pretrained=True), layers, pooling)


def resnet50(layers, pooling="avg"):
    return _nst_pipeline(models.resnet50(pretrained=True), layers, pooling)


def resnext101_32x8d(layers, pooling="avg"):
    return _nst_pipeline(models.resnext101_32x8d(pretrained=True), layers, pooling)


def resnext50_32x4d(layers, pooling="avg"):
    return _nst_pipeline(models.resnext50_32x4d(pretrained=True), layers, pooling)


def shufflenet_v2_x0_5(layers, pooling="avg"):
    return _nst_pipeline(models.shufflenet_v2_x0_5(pretrained=True), layers, pooling)


def shufflenet_v2_x1_0(layers, pooling="avg"):
    return _nst_pipeline(models.shufflenet_v2_x1_0(pretrained=True), layers, pooling)


def shufflenet_v2_x1_5(layers, pooling="avg"):
    return _nst_pipeline(models.shufflenet_v2_x1_5(pretrained=True), layers, pooling)


def shufflenet_v2_x2_0(layers, pooling="avg"):
    return _nst_pipeline(models.shufflenet_v2_x2_0(pretrained=True), layers, pooling)


def squeezenet1_0(layers, pooling="avg"):
    return _nst_pipeline(models.squeezenet1_0(pretrained=True), layers, pooling)


def squeezenet1_1(layers, pooling="avg"):
    return _nst_pipeline(models.squeezenet1_1(pretrained=True), layers, pooling)


def vgg11(layers, pooling="avg"):
    return _nst_pipeline(models.vgg11(pretrained=True), layers, pooling)


def vgg11_bn(layers, pooling="avg"):
    return _nst_pipeline(models.vgg11_bn(pretrained=True), layers, pooling)


def vgg13(layers, pooling="avg"):
    return _nst_pipeline(models.vgg13(pretrained=True), layers, pooling)


def vgg13_bn(layers, pooling="avg"):
    return _nst_pipeline(models.vgg13_bn(pretrained=True), layers, pooling)


def vgg16(layers, pooling="avg"):
    return _nst_pipeline(models.vgg16(pretrained=True), layers, pooling)


def vgg16_bn(layers, pooling="avg"):
    return _nst_pipeline(models.vgg16_bn(pretrained=True), layers, pooling)


def vgg19(layers, pooling="avg"):
    return _nst_pipeline(models.vgg19(pretrained=True), layers, pooling)


def vgg19_bn(layers, pooling="avg"):
    return _nst_pipeline(models.vgg19_bn(pretrained=True), layers, pooling)


def wide_resnet101_2(layers, pooling="avg"):
    return _nst_pipeline(models.wide_resnet101_2(pretrained=True), layers, pooling)


def wide_resnet50_2(layers, pooling="avg"):
    return _nst_pipeline(models.wide_resnet50_2(pretrained=True), layers, pooling)


