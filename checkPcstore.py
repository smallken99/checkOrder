import gmail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import decimal
import os
import json
import time
from bs4 import BeautifulSoup

def setTimeisSend():
	# 早上7點至8點一律通知
	int_time = int(time.strftime("%H%M"))
	if int_time > 700 and int_time < 800:
		return  True
	else:
		return False

def check():	
	# Browser = webdriver.Chrome()
	Browser = webdriver.PhantomJS(executable_path=r'phantomjs-2.1.1-windows\bin\phantomjs.exe')
	o = open("pchome.txt","rt")
	LoginUrl= 'https://cadm.pcstore.com.tw/ords/ship.htm'
	with open("pwd.txt",'rt') as ff:
		UserPass= ff.readline()
	UserName = o.readlines()
	content = "" #email內文
	Browser.get(LoginUrl)

	# 早上7點至8點一律通知
	isSend = setTimeisSend()


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
			except BaseException:
				tbody = "沒有訂單"
			# 以 Beautiful Soup 解析 HTML 程式碼,判斷要不要寄信
			soup = BeautifulSoup(tbody, 'html.parser')
			tr_tag = soup.select("tr")
			for tr in tr_tag:
				text = BeautifulSoup(str(tr), 'html.parser').select_one("td:nth-of-type(8)")
				if text != None:
					if str(text.string).strip() == '':
						isSend = True
	

			content = content + tbody + "\n\n"
			Browser.get("https://paystore.pcstore.com.tw/adm/logout.htm") # 登出
			sleep(2)
			Browser.get(LoginUrl)
		else:			
			Browser.find_element_by_xpath('//*[@id="inpuid"]').clear()
			Browser.find_element_by_xpath('//*[@id="inpuid"]').send_keys(username)
			Browser.find_element_by_xpath('//*[@id="userpass"]').send_keys(UserPass)
			Browser.find_element_by_xpath('//*[@id="userpass"]').send_keys(Keys.ENTER)
			sleep(5)
			Browser.get("https://cadm.pcstore.com.tw/ords/ship.htm") # 出貨管理
			sleep(20)
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
	Browser.quit()
	if isSend:
		gmail.sendMail("pc訂單通知", content,[])


if __name__ == '__main__':
	check()
