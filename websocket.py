from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from predictnextconfig import predictNextConfiguration

import json

# To solve "Too many packets in payload error" 
# see https://github.com/miguelgrinberg/python-engineio/issues/142 
from engineio.payload import Payload
Payload.max_decode_packets = 50

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#socketio stuffs
socketio = SocketIO(app)
yolo_event = "YOLO_EVENT"
light_change_needed_event = "LIGHT_CHANGE_NEEDED_EVENT"
next_config_ready_event = "NEXT_CONFIG_READY_EVENT"

# whether to enable debugging
debug = True

@app.route("/")
def main():
    socketio.emit("start event","main method called")
    return "Start of api call"

# for receiving data from client and sending back the output
# this one is particularly for the Machine Learning model input
# the input is an array and the output is an integer
@socketio.on(light_change_needed_event)
def get_next_light_configuration(received_data):
    deserialized_received_data = json.loads(received_data)

    next_configuration = predictNextConfiguration(deserialized_received_data)

    if debug:
        #**************Debug******************
        print(f"\nReceived_data: {deserialized_received_data}")
        print(f"\nPredicted configuration: {next_configuration}")
        #**************************************

    serialized_next_configuration = json.dumps(next_configuration)

    socketio.emit(next_config_ready_event, serialized_next_configuration)

# re-emitting the events emitted from client (yolo)
@socketio.on(yolo_event)
def re_emit_event(received_data):
    socketio.emit(yolo_event, received_data)

    if debug:
        #**************Debug******************
        print(f"\nRe-emitted Event : {yolo_event}")
        print(f"\nReceived data: {received_data}")
        #**************************************

if __name__ == '__main__':
    '''
    setting the host to "0.0.0.0" will expose the websocket over LAN properly
        but setting it to localhost or setting it empty won't expose it over lan.

        Also setting host to 0.0.0.0 will make it listen on all local ips regardless of the ip address ( if firewall allows it)
        so, ideal way is to configure it to lan ip address if intended to use over LAN. (e.g. 192.168.0.108)

    Here exposing doesn't mean dealing with the firewalls, the firewalls must be configured separately
    '''
    
    socketio.run(app, debug=True, host="0.0.0.0")
    