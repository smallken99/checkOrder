import gmail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import xlsxwriter
import decimal
import os
import json



def check():	
	Browser = webdriver.Chrome()
	# Browser = webdriver.PhantomJS(executable_path=r'phantomjs-2.1.1-windows\bin\phantomjs.exe')
	o = open("個人賣場.txt","rt")
	LoginUrl= 'https://cadm.pcstore.com.tw/ords/ship.htm'
	with open("pwd.txt",'rt') as ff:
		UserPass= ff.readline()
	UserName = o.readlines()
	content = "" #email內文
	Browser.get(LoginUrl)
	isSend = False

	for username in UserName:
		sleep(2)
		username = username.strip()
		fileName = 'pc_' + username + '_cookie.txt'
		if os.path.isfile(fileName):
			print(fileName,'cookie檔案存在')
			fi = open(fileName, 'rt')
			cookies = json.load(fi)
			for cookie in cookies:
				Browser.add_cookie(cookie)
			Browser.get("https://cadm.pcstore.com.tw/ords/ship.htm") # 出貨管理
			sleep(10)
			content = content + "<h1>帳號: " + username + "</h1>\n\n"
			try:
				tbody = Browser.find_element_by_xpath('//*[@id="d_IN"]/table').get_attribute('outerHTML')
				isSend = True
			except BaseException:
				tbody = "沒有訂單"
			content = content + tbody + "\n\n"
			Browser.get("https://paystore.pcstore.com.tw/adm/logout.htm") # 登出
			sleep(1)
			Browser.get(LoginUrl)
		else:			
			Browser.find_element_by_xpath('//*[@id="inpuid"]').clear()
			Browser.find_element_by_xpath('//*[@id="inpuid"]').send_keys(username)
			Browser.find_element_by_xpath('//*[@id="userpass"]').send_keys(UserPass)
			Browser.find_element_by_xpath('//*[@id="userpass"]').send_keys(Keys.ENTER)
			sleep(5)
			Browser.get("https://cadm.pcstore.com.tw/ords/ship.htm") # 出貨管理
			sleep(10)
			content = content + "<h1>帳號: " + username + "</h1>\n\n"
			try:
				tbody = Browser.find_element_by_xpath('//*[@id="d_IN"]/table').get_attribute('outerHTML')
			except BaseException:
				tbody = "沒有訂單"
			content = content + tbody + "\n\n"
			# 儲存cookies
			cookies = Browser.get_cookies()
			f1 = open(fileName, 'w')
			f1.write(json.dumps(cookies))
			f1.close
			Browser.get("https://paystore.pcstore.com.tw/adm/logout.htm") # 登出
			sleep(2)
			Browser.get(LoginUrl)
			
	if(isSend):
		gmail.sendMail("訂單通知", content,[])


if __name__ == '__main__':
	check()