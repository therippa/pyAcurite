## pyAcurite

A simple service that takes the data from the Acurite SmartHub (to be discontinued Summer 2018 due to Acurite being a bad and stupid company), and sends it off to Weather Underground.

I started setting up weewx, but it seemed like a lot of overhead for a simple thing, so I made this.

This uses the "listen" method, so you must be able to configure your router to point the DNS entry of hubapi.myacurite.com to something listening on your local network (PC or raspberry pi).  Traffic that the SmartHub sends out will now be routed to that device.

This could also easily be used with the "sniffing" method - just forward the data to http://\<pyacurite-device\>/weatherstation/updateweatherstation

### Configuration
Copy config.example.py to config.py, and in an editor set your STATION_ID and STATION_KEY.  These can be found on your Weather Underground station setting page.  Also here you can adjust the frequency to send data, and choose whether to still forward the data to Acurite's server.

### Usage
First, install the requirements:

`pip install requirements.txt`

Then, run the app on port 80 using something like this:

`sudo FLASK_APP=main.py flask run --host=0.0.0.0 --port=80`

or run it on its default port (5000) and set up a reverse proxy with nginx or apache.
