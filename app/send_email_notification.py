################################################################################################
# purpose: the purpose of this code is to send process status
# send_email_notification.py
# note: n/a
# author: dheeraj rekula (rekula.d@gmail.com)
################################################################################################



import os
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import *

def send_email(text):
    
    load_dotenv()
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
    MY_EMAIL_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    ### load email variables
    from_email = Email(MY_EMAIL_ADDRESS)
    to_email = Email(MY_EMAIL_ADDRESS)
    subject = "Example Notification"
    sub_text = text
    message_text = f"Dear User, \nThis is an automated email response. \n {sub_text}"
    content = Content("text/plain", message_text)
    mail = Mail(from_email, subject, to_email, content)
    ### issue request
    response = sg.client.mail.send.post(request_body=mail.get())
    return response
    #print("Status:", response.status_code)


    ### TODO: delete this at the end
    #print("----------------------")
    #print("----------------------")
    #print("RESPONSE: ", type(response))
    #print("STATUS:", response.status_code) #> 202 means success
    #print("HEADERS:")
    #pp.pprint(dict(response.headers))
    #print("BODY:")
    #print(response.body) #> this might be empty. it's ok.)