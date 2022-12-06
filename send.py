import imghdr
from email.message import EmailMessage
import smtplib
import ssl


password='xwwxetivpwxxnfsm'
username='bloodshreder1@gmail.com'
receiver='bloodshreder1@gmail.com'
def send_mail(new):
    file=new
    # print(file)
    message=EmailMessage()
    message['Subject']='Found someone'
    message.set_content('New person showed up on house')



    with open(file,'rb') as file1:
        content1=file1.read()
    message.add_attachment(content1,maintype='image',subtype=imghdr.what(None,content1))
    context=ssl.create_default_context()
    gmail=smtplib.SMTP_SSL('smtp.gmail.com',465,context=context)
    gmail.ehlo()
    # gmail.starttls()
    gmail.login(username,password)
    gmail.sendmail(username,receiver,message.as_string())
    gmail.quit()

