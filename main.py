import requests
import pprint
import json
import threading
import time
import datetime
import sys
import config as config
from flask import request
from flask import Flask

app = Flask(__name__)
station_data = {}
pp = pprint.PrettyPrinter(indent=4)


def send_it():
    threading.Timer(config.FREQUENCY, send_it).start()
    global station_data
    if 'ID' in station_data:
        pretty_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        pretty_data = json.dumps(station_data)
        pretty_data = pretty_data.replace(station_data['PASSWORD'], '*****')
        sys.stdout.write('[%s] sending info: %s\n' % (pretty_date, pretty_data))
        r = requests.get(url='https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php', params=station_data)
        if 'success' not in r.text:
            pretty_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            sys.stdout.write('[%s] ERROR SENDING DATA: %s\n' % (pretty_date, r.text))
    sys.stdout.flush()


@app.route('/weatherstation/updateweatherstation')
def capture_it():
    if (request.args['mt'].startswith('5N1x')):
        credentials = {
            'ID': config.STATION_ID,
            'PASSWORD': config.STATION_KEY,
            'realtime': '1',
            'rtfreq': config.FREQUENCY
        }
        global station_data
        station_data.update(credentials)
        new_station_data = request.args.copy()
        new_station_data.pop('id', None)
        station_data.update(new_station_data)

    return ('', 204)

send_it()
