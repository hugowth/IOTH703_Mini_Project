import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from picamera import PiCamera
from PIL import Image

#define smtp servcer
SMTP_SERVER = "smtp.gmail.com" #gmail smtp server
SMTP_PORT = 587 #Server Port
USERNAME = "ioth703project@gmail.com" #username

f = open("secret", "r")
PASSWORD = f.read()
f.close()

class Email:
    def send(self, recipient, subject, content, image):
        #email headers
        emailData = MIMEMultipart()
        emailData['Subject'] = subject
        emailData['To'] = recipient
        emailData['From'] = USERNAME

        #email content
        emailData.attach(MIMEText(content))

        #attach image data
        imageData = MIMEImage(open(image, 'rb').read(), 'jpg')
        imageData.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
        emailData.attach(imageData)

        #connect to gmail server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(USERNAME, PASSWORD)

        #send email
        session.sendmail(USERNAME, recipient, emailData.as_string())
        session.quit


        