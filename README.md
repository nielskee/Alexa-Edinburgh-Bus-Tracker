# Alexa-Edinburgh-Bus-Tracker
Playing with the Amazon Echo, following on from a work hackathon project

Pretty basic app to get the local bus times for you. Should be fairly straightforward to get up and running.

You'll need
* An Amazon Echo
* An Amazon AWS Account
* An Edinburgh Bus API Key (can be requested from here - http://www.mybustracker.co.uk/?page=API%20Key)

Simplest (and laziest) way is to copy the code straight over in the create AWS Lamdba workflow. You'll need the Utterances and intents when creating the Alexa Skill.

To get your local bus stop id, you can actually retrieve this directly from Google Maps by just clicking on the stop. This code requests for a single stop only but you can add multiple stops simply - just check the API guide in the link above for instructions.

