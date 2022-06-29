import torchvision.transforms as transforms
import torch
from PIL import Image
from src.device_getter import get_device

class ImagePreparator():
    def __init__(self, content_path, style_path):
        self.content_path = content_path
        self.style_path = style_path
        self.image_size = 512 if torch.cuda.is_available() else 128
        self.tarnsformer = self._create_loader()

    def _create_loader(self):
        return transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.CenterCrop(self.image_size),
            transforms.ToTensor()])

    def create_image(self, type='content'):
        if (type == 'content'):
            image = Image.open(self.content_path)
        elif (type == 'style'):
            image = Image.open(self.style_path)
        else:
            print('Error')
        image = self.tarnsformer(image).unsqueeze(0)
        return image.to(get_device(), torch.float)
