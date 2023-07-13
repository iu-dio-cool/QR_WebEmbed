# 编写人员：刘嘉豪
#
# 开发时间：2023/6/30 12:07
from flask import Flask, request, jsonify, render_template, make_response, send_file
import numpy as np
from PIL import Image, ImageDraw
from pyzbar import pyzbar
import Steganographic_algorithm_dir.MOPNA
import matplotlib.pyplot as plt
import base64
import io

np.set_printoptions(threshold=np.inf)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# 功能1：隐藏
@app.route('/hide', methods=['POST'])
def hide():
    # 获取上传的两个二维码图片文件 qr_code1要隐藏二维码数据 qr_code2隐藏载体
    qr_code1 = request.files['qrCode1']
    qr_code2 = request.files['qrCode2']

    # 执行隐藏操作，生成新的二维码图片
    # 打开图像
    image = Image.open(qr_code1)
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
    # print("要隐藏的数据长度" + str(s_data) + str(len(s_data)))

    # 选取隐藏算法:
    img_out, recover_d_array = Steganographic_algorithm_dir.MOPNA.sole_fun(qr_code2, s_data)
    '''
        因为像素值超过255 所以保存tif图片
        打开的和保存打开的 不一样，image.show() 因为位深度，所以需要astype(np.uint8)
    '''

    # img_out = img_out.reshape(shape1, shape2)
    img_out = Image.fromarray(img_out.astype('uint8'))
    # 将图片转换为Base64编码
    image_data = io.BytesIO()
    img_out.save(image_data, format='png')
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    image_base64 = image_base64.replace('=', '')

    # 返回Base64编码的图片数据
    return jsonify({'imageData': image_base64})

# 打开tif图，因为MOPNA算法的像素值有超过255的
# 功能2：分割
@app.route('/extract', methods=['POST'])
def split():
    # 获取上传的图片文件
    input_image = request.files['inputImage']
    # 获取上传的版本
    qrVersion = request.form['qrVersion']
    print(qrVersion, type(qrVersion))
    qrVersion = int(qrVersion)
    # 开始实验
    img = Image.open(input_image)
    # 将二维数组，转换为一维数组
    img_array1 = np.array(img)
    img_array2 = img_array1.flatten()
    # 执行分割操作，生成两张二维码图片
    # 读取分割后的二维码图片数据
    shape1 = shape2 = (qrVersion * 4 + 17) * 5 + 4 * 5 * 2
    recover_d_array = Steganographic_algorithm_dir.MOPNA.extract_data_from_image(img_array2, shape1, shape2)
    img_out = recover_d_array
    print(len(img_out), 'len=', len(recover_d_array), shape1)
    img_out = img_out * 255
    img_out = img_out.reshape(shape1, shape2)
    img_out = img_out.astype(np.uint8)
    img_out = Image.fromarray(img_out)
    img_out = img_out.convert('L')
    image_data = io.BytesIO()
    img_out.save(image_data, format='PNG')
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    image_base64 = image_base64.replace('=', '')
    return jsonify({'imageData': image_base64})


if __name__ == '__main__':
    # 通过url_map可以查看整个flask中的路由信息
    print(app.url_map)
    app.run(debug=True, port=3089)
