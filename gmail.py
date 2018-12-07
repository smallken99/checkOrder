import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time


def main():
	sendMail('訂單通知','''\
<html>
  <head></head>
  <body>
    <p>Salut! 
    <p>Cela ressemble  excellent
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            recipie
        </a>  
    </p>    
  </body>
</html>	
''',['0921584584.png','0963255465.png'])

	
def sendMail(title,content,files):

	str_time = time.strftime("%H:%M:%S")
	title = title + " " + str_time
	content = '<html>' + content + '</html>'
	msg = MIMEMultipart('alternative')

	msg['Subject'] = title
	msg['From'] = 'smallken@smallken.com'
	msg['To'] = 'oioi7211@gmail.com, smallken@gmail.com'
	# 附加 html內文
	html_part = MIMEText(content,'html')
	msg.attach(html_part)

	# 附加圖片
	for file in files:
		with open(file, 'rb') as fp:
			img = MIMEImage(fp.read())
		msg.attach(img)		

	server = smtplib.SMTP('smallken.com')
	server.send_message(msg)

	print('Email sent!:\n')
	print('title:{}\n{}'.format(title,content))



if __name__ == '__main__':
	main()




