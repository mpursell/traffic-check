import requests
import os
from dotenv import load_dotenv, find_dotenv
from datetime import date, timedelta
from twilio.rest import Client


class TwilioTextMessage:
    def __init__(self, messageText):
        load_dotenv(find_dotenv())
        self.accountSID = os.environ.get("TWILIO_ACCOUNT_SID")
        self.authToken = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilioPhoneNumber = os.environ.get("TWILIO_PHONE_NUMBER")
        self.myPhoneNumber = os.environ.get("MY_PHONE_NUMBER")
        self.messageText = messageText

    def send_message(self):
        self.twilioClient = Client(self.accountSID, self.authToken)

        self.message = self.twilioClient.messages.create(
            to=self.myPhoneNumber, from_=self.twilioPhoneNumber, body=self.messageText
        )


class ApiHandler:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.url = "https://maps.googleapis.com/maps/api/directions/json?"
        self.apiKey = os.environ.get("API_KEY")

    def response(self, origin, destination) -> object:
        self.origin = origin
        self.destination = destination
        params = {
            "origin": self.origin,
            "destination": self.destination,
            "departure_time": "now",
            "alternatives": "true",
            "key": self.apiKey,
        }
        apiCall = requests.get(self.url, params=params)
        return apiCall


def GetTrafficSummaryAndDuration(origin, destination) -> str:

    api = ApiHandler()
    trafficResponse = api.response(origin, destination)

    # return non zero code if Google API doesn't respond properly,
    # we don't want to send text messages if the api response is useless
    if not trafficResponse.status_code == 200:
        return 1

    else:

        traffic_json = trafficResponse.json()
        resultList = []
        routes = traffic_json["routes"]

        for route in routes:
            summary = route["summary"]
            duration = route["legs"][0]["duration_in_traffic"]["text"]
            resultList.append(summary + " " + duration)

        # join the list with newlines so we can just return a string
        # for the text message.
        resultString = " \n".join(str(elem) for elem in resultList)
        return resultString


def SendTrafficSummaryAndDuration(origin, destination):

    trafficString = GetTrafficSummaryAndDuration(origin, destination)

    if trafficString == 1:
        exit()
    else:
        textMessage = TwilioTextMessage(trafficString)
        textMessage.send_message()


SendTrafficSummaryAndDuration(
    "Underwood,+Nottingham", "Alfreton+Park+Special+School,+Alfreton"
)
