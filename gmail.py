import smtplib
from email.mime.text import MIMEText


def main():
	sendMail('重要通知','你好,有一件重要的事請你處理')

	
def sendMail(title,content):
	gmail_user = 's1059005@gmail.com'

	# 讀取gmail應用程式密碼
	with open('gmail.txt','rt') as fi:
		gmail_password = fi.readline()

	msg = MIMEText(content)
	msg['Subject'] = title
	msg['From'] = gmail_user
	msg['To'] = 'smallken@gmail.com'

	# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	# server.ehlo()
	# server.login(gmail_user, gmail_password)
	# server.send_message(msg)
	# server.quit()

	print('Email sent!:\n')
	print('title:{}\n{}'.format(title,content))



if __name__ == '__main__':
	main()




