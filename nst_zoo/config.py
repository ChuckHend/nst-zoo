import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict


CUDA = int(os.getenv("CUDA", 0))


@dataclass
class NSTConfig:
    # model
    model: str = "vgg19"
    pool: str = "avg"

    # style
    style_img: Optional[str] = None
    style_layers: Optional[Dict] = field(default_factory=lambda: {})
    style_layer_weights: Optional[List[float]] = field(default_factory=lambda: [None])

    # content
    content_img: Optional[str] = None
    content_layers: Optional[Dict] = field(default_factory=lambda: {})
    alpha: Optional[float] = None  # total_loss = alpha*content_loss + (1-alpha)*style_loss

    # loss
    style_gram_class: Optional[str] = None

    # optimization
    optimization_method: str = "LBFGS"
    optimization_kwargs: Dict = field(default_factory=lambda: {"line_search_fn": "strong_wolfe"})

    output_filepath: str = ""

    def __post_init__(self):
        """
        combine style_image and content_image names if output_filepath is not specified
        """
        self.layers = {**self.style_layers, **self.content_layers}

        if not self.output_filepath:
            content_name = os.path.basename(self.content_image).split('.')[0]
            style_name = os.path.basename(self.style_image).split('.')[0]
            self.output_filepath = f"nst_zoo/data/generated/{content_name}_{style_name}.jpg"
