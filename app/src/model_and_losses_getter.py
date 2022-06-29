from src.device_getter import get_device
import torch.nn as nn
from src.Normalizator import Normalization
import src.losses as losses

class ModelGetter():
    def __init__(self):
        self.default_content_layers = ['conv_5']
        self.default_style_layers = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']
    
    def get_style_model_and_losses(
        self,
        cnn,
        normalization_mean,
        normalization_std,
        style_img,
        content_img,
        content_layers = None,
        style_layers = None
    ):
        normalization = Normalization(normalization_mean, normalization_std).to(get_device())
        content_losses = []
        style_losses = []

        model = nn.Sequential(normalization)
        i = 0
        for layer in cnn.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = 'conv_{}'.format(i)
            elif isinstance(layer, nn.ReLU):
                name = 'relu_{}'.format(i)
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = 'pool_{}'.format(i)
            elif isinstance(layer, nn.BatchNorm2d):
                name = 'bn_{}'.format(i)
            else:
                raise RuntimeError('Unrecognized layer: {}'.format(layer.__class__.__name__))

            model.add_module(name, layer)

            if content_layers is None:
                content_layers = self.default_content_layers
            if name in content_layers:
                target = model(content_img).detach()
                content_loss = losses.ContentLoss(target)
                model.add_module("content_loss_{}".format(i), content_loss)
                content_losses.append(content_loss)
            
            if style_layers is None:
                style_layers = self.default_style_layers
            if name in style_layers:
                target_feature = model(style_img).detach()
                style_loss = losses.StyleLoss(target_feature)
                model.add_module("style_loss_{}".format(i), style_loss)
                style_losses.append(style_loss)

        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], losses.ContentLoss) or isinstance(model[i], losses.StyleLoss):
                break

        model = model[:(i + 1)]

        return model, style_losses, content_losses