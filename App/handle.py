import torch
from src.device_getter import get_device
import torchvision.models as models
import torch.optim as optim
from src.ImagePreparator import ImagePreparator
from src.transfer_ranner import StyleTransferer

class ImageHandler():
    def __init__(self, content_image, style_image, path_user_folder, depth):
        obj = ImagePreparator(content_image, style_image)
        self.content_path = obj.create_image('content')
        self.style_path = obj.create_image('style')
        self.path_user_folder = path_user_folder
        self.model = models.vgg19(pretrained=True).features.to(get_device()).eval()
        self.input_img = self.content_path.clone()
        self.optimisator = optim.LBFGS([self.input_img], lr=1e-1)
        self.cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(get_device())
        self.cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(get_device())
        self.depth = depth

    def get_model(self):
        return self.model.to(get_device()).eval()
    
    def get_optimisator(self):
        return self.optimisator
    
    def get_cnn_normalization_mean(self):
        return self.cnn_normalization_mean
    
    def get_cnn_normalization_std(self):
        return self.cnn_normalization_std

    def get_content_path(self):
        return self.content_path
    
    def get_style_path(self):
        return self.style_path
    
    def get_path_user_folder(self):
        return self.path_user_folder
    
    def get_input_image(self):
        return self.input_img

    def run(self):
        print(self.get_input_image())
        num_steps = self.depth / 100 * 800
        return StyleTransferer(self.get_input_image()).run_style_transfer(
            self.get_model(),
            self.get_optimisator(),
            self.get_cnn_normalization_mean(),
            self.get_cnn_normalization_std(),
            self.get_content_path(),
            self.get_style_path(),
            self.get_path_user_folder(),
            num_steps=num_steps,
            style_weight=1e2,
            content_weight=1e-2
        )

