# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACd836e2ff2ce9242645209cc2fa589909'
auth_token = 'e2e34c542a9c3c761f18563c597e8d67'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+19569487628',
                     to='+919980708840'
                 )

print(message.sid)
