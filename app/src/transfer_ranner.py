import torch
from src.model_and_losses_getter import ModelGetter
from datetime import datetime
import os
from torchvision.utils import save_image

class StyleTransferer():
    def __init__(self, input_img):
        self.run = 0
        self.paths = []
        self.input_img = input_img
    
    def run_style_transfer(
        self,
        cnn,
        optimizer,
        normalization_mean,
        normalization_std,
        content_img,
        style_img,
        path_user_folder,
        num_steps=300,
        style_weight=1000000,
        content_weight=1
    ):
        self.path_user_folder = path_user_folder
        self.style_weight = style_weight
        self.content_weight = content_weight
        self.optimizer = optimizer
        model, style_losses, content_losses = ModelGetter().get_style_model_and_losses(cnn,
            normalization_mean, normalization_std, style_img, content_img)
        self.model = model
        self.style_losses = style_losses
        self.content_losses = content_losses
        self.input_img.requires_grad_(True)
        self.model.requires_grad_(False)

        self.start_time = datetime.now()
        if not os.path.exists(f"./{path_user_folder}"):
            os.makedirs(f"./{path_user_folder}")
        while self.run <= num_steps:
            def closure():
                # correct the values of updated input image
                with torch.no_grad():
                    self.input_img.clamp_(0, 1)

                optimizer.zero_grad()
                model(self.input_img)
                style_score = 0
                content_score = 0

                for sl in style_losses:
                    style_score += sl.loss
                for cl in content_losses:
                    content_score += cl.loss

                style_score *= style_weight
                content_score *= content_weight

                loss = style_score + content_score
                loss.backward()

                self.run += 1
                if self.run % (self.num_steps / 2) == 0:
                    path = os.path.join(f"{self.path_user_folder}", f"{self.start_time}_{self.run}.jpg")
                    self.paths.append(path)
                    save_image(self.input_img, path)

                return style_score + content_score

        self.optimizer.step(closure)
        with torch.no_grad():
            self.input_img.clamp_(0, 1)

        return self.paths

