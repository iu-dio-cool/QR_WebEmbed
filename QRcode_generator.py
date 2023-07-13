# 编写人员：刘嘉豪
#
# 开发时间：2023/7/2 9:38

import qrcode


def generate_qrcode(data, version, error_correction, box_size, border):
    """
    生成二维码并保存为图像文件
    :param data: 要编码的数据
    :param version: 版本号
    :param error_correction: 纠错级别
    :param box_size: 盒子大小
    :param border: 边框大小
    """
    # 创建QRCode对象
    qr = qrcode.QRCode(version, error_correction, box_size, border)

    # 添加数据
    qr.add_data(data)

    # 编码数据
    qr.make()

    # 创建图像
    image = qr.make_image(fill_color="black", back_color="white")
    filename = 'D:\ALL_aboutSWU\cat_dog_lab\QR_embed\in_pic\\'
    filename = filename + f"qrcode_v{version}_ec{error_correction}_bs{box_size}_bd{border}.png"
    # 保存图像
    image.save(filename)


# 示例用法
data = "Hello, World!"  # 要编码的数据
version = 1  # 版本号
error_correction = qrcode.constants.ERROR_CORRECT_M  # 纠错级别
box_size = 5  # 盒子大小
border = 4  # 边框大小

generate_qrcode(data,version,error_correction,box_size,border)
