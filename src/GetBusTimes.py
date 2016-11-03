import json
import collections
import random
from urllib import urlencode
from urllib2 import urlopen
from hashlib import md5
from datetime import datetime


class Buses:
    API_BASE = "http://ws.mybustracker.co.uk"
    API_KEY = "PUT YOUR KEY HERE"
    API_KEY_MD5 = md5(API_KEY + datetime.now().strftime("%Y%m%d%H")).hexdigest()

    url_data = {}
    url_data["module"] = "json"
    url_data["key"] = API_KEY_MD5
    url_data["function"] = "getBusTimes"
    url_data["nb"] = 3
    url_data["stopId1"] = ADDYOURSTOPIDHERE

    def get_bus_times(self, intent):
        url_values = urlencode(self.url_data)

        response = json.load(urlopen(self.API_BASE + "?" + url_values))
        buses = {}
        for service in response["busTimes"]:
            buses[service["mnemoService"]] = []
            for bus_time in service["timeDatas"]:
                buses[service["mnemoService"]].append(bus_time["minutes"])
        buses = collections.OrderedDict(sorted(buses.items()))

        bus_times_string = "OK. "
        for bus_number, bus_set in buses.iteritems():
            if bus_set[0] < 1:
                bus_set.pop(0)
            if len(bus_set) > 1:
                final_bus = buses[bus_number].pop(len(buses[bus_number]) - 1)
                bus_minutes_string = ", and ".join((", ".join(str(y) for y in buses[bus_number]),str(final_bus)))
            else:
                bus_minutes_string = ", ".join(str(y) for y in buses[bus_number])
            bus_times_string += "The {0} is leaving in {1} minutes. ".format(bus_number, bus_minutes_string)

        return bus_times_string

bus_times = Buses()

end_session_global = False

def lambda_handler(event, context):
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])


def on_session_started(session_started_request, session):
    print "Starting new session."


def on_launch(launch_request, session):
    return get_welcome_response()


def get_welcome_response():
    return notify("Ask me when the next bus is")


def on_session_ended(session_ended_request, session):
    print "Ending session."
    return notify("Goodbye")


def notify(message, title = "BusTracker", end_session = None, reprompt_text = None):
    global end_session_global
    if end_session == None:
        end_session = end_session_global
    return {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": message
            },
            "card": {
                "type": "Simple",
                "title": title,
                "content": message
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": reprompt_text
                }
            },
            "shouldEndSession": end_session
        }
    }


def on_intent(intent_request, session):
    global end_session_global
    if session["new"] == True:
        end_session_global = True
    else:
        end_session_global = False

    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetBusTimes":
        return notify(bus_times.get_bus_times(intent), "Bus Times")
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return notify("Goodbye then", "Goodbye", True)
    else:
        raise ValueError("Invalid intent")
