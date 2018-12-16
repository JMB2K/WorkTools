import smtplib, os
from email.message import EmailMessage


s=smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
s.starttls()
s.login('reprocon@corgan.com', 'Repro@Corgan401')

msg=EmailMessage()
msg['From'] = 'reprocon@corgan.com'
msg['To'] = 'jonathanmb2000@gmail.com'
msg['Subject'] = 'Reports'
msg.preamble = 'This is a test'

location = 'C:\\Users\\00015\\Documents\\Reports\\February 2018'
directory = os.listdir(location)
for file in directory:
    msg.add_attachment(os.path.join(location, file))

s.send_message(msg)
