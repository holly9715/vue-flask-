import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import transforms
from torchvision.datasets import ImageFolder
import PIL
import numpy as np

criterion = nn.MSELoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)

class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()

        # 编码器
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1),  # 输出: 512x512x16
            nn.ReLU(True),
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),  # 输出: 256x256x32
            nn.ReLU(True),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),  # 输出: 128x128x64
            nn.ReLU(True),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),  # 输出: 64x64x128
            nn.ReLU(True),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),  # 输出: 32x32x256
            nn.ReLU(True),
        )

        # 解码器
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1),  # 输出: 64x64x128
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),  # 输出: 128x128x64
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1),  # 输出: 256x256x32
            nn.ReLU(True),
            nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, output_padding=1),  # 输出: 512x512x16
            nn.ReLU(True),
            nn.ConvTranspose2d(16, 3, kernel_size=3, stride=2, padding=1, output_padding=1),  # 输出: 1024x1024x3
            nn.Sigmoid(),  # 输出范围限制在 [0, 1] 之间
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

def image_to_tensor(image):
    # 定义图像预处理操作
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # 调整图片大小
        transforms.ToTensor(),          # 将图片转换为Tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 归一化
    ])
    # 读取图片
    # image = Image.open(image_path).convert('RGB')  # 确保图片是RGB模式
    # 应用预处理操作
    tensor_image = transform(image)
    # 将Tensor转换为[1, C, H, W]的形状，以匹配大多数模型的输入要求
    tensor_image = tensor_image.unsqueeze(0)
    return tensor_image

def detect_part(image):
    threshold = 1.315  # 这是一个示例阈值，可以根据实际情况调整
    criterion = nn.MSELoss()
    # 检测异常
    model=torch.load('App/model/model.pth')
    model.eval()
    image=image_to_tensor(image)
    # plt.imshow(image)
    print('检测种')
    with torch.no_grad():
        output = model(image)
        mse_loss = criterion(output, image)
        print(f'MSE Loss: {mse_loss:.4f}')
        if(mse_loss>threshold):
            return True
        else:
            return False
