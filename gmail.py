import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


def main():
	sendMail('重要通知','''\
<html>
  <head></head>
  <body>
    <p>Salut! 
    <p>Cela ressemble à un excellent
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            recipie
        </a>  
    </p>    
  </body>
</html>
''')

	
def sendMail(title,content):
	gmail_user = 's1059005@gmail.com'
	str_time = time.strftime("%H:%M:%S")
	title = title + " " + str_time
	# 讀取gmail應用程式密碼
	with open('gmail.txt','rt') as fi:
		gmail_password = fi.readline()

	msg = MIMEMultipart('alternative')

	msg['Subject'] = title
	msg['From'] = gmail_user
	msg['To'] = 'smallken@gmail.com'
	# 附加 html內文
	html_part = MIMEText(content,'html')
	msg.attach(html_part)

	# 附加圖片
	# with open(file, 'rb') as fp:
	# 	img = MIMEImage(fp.read())
	# msg.attach(img)		

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(gmail_user, gmail_password)
	server.send_message(msg)
	server.quit()

	print('Email sent!:\n')
	print('title:{}\n{}'.format(title,content))



if __name__ == '__main__':
	main()




