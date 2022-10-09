from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

from predictnextconfig import predictNextConfiguration

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app)

@app.route("/")
def main():
    socketio.emit("start event","main method called")
    return "Start of api call"

@socketio.on('traffic')
def trafficControl(data):
    print(data)

# for receiving data from client and sending back the output
# this one is particularly for the Machine Learning model input
# the input is an array and the output is an integer
@socketio.event(namespace='/predict-traffic')
def response(server_id, received_data):
    next_configuration = predictNextConfiguration(received_data)

    #**************Debug******************
    print(f"\nserver_id: {server_id}. received_data: {received_data}")
    print(f"\nPredicted configuration: {next_configuration}")
    #**************************************

    socketio.send(next_configuration)
    

if __name__ == '__main__':
    socketio.run(app, debug=True)