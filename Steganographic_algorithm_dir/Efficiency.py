# 编写人员：刘嘉豪
#
# 开发时间：2022/6/9 16:54
import math
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def E(n):
    return ((2 * n + 1) * math.log(2, 2 * n + 1)) / 2 * n


def R(n):
    return (math.log(2, 2 * n + 1)) / n


# Peak Signal-to-Noise Ratio
def PSNR(image_array1, image_array2):
    # 输入为两个图像数组，一维，大小相同
    assert (np.size(image_array1) == np.size(image_array2))
    n = np.size(image_array1)
    assert (n > 0)
    MSE = 0.0
    for i in range(0, n):
        MSE += math.pow(int(image_array1[i]) - int(image_array2[i]), 2)
    MSE = MSE / n
    if MSE > 0:
        rtnPSNR = 10 * math.log10(255 * 255 / MSE)
    else:
        rtnPSNR = 100
    return rtnPSNR

def calculate_ssim(reference_image_path, test_image_path):
    # 打开参考图像和测试图像
    reference_image = Image.open(reference_image_path)
    test_image = Image.open(test_image_path)

    # 将图像转换为灰度图像
    reference_image_gray = reference_image.convert('L')
    test_image_gray = test_image.convert('L')

    # 将图像转换为NumPy数组
    reference_array = np.array(reference_image_gray)
    test_array = np.array(test_image_gray)

    # 计算SSIM指数
    ssim_value = ssim(reference_array, test_array)

    return ssim_value


