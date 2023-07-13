# 编写人员：刘嘉豪
#
# 开发时间：2023/7/4 16:11
from flask import Flask, request, jsonify, render_template, make_response, send_file
import numpy as np
from PIL import Image, ImageDraw
from pyzbar import pyzbar
import Steganographic_algorithm_dir.MOPNA
import matplotlib.pyplot as plt
import base64
import io
np.set_printoptions(threshold=np.inf)

img = Image.open('D:\ALL_aboutSWU\cat_dog_lab\QR_embed\out_pic\img_out2.tif')
# 将二维数组，转换为一维数组
img_array1 = np.array(img)
img_array2 = img_array1.flatten()
print(img_array2)
