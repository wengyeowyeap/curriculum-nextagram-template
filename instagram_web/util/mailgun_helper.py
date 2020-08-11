from app import app
import requests

def send_donation_message():  
  return requests.post(
    f"https://api.mailgun.net/v3/{app.config.get('MAILGUN_DOMAIN')}/messages",
    auth=("api", app.config.get('MAILGUN_API')),
    data={"from": f"Nextagram <mailgun@{app.config.get('MAILGUN_DOMAIN')}>",
          "to": ["wengyeowyeap@gmail.com"],
          "subject": "You have received a donation!",
          "text": "Test"})
