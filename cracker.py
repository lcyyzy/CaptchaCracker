#!/usr/local/bin/python
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
robberURL = 'http://www.niwodai.com/multiRegister.html?artId=5820160000010275' # you me die

# selenim settings
chromedriver = '/Users/LCY/Downloads/chromedriver'

# rigistor robber
# account & passwd settings
password = '1qaz2wsx'

#######################################################################
# registor process
# intial webbrowser
def switch_language(language_no):
	if (language_no == 0):
		return 'de-AT'
	elif (language_no == 1):
		return "en-US"
	elif (language_no == 2):
		return "en-AU"
	elif (language_no == 3):
		return "nl-BE"
	elif (language_no == 4):
		return "en-CA"
	elif (language_no == 5):
		return "zh-HK"
	elif (language_no == 6):
		return "zh-SG"
	elif (language_no == 7):
		return "zh-TW"
	elif (language_no == 8):
		return "nl-BE"
	elif (language_no == 9):
		return "en-BZ"
	elif (language_no == 10):
		return "en-CA"
	elif (language_no == 11):
		return "en-IE"
	elif (language_no == 12):
		return "en-JM"
	elif (language_no == 13):
		return "en-NZ"
	elif (language_no == 14):
		return "en-ZA"
	elif (language_no == 15):
		return "en-TT"
	elif (language_no == 16):
		return "en-GB"
	elif (language_no == 17):
		return "fr-BE"
	elif (language_no == 18):
		return "fr-CA"
	elif (language_no == 19):
		return "fr-LU"
	elif (language_no == 20):
		return "fr-CH"
	elif (language_no == 21):
		return "de-DE"
	elif (language_no == 22):
		return "de-CH"
	elif (language_no == 23):
		return "ru-RU"
	elif (language_no == 24):
		return "el-GR"
	elif (language_no == 25):
		return "es-LA"
	elif (language_no == 26):
		return "es-MX"
	elif (language_no == 27):
		return "es-PR"
	elif (language_no == 28):
		return "es-ES"
	elif (language_no == 29):
		return "es-US"
	elif (language_no == 30):
		return "it-IT"
	elif (language_no == 31):
		return "no-NO"
	elif (language_no == 32):
		return "hu-HU"
	elif (language_no == 33):
		return "tr-TR"
	elif (language_no == 34):
		return "cs-CZ"
	elif (language_no == 35):
		return "sv-SE"

os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"intl.accept_languages": switch_language(random.randint(0, 35))})
webbrowser = webdriver.Chrome(chromedriver, chrome_options = options)
webbrowser.implicitly_wait(5)
webbrowser.set_window_size(800,800)
webbrowser.delete_all_cookies()


def process(webbrowser):
	# get web
	webbrowser.get(robberURL)

	# wait for loading
	time.sleep(2)

	# get elements

	# fill in passwd

	# sliding 
	try:
		# webbrowser.find_element_by_css_selector("input#pwd.nwd-input-inner.nwd-input-placeholder").send_keys(password)

		for i in range(5):
			bgURL = webbrowser.find_element_by_css_selector("img.yidun_bg-img").get_attribute("src")
			if len(bgURL) == 0:
				return
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
			    time.sleep(random.randint(10, 50) / 10000)
			print track_string
			time.sleep(0.5)
			ActionChains(webbrowser).release(yidun_slider).perform()
			time.sleep(1)
			print webbrowser.find_element_by_css_selector("#wyBox > div > div:nth-child(2) > div.yidun_tips > span.yidun_tips__text").get_attribute("innerText")
			if webbrowser.find_element_by_css_selector("#wyBox > div > div:nth-child(2) > div.yidun_tips > span.yidun_tips__text").get_attribute("innerText") == "" :
				print ("[LOG]-----> slider crack successfully")
				break

	except Exception, e:
		print "[ERR]****** error when sliding slider"
		return

	else:
		print webbrowser.find_element_by_css_selector("#wyBox > div > div:nth-child(2) > div.yidun_tips > span.yidun_tips__text").get_attribute("innerText")
		if webbrowser.find_element_by_css_selector("#wyBox > div > div:nth-child(2) > div.yidun_tips > span.yidun_tips__text").get_attribute("innerText") != "":
			print ("[LOG]-----> slider crack failed")
			return				

		get and fill in mobile
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

		# 请刷新页面
		# print webbrowser.find_element_by_css_selector("#gainMessage").get_attribute("value")
		# if webbrowser.find_element_by_css_selector("#gainMessage").get_attribute("value") == "获取验证码":
		# 	releaseMobile(mobile)
		# 	print ("[LOG]-----> slider crack failed: please refresh")
		# 	return	
		flag = 0
		try:
			webbrowser.find_element_by_css_selector("#imgCodeMSG > div > span")
		except:
			flag = 1
		else:
			flag = 0

		if flag == 0:
			releaseMobile(mobile)
			print ("[LOG]-----> slider crack failed: please refresh")
			return	

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
		flag_sms = 0
		try:
			checkStr = webbrowser.find_element_by_css_selector("span.nwd-validate-content").get_attribute("text")
			if checkStr == "验证码输入有误，请重新输入":
				flag_sms = 1
				print "[ERR]****** error, wrong verify: " + str(mobile)
				return
		except:
			if flag_sms == 0:
				saveAccount(mobile, password)
				black(mobile)
				releaseMobile(mobile)
				print ("[LOG]-----> You are good Robber")
			return
		saveAccount(mobile, password)
		black(mobile)
		releaseMobile(mobile)
		print ("[LOG]-----> You are good Robber")
		
		# check & save account
		time.sleep(1)
		redirect = webbrowser.current_url.split('/')[-1]
		if redirect == 'loading.html':
			print ("[LOG]-----> Redirect")
		else:
			print "[ERR]****** error, not redirect"
			black(mobile)
			releaseMobile(mobile)
		return 
# webbrowser.close()

# js='window.open("' + robberURL + '")'
# webbrowser.execute_script(js)

for i in range(500):
	try:
		process(webbrowser)
	except Exception, e:
		print "[ERR]****** ERROR"
		print repr(e)
		print str(e)
		webbrowser.quit()
		break

