import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

	# 讀取gmail應用程式密碼
	with open('gmail.txt','rt') as fi:
		gmail_password = fi.readline()

	msg = MIMEMultipart('alternative')
	html_part = MIMEText(content,'html')
	msg['Subject'] = title
	msg['From'] = gmail_user
	msg['To'] = 'smallken@gmail.com'
	msg.attach(html_part)
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(gmail_user, gmail_password)
	server.send_message(msg)
	server.quit()

	print('Email sent!:\n')
	print('title:{}\n{}'.format(title,content))



if __name__ == '__main__':
	main()




