#!/usr//local/bin/python
# -*- coding: UTF-8 -*-

import cv2
import re
import numpy as np
from PIL import Image


def get_operator(filepath, expand = False):
    shape = cv2.resize(cv2.imread(filepath), (69, 69))

    shape_gray = cv2.cvtColor(shape, cv2.COLOR_BGR2GRAY)

    # cv2.imwrite('data/shape_gray.png',shape_gray)

    _, shape_binary = cv2.threshold(shape_gray, 127, 255, cv2.THRESH_BINARY)

    _, contours, hierarchy = cv2.findContours(shape_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = contours[0]

    operator = np.zeros((69, 69))

    for point in contour:
        operator[point[0][0]][point[0][1]] = 1
        if expand:
            if point[0][0] > 0:
                operator[point[0][0] - 1][point[0][1]] = 1
            if point[0][0] < 68:
                operator[point[0][0] + 1][point[0][1]] = 1
            if point[0][1] > 0:
                operator[point[0][0]][point[0][1] - 1] = 1
            if point[0][1] < 68:
                operator[point[0][0]][point[0][1] + 1] = 1

    return operator

def best_match(image, operator):
    y_range, x_range = image.shape
    max_value, position = 0, (1, 1)

    for y in range(1, y_range - 1):
        for x in range(1, x_range - 1):
            if y + 69 > 185 or x + 69 > 315:
                continue
            block = image[(y - 1):(y + 68), (x - 1):(x + 68)]
            value = (block * operator).sum()
            if value > max_value:
                max_value = value
                position = (x, y)

    return position, max_value

def getBlockTop(filename):
    line = open(filename).read()
    pattern = re.compile(r'top:(\d+)px')
    top = pattern.findall(line)[0]
    return int(top)


def solvePuzzle(image, row, col, hack):

    # line = open(hack).read()

    line = hack

    pattern = re.compile(r'background-position:\s+(-?\d+)px\s+(-?\d+)px;\s+width:\s+(-?\d+)px;\s+height:\s+(-?\d+)px;')
    res = pattern.findall(line)

    im = Image.open(image)
    imbak = Image.open(image)
    offset_x = im.size[0] / row;
    offset_y = im.size[1] / col;

    for index in range(40):
        src_upperleft_x = index % row * offset_x
        src_upperleft_y = index / row * offset_y
        src_bottomright_x = src_upperleft_x + offset_x
        src_bottomright_y = src_upperleft_y + offset_y

        srcBox = (src_upperleft_x, src_upperleft_y, src_bottomright_x, src_bottomright_y)

        # print str(index) + " ======"
        # print srcBox

        des_upperleft_x = -int(res[index][0])
        des_upperleft_y = int(res[index][1])
        des_bottomright_x = des_upperleft_x + offset_x
        des_bottomright_y = des_upperleft_y + offset_y

        desBox = (des_upperleft_x, des_upperleft_y, des_bottomright_x, des_bottomright_y)

        # print desBox

        region = im.crop(desBox)

        imbak.paste(region, srcBox)

    return imbak

def getCanny(filename):
    img = np.array(Image.open(filename).convert('RGB'))
    img_blur = cv2.GaussianBlur(img, (3, 3), 0)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 250, 250)
    cv2.imwrite(filename,img_canny)


def shoot(image,Target,value,top):
    import cv2
    import numpy as np
    img_rgb = cv2.imread(image)
    # img_rgb = image
    img_rgb = img_rgb[top-10:top+70,:]
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where( res >= threshold)


    tmp = set()
    targets = []
    pt = zip(*loc[::-1])
    for pt in zip(*loc[::-1]):
        tmp.add(pt[0])

    cols = list(tmp)
    cols.sort()

    low = 0
    high = 0
    while high < len(cols) - 1:
        if cols[high] == cols[high+1] - 1:
            high += 1
        else:
            targets.append(cols[low + (high - low) / 2] + 34.5)
            low = high+1
            high = low
    print low + (high - low) / 2
    targets.append(cols[low + (high - low) / 2] + 34.5)

    return targets

def mkdir(path):
    import os
    # 去除左右两边的空格
    path=path.strip()
    # 去除尾部 \符号
    path=path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)

    return path

def save_img(path, file_name, url):
    import urllib2
    request = urllib2.Request(url)
    pic = urllib2.urlopen(request)
    save_file(path, file_name, pic.read())

def save_file(path, file_name, data):
    if data == None:
        return

    mkdir(path)
    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()
