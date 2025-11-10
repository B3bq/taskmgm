import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def mail_sent(mail, code):
    api_key = os.getenv("SENDGRID_API_KEY")
    sender = os.getenv("EMAIL_SENDER")

    if not api_key:
        raise ValueError("SENDGRID_API_KEY is missing in environment variables")

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

    # making message
    message = Mail(
        from_email=sender,
        to_emails=mail,
        subject="Verification code",
        html_content=html_template
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("Email sent:", response.status_code)
        return True
    except Exception as e:
        print("SendGrid error:", e)
        return False
