import gmail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import xlsxwriter
import decimal



def check():	
	# Browser = webdriver.Chrome()
	Browser = webdriver.PhantomJS(executable_path=r'phantomjs-2.1.1-windows\bin\phantomjs.exe')
	o = open("個人賣場.txt","rt")
	LoginUrl= 'https://cadm.pcstore.com.tw/ords/ship.htm'
	with open("pwd.txt",'rt') as ff:
		UserPass= ff.readline()
	UserName = o.readlines()

	content = "" #email內文
	Browser.get(LoginUrl)

	for username in UserName:
		sleep(2)
		content = content + "帳號: " + username + "\n\n"
		username = username.strip()
		Browser.find_element_by_xpath('//*[@id="inpuid"]').clear()
		Browser.find_element_by_xpath('//*[@id="inpuid"]').send_keys(username)
		Browser.find_element_by_xpath('//*[@id="userpass"]').send_keys(UserPass)
		Browser.find_element_by_xpath('//*[@id="userpass"]').send_keys(Keys.ENTER)
		sleep(2)
		Browser.get("https://cadm.pcstore.com.tw/ords/ship.htm") # 出貨管理
		sleep(2)
		try:
			tbody = Browser.find_element_by_xpath('//*[@id="d_IN"]/table').get_attribute('outerHTML')
		except BaseException:
			tbody = "沒有訂單"
		
		# print(tbody)
		content = content + tbody + "\n\n"

		Browser.get("https://paystore.pcstore.com.tw/adm/logout.htm") # 登出
		Browser.get(LoginUrl)

	gmail.sendMail("訂單通知", content)


if __name__ == '__main__':
	check()