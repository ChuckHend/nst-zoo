from nst_zoo.loss import NSTLoss
from nst_zoo.models import get_activations
from torch import optim
from torch.optim.lbfgs import LBFGS
from functools import singledispatch


@singledispatch
def optimize(optimizer: optim.Optimizer, noise_img, model, nst_loss: NSTLoss, epochs=200):
    epoch = 0
    while epoch < epochs:
        optimizer.zero_grad()
        activations = get_activations(model, noise_img)
        loss = nst_loss(style_activations=activations)
        loss.backward()
        epoch += 1
        optimizer.step()
    return noise_img


@optimize.register(LBFGS)
def _(optimizer: optim.Optimizer, noise_img, model, nst_loss: NSTLoss, epochs=200):
    epoch = 0
    while epoch < epochs:
        def closure():
            nonlocal epoch
            optimizer.zero_grad()
            activations = get_activations(model, noise_img)
            loss = nst_loss(generated_style_activations=activations)
            loss.backward()
            epoch += 1
            return loss
        optimizer.step(closure)
    return noise_img
