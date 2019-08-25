#!/usr//local/bin/python
# -*- coding: UTF-8 -*-

########################################################################
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random

from rUtil import save_bg
from rUtil import getDefaultPosition
from rUtil import getTrack

from rUtil import getAntMobile
from rUtil import getVerify
from rUtil import black
from rUtil import saveAccount
from rUtil import releaseAll
from rUtil import releaseMobile
########################################################################
class Actions(ActionChains):
    def wait(self, time_s):
        self._actions.append(lambda: time.sleep(time_s))
        return self
# basic settings
robberURL = 'http://www.youku.com/' # yk chou sb

# selenim settings
chromedriver = '/usr/local/Cellar/chromedriver/2.36/bin/chromedriver'

# rigistor robber
# account & passwd settings
password = 'sxl520'

#######################################################################
# registor process
# intial webbrowser
os.environ["webdriver.chrome.driver"] = chromedriver
webbrowser = webdriver.Chrome(chromedriver)
webbrowser.delete_all_cookies()

def process(webbrowser):
	# get web
	webbrowser.get(robberURL)

	# wait for loading
	time.sleep(2)

	# get elements

	# fill in passwd
	webbrowser.find_element_by_css_selector("span#YT-form-tips.r-mPassword-tips").send_keys(password)
	webbrowser.find_element_by_css_selector("span#YT-form-tips.r-mRepeatPwd-tips").send_keys(password)

	# sliding 
	while webbrowser.find_element_by_css_selector("#wyBox > input").get_attribute("value") == "":
		bgURL = webbrowser.find_element_by_css_selector("img.yidun_bg-img").get_attribute("src")
		save_bg(bgURL)

		offset = getDefaultPosition()
		print "[LOG]-----> extract offset successfully " + str(offset)

		yidun_slider = webbrowser.find_element_by_css_selector("div.yidun_slider")
		action = Actions(webbrowser)
		action.click_and_hold(yidun_slider)
		action.wait(1)
		# time.sleep(1)

		move = offset[0] * 0.56 + 17

		print "try"
		ActionChains(webbrowser).click_and_hold(yidun_slider).perform()
		track_list = getTrack(move)     
		track_string = ""
		#这边滑块的高度为：42，宽度为：40
		for track in track_list:
		    track_string = track_string + "{%d,%d}," % (track, 19)
		    # ActionChains(webbrowser).move_to_element_with_offset(to_element=yidun_slider, xoffset=track+5 ,yoffset=19).perform()
		    ActionChains(webbrowser).move_by_offset(track, 1).perform()
		    time.sleep(random.randint(10, 50) / 100)
		print track_string
		time.sleep(1)
		ActionChains(webbrowser).release(yidun_slider).perform()
		time.sleep(1)

	print ("[LOG]-----> slider crack successfully")

	# get and fill in mobile
	mobile = getAntMobile()
	if mobile != "" and len(mobile) == 11:
		print "[LOG]-----> get mobile number successfully: " + str(mobile)
		webbrowser.find_element_by_css_selector("input#mobile.nwd-input-inner.nwd-input-placeholder").send_keys(mobile)
	else:
		print "[ERR]****** error when fetching mobile, error number: " + str(mobile)
		return

	# get and fill in verify
	webbrowser.find_element_by_css_selector("#gainMessage").click()
	time.sleep(1)
	s = webbrowser.find_element_by_css_selector("#mobileMsg").get_attribute("innerHTML")
	print s
	if len(s.strip()) == 0:
		print "[LOG]-----> mobile is qualified: " + str(mobile)
		verify = getVerify(mobile)
		if verify != "FAIL":
			print "[LOG]-----> receive verify: " + str(verify)
			webbrowser.find_element_by_css_selector("input#phoneCode.nwd-input-inner.nwd-input-placeholder").send_keys(verify)
			# black(mobile)
		else:
			print "[ERR]****** error, mobile was used: " + str(mobile)
			black(mobile)
			releaseMobile(mobile)
			return
	else:
		print "[ERR]****** error, mobile was used: " + str(mobile)
		black(mobile)
		releaseMobile(mobile)
		return

	# click to registered
	webbrowser.find_element_by_css_selector("#regSubmit").click()
	checkStr = webbrowser.find_element_by_css_selector("span.nwd-validate-content").get_attribute("text")
	if checkStr == "验证码输入有误，请重新输入":
		print "[ERR]****** error, wrong verify: " + str(mobile)

	# check & save account
	time.sleep(1)
	redirect = webbrowser.current_url.split('/')[-1]
	if redirect == 'loading.html':
		saveAccount(mobile, password)
		black(mobile)
		releaseMobile(mobile)
		print ("[LOG]-----> You are good Robber")
	else:
		print "[ERR]****** error, registed failed"
		black(mobile)
		releaseMobile(mobile)
	return
# webbrowser.close()

# js='window.open("' + robberURL + '")'
# webbrowser.execute_script(js)

for i in range(20):
	process(webbrowser)































































