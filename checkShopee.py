import gmail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import xlsxwriter
import decimal
import json
import os

 
def check():	

	# Browser = webdriver.PhantomJS(executable_path=r'phantomjs-2.1.1-windows\bin\phantomjs.exe')
	with open("pwd.txt",'rt') as ff:
		UserPass= ff.readline()
	with open("蝦皮.txt","rt") as o:
		UserName = o.readlines()
	isSend = False;
	content = "" #email內文	
	fileList = []
	for username in UserName:
		Browser = webdriver.Chrome()
		Browser.get('https://seller.shopee.tw/portal/sale?type=toship')
		sleep(2)
		username = username.strip()
		fileName = username + '_cookie.txt'
		if os.path.isfile(fileName):
			print(fileName,'cookie檔案存在')
			fi = open(fileName, 'rt')
			cookies = json.load(fi)
			for cookie in cookies:
				Browser.add_cookie(cookie)
			# Browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[4]/div/div/div/div[2]/div[1]/div/input').send_keys(username)
			# Browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[4]/div/div/div/div[2]/div[2]/div/input').send_keys(UserPass)
			# Browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[4]/div/div/div/div[2]/div[2]/div/input').send_keys(Keys.ENTER)
			# 我的銷售
			sleep(10)
			Browser.get('https://seller.shopee.tw/portal/sale?type=toship')
			sleep(10)
			try:
				div = Browser.find_element_by_xpath("//div[contains(@class, 'order-items toship')]").get_attribute('outerHTML')
				# Browser.maximize_window()
			except BaseException:
				Browser.get('https://seller.shopee.tw/portal/sale?type=toship')
				sleep(20)
				try:
					div = Browser.find_element_by_xpath("//div[contains(@class, 'order-items toship')]").get_attribute('outerHTML')
				except BaseException:
					Browser.get('https://seller.shopee.tw/portal/sale?type=toship')
					sleep(40)
					try:
						div = Browser.find_element_by_xpath("//div[contains(@class, 'order-items toship')]").get_attribute('outerHTML')
					except BaseException:
						div = "沒有訂單"
			try:# 有找到 [產生寄件編號] 要寄mail通知
				Browser.find_element_by_xpath("//div[contains(@class, 'shopee-button shopee-button--inactive shopee-button--primary ember-view')]").get_attribute('innerHTML')						
				isSend = True
			except BaseException:
				pass
			Browser.save_screenshot(username + ".png")
			fileList.append(username + ".png")
			print(div)
			sleep(10)
			content = content + "<h1>帳號: " + username + "</h1>\n\n"
			content = content +  div + '\n\n'

		else:
			print(fileName,'cookie檔案不存在')
			Browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[4]/div/div/div/div[2]/div[1]/div/input').send_keys(username)
			Browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[4]/div/div/div/div[2]/div[2]/div/input').send_keys(UserPass)
			Browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[4]/div/div/div/div[2]/div[2]/div/input').send_keys(Keys.ENTER)			
			sleep(30)
			cookies = Browser.get_cookies()
			# 儲存cookies
			f1 = open(fileName, 'w')
			f1.write(json.dumps(cookies))
			f1.close
		Browser.quit()
		# try:
		# 	tbody = Browser.find_element_by_xpath('//*[@id="d_IN"]/table').get_attribute('outerHTML')
		# except BaseException:
		# 	tbody = "沒有訂單"
		
		# print(tbody)
		# content = content + tbody + "\n\n"

		# Browser.get("https://paystore.pcstore.com.tw/adm/logout.htm") # 登出
		# Browser.get(LoginUrl)
	if(isSend):
		gmail.sendMail("shopee訂單通知", content, fileList)
	

 

if __name__ == '__main__':
	check()