import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

def mail_sent(mail, code):
  
    load_dotenv(dotenv_path="c:/Users/Sebastian/flaskapp/.env") # load variables from .env file   
    # configuration settings
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    sender = os.getenv("EMAIL_LOGIN")
    sender_pass = os.getenv("EMAIL_PASSWORD")
    receiver = mail 
    
    if not sender or not sender_pass:
        raise ValueError("EMAIL_LOGIN or EMAIL_PASSWORD is empty in .env file")

    # html template
    html_template = f"""
    <html lang="en" style="font-size: 87.5%; box-sizing: border-box;">
    <body style="display: flex; flex-direction: column;">
        <main style="box-shadow: 0px 2px 2px 2px;">
            <header style="display: flex; flex-direction: column; align-items: center; background-color: #3b3a3a; color: #f0f3f4">
                <h2 style="margin-bottom: 0;">THANKS FOR SIGNING UP:</h2>
                <h1>Verify Your E-Mail Address</h1>
                <p style="margin-bottom: 20px;">Use this code to verificate your e-mail address.</p>
            </header>
            <h2 style="display: flex; flex-direction: column; align-items: center;">Your verification code</h2>
            <section style=" display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 20px 0px 20px 0px;">
                <p style=" display: flex; flex-direction: column; align-items: center; justify-content: center; width: 500px; height: 100px; background-color: #e8e8e8; border-radius: 25px; font-size: 50px">{code}</p>
            </section>
            <footer style="display: flex; flex-direction: column; align-items: center;">
                <p style="margin-bottom: 0;">If this isn't you, ignore the message</p>
                <p style="margin-bottom: 20px;">Don't reply to this mail, this is an automatically generated message</p>
            </footer>
        </main>
    </body>
    </html>
    """ 
    # make a message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verification code"
    msg['From'] = "TaskMgm"
    msg['To'] = receiver    
    # adding html
    html_part = MIMEText(html_template, 'html')
    msg.attach(html_part)   
    # sending mail
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(sender, sender_pass)
        server.sendmail(sender, receiver, msg.as_string())  
    return True