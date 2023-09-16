# 编写人员：刘嘉豪
#
# 开发时间：2023-08-30 21:46
from PIL import Image
import numpy as np
import math


def LSB_EMBED(image, secret_string):
    image1 = Image.open(image)
    # 转换为灰度图像
    if image1.mode == "L":
        pass
    else:
        print("图像不是灰度图像")
        image1 = image1.convert("L")
    # 获取图像像素值
    image_array = np.array(image1)

    width, height = image_array.shape
    if len(secret_string) > width * height:
        raise Exception("消息太长，无法嵌入到图像中。")
    index = 0
    flattened_image = image_array.flatten()
    for i in range(len(flattened_image)):
        pixel_value = flattened_image[i]
        # for bit_index in range(8):  # 遍历每个字节的位
        if index < len(secret_string):
            pixel_value = pixel_value & ~1 | int(secret_string[index])
            index += 1

        flattened_image[i] = pixel_value
    output_image = flattened_image.reshape(width,height)
    output_image = Image.fromarray(output_image, mode="L")



    return output_image


def LSB_EXTRACT(image_input):
    # 判断文件类型
    if isinstance(image_input, str):
        # 如果输入是字符串，假定它是文件路径，使用image.open打开图像
        image_path = Image.open(image_input).convert("L")  # 将图像转换为灰度图
        image_array = np.array(image_path)
    elif isinstance(image_input, np.ndarray):
        # 如果输入是NumPy数组，直接返回该数组
        image_array = image_input
        pass
    else:
        # 如果输入既不是字符串也不是NumPy数组，抛出异常或者返回默认值，根据需要自行处理
        raise ValueError("Unsupported input type")

    binary_message = ''
    for pixel_value in image_array.flatten():
        binary_message += str(pixel_value & 1)

    # 将二进制消息转换为二进制数组
    binary_message_array = np.array([int(bit) for bit in binary_message], dtype=np.uint8)

    return binary_message_array


if __name__ == '__main__':
    # 数据源
    qrCode1 = 'D:\ALL_aboutSWU\cat_dog_lab\QR_embed\out_pic\\1to3.png'
    # 信息载体
    qrCode2 = 'D:\ALL_aboutSWU\cat_dog_lab\QR_embed\in_pic\qrcode_v5_ec0_bs5_bd4.png'
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
    # s_data2 = s_data.reshape(145, 145)
    img_out = LSB_EMBED(qrCode2, s_data)
    img_out.save('D:\ALL_aboutSWU\cat_dog_lab\QR_embed\out_pic\\1to3to5.png', mode="L")
    img_EXTRACT = LSB_EXTRACT('D:\ALL_aboutSWU\cat_dog_lab\QR_embed\out_pic\\1to3to5.png')
    img_EXTRACT = img_EXTRACT[:185*185]*255
    img_EXTRACT1 = img_EXTRACT.reshape(185, 185)
    img_EXTRACT2 = Image.fromarray(img_EXTRACT1)
    img_EXTRACT2.show()

    img_EXTRACT3 = LSB_EXTRACT(img_EXTRACT)
    img_EXTRACT3 = img_EXTRACT3[:165*165]*255
    img_EXTRACT4 = img_EXTRACT3.reshape(165, 165)
    img_EXTRACT4 = Image.fromarray(img_EXTRACT4)
    img_EXTRACT4.show()
    pass
    # img_out
