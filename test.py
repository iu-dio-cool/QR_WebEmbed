# 编写人员：刘嘉豪
#
# 开发时间：2023/7/4 16:11
from flask import Flask, request, jsonify, render_template, make_response, send_file
import numpy as np
from PIL import Image, ImageDraw
from pyzbar import pyzbar
import Steganographic_algorithm_dir.Efficiency
import matplotlib.pyplot as plt
import base64
import io
np.set_printoptions(threshold=np.inf)
qrCode1 = 'D:\ALL_aboutSWU\cat_dog_lab\QR_embed\in_pic\qrcode_v3_ec0_bs5_bd4.png'
qrCode2 = 'D:\ALL_aboutSWU\cat_dog_lab\QR_embed\out_pic\\1to3.png'

if __name__ == '__main__':

    # 打开图像
    image1 = Image.open(qrCode1).convert("L")
    pixel_values1 = np.array(image1).flatten()
    image2 = Image.open(qrCode2).convert("L")
    pixel_values2 = np.array(image2).flatten()
    # print(pixel_values2)
    PSNR = Steganographic_algorithm_dir.Efficiency.PSNR(pixel_values1,pixel_values2)

    SSIM = Steganographic_algorithm_dir.Efficiency.calculate_ssim(qrCode1,qrCode2)
    print('PSNR=',PSNR,'SSIM = ',SSIM)