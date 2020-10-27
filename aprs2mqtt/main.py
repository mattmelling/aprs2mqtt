import json
import os
import requests
import paho.mqtt.publish as publish

CALLSIGNS = os.environ['APRS_CALLSIGNS'].split(',')


def get_callsign_lock_name(callsign):
    return f'{os.environ["LOCK_LOCATION"]}/{callsign}.lock'


def get_last_message_timestamp(callsign):
    filename = get_callsign_lock_name(callsign)
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return int(f.read())
    return 0


def set_last_message_timestamp(callsign, timestamp):
    filename = get_callsign_lock_name(callsign)
    with open(filename, 'w') as f:
        f.write(str(timestamp) + '\n')


def get_messages_for_callsign(callsign):
    key = os.environ['APRSFI_KEY']
    url = f'https://api.aprs.fi/api/get?what=msg&dst={callsign}&apikey={key}' \
        + '&format=json'
    last_timestamp = get_last_message_timestamp(callsign)
    response = requests.get(url).json()
    messages = response['entries']
    messages.sort(key=lambda x: int(x['time']))
    for message in messages:
        t = int(message['time'])
        if t > last_timestamp:
            last_timestamp = t
            yield message
    set_last_message_timestamp(callsign, last_timestamp)


def publish_messages(messages):
    publish.multiple(({
        'topic': os.environ['MQTT_TOPIC'],
        'payload': json.dumps(message),
    } for message in messages),
                     hostname=os.environ['MQTT_HOST'],
                     port=int(os.environ['MQTT_PORT']),
                     client_id=os.environ['MQTT_USER'],
                     auth={
                         'username': os.environ['MQTT_USER'],
                         'password': os.environ['MQTT_PASSWORD']
                     })


def main():
    for callsign in CALLSIGNS:
        messages = list(get_messages_for_callsign(callsign))
        if len(messages) > 0:
            publish_messages(messages)


if __name__ == '__main__':
    main()
