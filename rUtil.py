#!/usr//local/bin/python
# -*- coding: UTF-8 -*-

import cv2
import re
import numpy as np
from PIL import Image 

from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import os
import random
import urllib2

########################################################################
# crack settings
# path settings
contourFilePath = './rData/contour.dat'
storagePath = './jigsaw/tmpCrawlData'
bgPath = storagePath + '/bg'
shapePath = storagePath + '/shape'
originPath = storagePath + '/origin'
# filename settings
bgName = 'bg.png'
shapeName = 'shape.png'


# Ant settings
# ant message settings
token = '887f8cc91d2d3acabe646e064c250b89'
itemid = '137'
verifyWaitSec = 5
# url settings
getMobileURL = 'http://www.66yzm.com/api/admin/getmobile/linpai/' + token + '/itemid/' + itemid
getVerifyURLPrefix =  'http://www.66yzm.com/api/admin/shortmessage/linpai/' + token + '/itemid/' + itemid + '/mobile/'
blackURLPrefix = 'http://www.66yzm.com/api/admin/blacklist/linpai/' + token + '/itemid/ ' + itemid + ' /mobile/'
releasePrefix = 'http://www.66yzm.com/api/admin/release/linpai/' + token + '/itemid/ '+ itemid + '/mobile/'
releaseAllURL = 'http://www.66yzm.com/api/admin/releaseadd/linpai/' + token
# file settings
ledgerPath = "./rData/ledger.txt"


########################################################################
# crack util
def nwOperator():
    operator = np.zeros((91, 91))

    file = open(contourFilePath)
    lines = file.readlines()
    for line in lines:
        x = int(line.split(' ')[0])
        y = int(line.split(' ')[1])

        operator[x][y] = 1
        if False:
            if x > 0:
                operator[x - 1][y] = 1
            if x < 90:
                operator[x + 1][y] = 1
            if y > 0:
                operator[x][y - 1] = 1
            if y < 90:
                operator[x][y + 1] = 1

    return operator 

def best_match(image, operator):
    # cv2.imshow('Detected',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    size = 91
    y_range, x_range = image.shape
    max_value, position = 0, (1, 1)

    for y in range(1, y_range - 1):
        for x in range(1, x_range - 1):
            if y + size > y_range-1 or x + size > x_range-1:
                continue
            block = image[(y - 1):(y + size-1), (x - 1):(x + size-1)]
            value = (block * operator).sum()
            if value > max_value:
                max_value = value
                position = (x, y)

    return position, max_value

def getTrack(length):
    # '''
    # 根据缺口的位置模拟x轴移动的轨迹
    # '''
    pass
    list=[]
#     间隔通过随机范围函数来获得
    x=random.randint(1,3)
    while length-x>=5:
        list.append(x)
        length=length-x
        x=random.randint(3,8)
    for i in xrange(int(length)):
        list.append(1)
    return list

def getPosition(bgName):
    img = np.array(Image.open(bgName).convert('RGB'))
    img_blur = cv2.GaussianBlur(img, (3, 3), 0)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 250, 250)

    # operator = get_operator(shapeName)
    operator = nwOperator()
    (x, y), _ = best_match(img_canny, operator)
    return (x,y)

def getDefaultPosition():
	return getPosition(bgPath + '/'+ bgName)
########################################################################
# Ant util
# getAccount
def getAntMobile():
	req = urllib2.Request(getMobileURL) 
	response = urllib2.urlopen(req)
	mobile = response.read()[1:-1]
	return mobile

def releaseMobile(mobile):
	req = urllib2.Request(releasePrefix + mobile) 
	response = urllib2.urlopen(req)
	flag = response.read()
	print flag
	if (flag == "14"):
		print "[ANT][release success]" + str(mobile)
	else:
		print "[ANT ERROR][release failed]"

def releaseAll():
	req = urllib2.Request(releaseAllURL) 
	response = urllib2.urlopen(req)
	flag = response.read()
	print flag
	if (flag == "14"):
		print "[ANT][release all success]"
	else:
		print "[ANT ERROR][release failed]"

def getVerify(mobile):
	message = ""
	flag = 0
	start = time.time()
	while flag == 0:
		req = urllib2.Request(getVerifyURLPrefix + str(mobile)) 
		response = urllib2.urlopen(req)
		message = response.read()
		if (time.time() - start > 30):
			black(mobile)
			releaseMobile(mobile)
			return "FAIL"

		if message == "17":
			flag = 0
			time.sleep(verifyWaitSec)
			print "[ANT][try fetching message]"
		else:
			flag = 1
		
	print "[ANT][receive message successfully]"

	try:
		verify = re.search(r'您的手机验证码：(\d+),', message, re.M|re.I).group(1)
	except:
		return "FAIL"
	else:
		if len(verify) != 6:
			print "[ANT ERROR][extract verify failed]"
			return "FAIL"
		else:
			print "[ANT][extract verify success]"
			print verify
			return verify

def black(mobile):
	req = urllib2.Request(blackURLPrefix + str(mobile)) 
	response = urllib2.urlopen(req)
	message = response.read()
	print message
	return message
########################################################################
# file util
def saveAccount(mobile, passwd):
    file=open(ledgerPath, "a")
    file.write(mobile + " " + passwd + '\n')
    file.flush()
    file.close()

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

def save_bg(url):
	save_img(bgPath, bgName, url)

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




