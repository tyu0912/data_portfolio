from twilio.rest import TwilioRestClient
import os

accountSID = os.getenv("twilioAccount")
authToken = os.getenv("twilioAuth")

twilioCli = TwilioRestClient(accountSID, authToken)

myTwilioNumber =os.getenv("twilioNumber")
myCellPhone = os.getenv("number")

message = twilioCli.messages.create(body='This is a Python test',from_=myTwilioNumber, to=myCellPhone)
