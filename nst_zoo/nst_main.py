from nst_zoo.image_processing import BaseProcessor, noise_of_same_type
from nst_zoo.loss import GramMatrix, style_loss, NSTLoss, NormalizedGramMatrix, style_loss_normalized
from nst_zoo.models import *
from nst_zoo.optimization import optimize
from torch import optim


gatys_style_config = {
        "a": [0],
        "b": [0, 2],
        "c": [0, 2, 4],
        "d": [0, 2, 4, 8],
        "e": [0, 2, 4, 8, 12]
    }


def main():
    """
    Currently just loops through gatys-vgg19 layers to generate various style configurations

    1) Preprocess image in accordance with torchvision model subset

    2) Store target gram matrices once (only requires 1 forward pass, so calculating before optimizing
    safes on compute (since the generated image requires a forward pass on each iteration)

    3) Define loss function (MSE of gram matrices  at corresponding ReLU activation - generated vs target)
        - 200 iterations by default but can be adjusted with a kwarg
        - LBFGS optimization by default but all optimization methods are supported

    4) Reverse the preprocessing from step 1 and save an image in nst_zoo/data/generated/


    Todo
    ----
    - Implement dynamic importing to enable for easier configuration
        - Probably want something like this (example only includes 1 kwarg):

        import nst_zoo.models


        def main(model_config: str):
            model_fn = getattr(nst_zoo.models, model_config)
            model = model_fn(layers, pooling="avg")

    """
    bp = BaseProcessor()
    style_img = bp.preprocess("nst_zoo/data/style/vangogh_starry_night.jpg")
    noise_img = noise_of_same_type(style_img)

    for style_id, vgg_layers in gatys_style_config.items():
        model = vgg19(layers={"ReLU": vgg_layers}, pooling="avg")
        style_activations = get_activations(model, style_img)
        style_grams = [NormalizedGramMatrix()(i) for i in style_activations]
        nst_loss = NSTLoss(
            style_targets=style_grams,
            style_weights=[1/len(style_activations) for _ in style_activations],
            style_loss_fn=style_loss_normalized
        )
        optimizer = optim.LBFGS([noise_img], line_search_fn="strong_wolfe")
        generated_image = optimize(optimizer, noise_img, model, nst_loss)
        bp.save(generated_image, fp=f"nst_zoo/data/generated/vangogh_style_{style_id}.jpg")


if __name__ == '__main__':
    main()
