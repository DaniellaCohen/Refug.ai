from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
from sets import Set
from wit import Wit
import json
account = "AC0479211f7176e6506df9d2bae2998591"
token = "1ea25df1dab9c5eb25cf3a3eec64e659"
client = TwilioRestClient(account, token)
app = Flask(__name__)

yesList = ("yes", "yea", "yeah", "ya", "yass", "y")
noList = ("no", "nope", "nah", "na", "n")

#Nodes for every situation
beginning = { # in the city, introduction
        "text" : "Should I try running?",
        
        "triggerPathSet" : {
            yesList : "escape",
            noList : "donthelp"
        }   
    }

escape = {
        "text" : "She escapes. Congrats. Play again?",
        
        "triggerPathSet" : {
            yesList : "beginning",
            noList : "donthelp"
        }
    }
    
donthelp = {
        "text" : "She dies.",
        
        "triggerPathSet" : {
            yesList : "nah",
            noList : "nah"
        }
    }

getNode = {
    "beginning" : beginning,
    "escape" : escape,
    "donthelp" : donthelp,
}

#List of users

users = {
 "+17863006532" : {
    "node" : beginning,
    "inventory" : ["wedding ring", "knife"]
 }
}



def send(request, response):
    print("sending..", response["text"])
def usrAction(request):
    print("receiving message..", request["text"])
actions = {
    "send": send,
    "usr_action": usrAction,
}
clientWit = Wit(access_token="IZSMSLY4OI44FG5MC5NNH5TCGKPLQ4NV",actions=actions)
#respWit = clientWit.message("hey")
#print("Yay, got Wit.ai response: " + str(respWit))


def makeChoice(user, response):
    for key in user["node"]["triggerPathSet"]:
        if response in key:
            print "s"
            user["node"] = getNode[user["node"]["triggerPathSet"].get(key)]
            

def send(content):
    message = client.messages.create(to="+17863006532", from_="+17479980222",body=content)
                                 #resp = twilio.twiml.Response()
    resp.message(message)

    
def displaySituation(user):
    return user["node"]['text']


#Initial message
user = users["+17863006532"]
content = displaySituation(user)
message = client.messages.create(to="+17863006532", from_="+17479980222",
                                     body=content)
    

@app.route("/", methods=['GET', 'POST'])
def sms():
    sender = request.values.get('From', None)
    user = users[sender]
    bodyContent = request.values.get('Body', None).lower()
    respWit = clientWit.converse("20170218", "hey", {})
    print("Yay, got Wit.ai response: " + str(respWit))
    parsedMsg = json.loads(str(respWit))
    print parsedMsg["msg"]
    print bodyContent
    
    #
    makeChoice(user, bodyContent)
    message = client.messages.create(to=sender, from_="+17479980222",
                                     body=displaySituation(user))
    
    resp = twilio.twiml.Response()
    resp.message(message)

    return ''


if __name__ == "__main__":
    app.run(debug=False)
