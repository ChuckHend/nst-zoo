from typing import List

import torch.nn as nn
import torch


class GramMatrix(nn.Module):
    """
    Base Gram Matrix calculation as per Gatys et al. 2015
    """
    def forward(self, input):
        b, c, h, w = input.size()
        F = input.view(b, c, h*w)
        G = torch.bmm(F, F.transpose(1, 2))
        G = G.div_(h*w)
        return G


class NormalizedGramMatrix(nn.Module):
    """
    I have found that normalizing the tensor before calculating the gram matrices leads to better convergence.
    """
    def forward(self, input):
        b, c, h, w = input.size()
        F = input.view(b, c, h*w)
        F = normalize_by_stddev(F)
        G = torch.bmm(F, F.transpose(1, 2))
        G = G.div_(h*w)
        return G


def normalize_by_stddev(tensor):
    """
    divides channel-wise by standard deviation of channel
    """
    channels = tensor.shape[1]
    stddev = tensor.std(dim=(0, 2)).view(1, channels, 1) + 10e-16
    return tensor.div(stddev)


def style_loss(
        generated_activations: List[torch.Tensor],
        style_gram_matrices: List[torch.Tensor]
) -> List[torch.Tensor]:
    """
    Calculate MSE of generated activations' Gram matrices vs target activation's Gram matrices

    Note: Function expects that you pass matrices of different shapes (see params)


    Parameters
    ----------
    - generated_activations: list of generated activations

    - style_gram_matrices: list of target GRAM MATRICES; this function expects that the target gram matrices do not need
      to be recalculated

    Returns
    -------
    list of loss corresponding with each activation that was passed
    """
    generated_gram_matrices = [GramMatrix()(i) for i in generated_activations]
    return [nn.MSELoss()(generated, target) for generated, target in zip(generated_gram_matrices, style_gram_matrices)]


def style_loss_normalized(
        generated_activations: List[torch.Tensor],
        style_gram_matrices: List[torch.Tensor]
) -> List[torch.Tensor]:
    """
    Does the same exact thing as style_loss, but uses NormalizedGramMatrix instead

    There's probably a better way to do this

    """
    generated_gram_matrices = [NormalizedGramMatrix()(i) for i in generated_activations]
    return [nn.MSELoss()(generated, target) for generated, target in zip(generated_gram_matrices, style_gram_matrices)]


class NSTLoss(nn.Module):
    """
    Utility class for calculating loss for Neural Style Transfer.

    Notes
    -----
    - Currently just supports style loss.
    - Stores target gram activations in self, to avoid re-calculating on every forward pass
    - Also stores style_weights and style_loss_fn in self for convenience
    """
    def __init__(
            self,
            style_targets=None,
            style_weights=None,
            style_loss_fn=None,
            content_targets=None,
            content_weights=None,
            content_loss_fn=None,
            alpha=None
    ):
        super(NSTLoss, self).__init__()
        self._init_style(style_targets, style_weights, style_loss_fn)
        self._init_content(content_targets, content_weights, content_loss_fn)
        self.alpha=alpha

    def _init_content(self, content_targets, content_weights, content_loss_fn):
        if content_targets or content_weights or content_loss_fn:
            raise NotImplementedError

    def _init_style(self, style_targets, style_weights, style_loss_fn):
        if style_targets or style_weights or style_loss_fn:
            if not (style_targets and style_weights and style_loss_fn):
                raise ValueError("If providing any style arguments, you mmust provide ALL style arguments")

        self.style_targets = style_targets
        self.style_weights = style_weights
        self.style_loss_fn = style_loss_fn

    def forward(self, generated_style_activations=None, generated_content_activations=None):
        """

        Parameters
        ----------
        generated_style_activations: activations from given layers in a given model
        generated_content_activations: activations from given layers in a given model


        Todo
        ----
        - Implement structured logging instead of print statements
        """

        content_losses = []
        style_losses = []

        if generated_style_activations:
            style_losses = self.style_loss_fn(generated_style_activations, self.style_targets)
            style_losses = [weight * loss for weight, loss in zip(self.style_weights, style_losses)]

        if generated_content_activations:
            content_losses = self.content_loss_fn(generated_content_activations, self.content_targets)
            content_losses = [weight * loss for weight, loss in zip(self.content_weights, content_losses)]

        if self.alpha:
            return (sum(content_losses) * self.alpha) + (sum(style_losses) * (1-self.alpha))
        print([float(i) for i in style_losses])
        return sum(content_losses) + sum(style_losses)

