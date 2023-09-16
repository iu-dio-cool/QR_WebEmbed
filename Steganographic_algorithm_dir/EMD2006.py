# 编写人员：刘嘉豪
#
# 开发时间：2023-08-28 20:53
from PIL import Image
import numpy as np
import math


def EMD06_EMBED(image, secret_string, n=4, k=3, image_file_name=''):
    # image:输入的图像
    # image_file_name:传入的图像文件名（带全路径）
    # n为一组像素的数量,我理解n只能取2，4,8,16等值，取其他值会导致嵌入的bit数不好确定
    image1 = Image.open(image)
    # 转换为灰度图像
    if image1.mode == "L":
        pass
    else:
        print("图像不是灰度图像")
        image1 = image1.convert("L")
    # 获取图像像素值
    image_array = np.array(image1)
    # 一维化
    image_array = image_array.flatten()
    assert (n == 2 or n == 4 or n == 8 or n == 16 or n == 32 or n == 64)
    moshu = 2 * n + 1  # 模数的底
    # 分成n个像素一组
    num_pixel_groups = math.ceil(image_array.size / n)
    pixels_group = np.zeros((num_pixel_groups, n))
    i = 0
    while (i < num_pixel_groups):
        for j in range(0, n):
            if (i * n + j < image_array.size):
                pixels_group[i, j] = image_array[i * n + j]
        i = i + 1
    # 每一个像素组计算出一个fG值
    fG_array = np.zeros(num_pixel_groups)
    for i in range(0, num_pixel_groups):
        fG = 0
        for j in range(0, n):
            fG += (j + 1) * pixels_group[i, j]
        fG_array[i] = fG % moshu
    # -----------------------------------------------------------------------------------
    # 从待嵌入bit串数据中取出m个比特，作为一组。m=math.log((2*n),2),以2为底的对数
    m = int(math.log((2 * n), 2))
    # 分组
    num_secret_groups = math.ceil(secret_string.size / m)
    secret_group = np.zeros((num_secret_groups, m))
    i = 0
    while (i < num_secret_groups):
        for j in range(0, m):
            if (i * m + j < secret_string.size):
                secret_group[i, j] = secret_string[i * m + j]
        i = i + 1
    # -----------------------------------------------------------------------------------

    # 一组pixels_group嵌入一组secret_group的信息，多了不能嵌入,最后一组pixel不用于嵌入以防止错误
    assert (np.shape(secret_group)[0] <= np.shape(pixels_group)[0] - 1)
    # 每一组secret_group计算得到一个d值，d为（2n+1）进制的一个数
    d_array = np.zeros(num_secret_groups)
    for i in range(0, num_secret_groups):
        # d代表一个（2n+1）进制的一个数
        d = 0
        for j in range(0, m):
            d += secret_group[i, j] * (2 ** (m - 1 - j))
            d_array[i] = d
    # -----------------------------------------------------------------------------------
    # 开始进行嵌入
    embedded_pixels_group = pixels_group.copy()
    for i in range(0, num_secret_groups):
        d = d_array[i]
        fG = fG_array[i]
        j = int(d - fG) % moshu
        if (j > 0):  # 如果为0的话，则不进行修改
            if (j <= n):
                embedded_pixels_group[i, j - 1] += 1
            else:
                embedded_pixels_group[i, (2 * n + 1 - j) - 1] += -1

    # 输出图像
    img_out = embedded_pixels_group.flatten()
    '''
     1！！！！！！！！！
    '''
    img_out = img_out[:256 * 256]  # 取前面的pixel
    # 重组图像
    img_out = img_out.reshape(256, 256)

    return img_out

# 提取算法


if __name__ == '__main__' :
    qrCode1 = 'D:\ALL_aboutSWU\cat_dog_lab\QR_embed\in_pic\qrcode_v1_ec0_bs5_bd4.png'
    qrCode2 = 'D:\ALL_aboutSWU\cat_dog_lab\QR_embed\in_pic\qrcode_v3_ec0_bs5_bd4.png'
    # 打开图像
    image = Image.open(qrCode1)
    # 转换为灰度图像
    if image.mode == "L":
        pass
    else:
        print("图像不是灰度图像")
        image = image.convert("L")
    # 获取图像像素值
    pixel_values = np.array(image)
    # 获取图像大小
    width, height = image.size
    # 隐藏数据
    od_pixel_values = pixel_values.flatten()
    # 二值化
    binary_pixelValues = np.where(od_pixel_values >= 128, 1, 0)
    # 拼接数据
    s_data = binary_pixelValues
    img_out = EMD06_EMBED(qrCode2, s_data)
