import smtplib
from email.message import EmailMessage
def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('charaneede9999@gmail.com','sxhv ezty vuoh xvrn')
    msg=EmailMessage()
    msg['From']='enter your email'
    msg['To']=to
    msg['Subject']=subject
    msg.set_content(body)
    server.send_message(msg)
    server.quit()