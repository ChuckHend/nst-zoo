### nst_zoo
(work in progress)

- Does the world really need another repo for neural style transfer?
    - Probably not, but I think this one will be unique in that it will eventually support all combinations of:
        - torchvision Models
        - Optimization Methods
        - Weighting Schemes
        - Loss functions & normalization methods
        - Pooling replacement ("avg" vs "max")
        
In addition to an output image, I believe there will be value in storing the following for each trial:
- Loss history
- Analysis of Gram Matrices (some seem to be more instable than others)  


Inspired by [Gatys et al. 2015](https://arxiv.org/abs/1508.06576)