import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

FROM = "kevin694026728@gmail.com"
TO = "gukailia@msu.edu"
Password = "fjydklnsatjiwfcr"


message = MIMEMultipart()
message["Subject"] = "Testing Email"
message["From"] = FROM
message["To"] = TO

text_body = "This is not a test!"

message.attach(MIMEText(text_body))
context = ssl.create_default_context()
server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
server.login(FROM, Password)
server.sendmail(FROM, TO, message.as_string())
server.quit()