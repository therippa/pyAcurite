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
station_data = {
    'ID': config.STATION_ID,
    'PASSWORD': config.STATION_KEY,
    'realtime': '1',
    'rtfreq': config.FREQUENCY,
    'softwaretype': 'PyAcurite'
}
raw_station_data = {}
pp = pprint.PrettyPrinter(indent=4)


def log_it(title, message, err=False):
    pretty_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    sys.stdout.write('[%s] %s: %s\n' % (pretty_date, title, message))
    sys.stdout.flush()
    if err:
        sys.stderr.write('[%s] %s: %s\n' % (pretty_date, title, message))
        sys.stderr.flush()


def send_it():
    threading.Timer(config.FREQUENCY, send_it).start()
    if 'tempf' in station_data:
        pretty_data = json.dumps(station_data)
        pretty_data = pretty_data.replace(station_data['PASSWORD'], '*****')
        log_it('Sending data', pretty_data)
        r = requests.get(url='https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php', params=station_data)
        if 'success' not in r.text:
            log_it('ERROR SENDING DATA', r.text, True)
        if config.SEND_TO_ACURITE:
            acurite = requests.get(url=('http://%s/weatherstation/updateweatherstation' % config.ACURITE_HUB_IP), params=raw_station_data)
            if acurite.status_code != requests.codes.ok:
                log_it('ERROR SENDING DATA TO ACURITE', acurite.text, True)


@app.route('/weatherstation/updateweatherstation')
def capture_it():
    if (request.args['mt'].startswith('5N1x')):
        global station_data
        global raw_station_data
        new_station_data = request.args.copy()
        raw_station_data = request.args.copy()
        new_station_data.pop('id', None)
        station_data.update(new_station_data)

    return ('', 204)

send_it()
