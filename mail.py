import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 
import html
import auth

def sendWelcome(recvAddress, passwd):
    try: 
        
        message = MIMEMultipart('alternative')
        message['From'] = auth.authEmail
        message['To'] = recvAddress
        message['Subject'] = 'Hotel Paradise - Sign Up' 

        message.attach(MIMEText(html.welcomeHtml(recvAddress, passwd), "html"))

        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls() 
        session.login(auth.authEmail, auth.authEmailPasswd) 
        text = message.as_string()
        session.sendmail(auth.authEmail, recvAddress, text)
        session.quit()
    except:
        pass
def sendOtp(otp, recvAddress):
    try:
        message = MIMEMultipart('alternative')
        message['From'] = auth.authEmail
        message['To'] = recvAddress
        message['Subject'] = 'Hotel Paradise - Sign Up'
        
        html = '''<html>
            <body>
                <p style="font-family:helvetica,arial;">
                    To continue, first verify it's you! 
                    Your otp: '''+str(otp)+'''
                </p>
            </body>
        </html>'''
       
        message.attach(MIMEText(html, "html"))

        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls()
        session.login(auth.authEmail, auth.authEmailPasswd) 
        text = message.as_string()
        session.sendmail(auth.authEmail, recvAddress, text)
        session.quit()

        del message,html,session,text
        return True
    except:
        return False
