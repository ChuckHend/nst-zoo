from nst_zoo.config import NSTConfig
from nst_zoo.image_processing import BaseProcessor, noise_of_same_type
from nst_zoo.loss import GramMatrix, style_loss, NSTLoss, NormalizedGramMatrix
from nst_zoo import models, loss
from nst_zoo.models import get_activations
from nst_zoo.optimization import optimize
import torch


def main(nst_config: NSTConfig) -> None:
    """
    Currently just loops through gatys-vgg19 layers to generate various style configurations

    1) Preprocess image in accordance with torchvision model subset

    2) Store target gram matrices once (only requires 1 forward pass, so calculating before optimizing
    safes on compute (since the generated image requires a forward pass on each iteration)

    3) Define loss function (MSE of gram matrices  at corresponding ReLU activation - generated vs target)
        - 200 iterations by default but can be adjusted with a kwarg
        - LBFGS optimization by default but all optimization methods are supported

    4) Reverse the preprocessing from step 1 and save an image in nst_zoo/data/generated/
    """
    bp = BaseProcessor()
    style_img = bp.preprocess(nst_config.style_img)
    noise_img = noise_of_same_type(style_img)

    model_fn = getattr(models, nst_config.model)
    model = model_fn(layers=nst_config.layers, pooling=nst_config.pool)

    # single forward pass to save target activations
    target_style_activations = get_activations(model, style_img)
    gram_class = getattr(loss, nst_config.style_gram_class)
    target_style_grams = [gram_class()(i) for i in target_style_activations]

    nst_loss = NSTLoss(
        style_targets=target_style_grams,
        style_weights=nst_config.style_layer_weights,
        style_loss_fn=loss.style_loss,
        style_gram_class=gram_class
    )

    optimization_fn = getattr(torch.optim, nst_config.optimization_method)
    optimizer = optimization_fn([noise_img], **nst_config.optimization_kwargs)
    generated_image = optimize(optimizer, noise_img, model, nst_loss)

    bp.save(generated_image, fp=nst_config.output_filepath)


if __name__ == '__main__':

    # default is to evaluate all styles proposed by Gatys et al. 2015
    gatys_style_config = {
        "a": [0],
        "b": [0, 2],
        "c": [0, 2, 4],
        "d": [0, 2, 4, 8],
        "e": [0, 2, 4, 8, 12]
    }

    for style_id, cnn_layers in gatys_style_config.items():
        nst_config = NSTConfig(
            model="vgg19",
            pool="avg",
            style_img="nst_zoo/data/style/vangogh_starry_night.jpg",
            style_layers={"ReLU": cnn_layers},
            style_layer_weights=[1/len(cnn_layers) for _ in cnn_layers],
            style_gram_class="NormalizedGramMatrix",
            optimization_method="LBFGS",
            optimization_kwargs={"line_search_fn": "strong_wolfe"},
            output_filepath=f"nst_zoo/data/generated/vangogh_style_{style_id}.jpg"
        )
        main(nst_config)
