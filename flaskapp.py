from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#transition_flag = threading.Event()
transition_msg = ""

# SETUP SERVER
@app.route('/index.html')
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/index2.html')
def index2():
  return render_template('index2.html')

@app.route('/index3.html')
def index3():
  return render_template('index3.html')


# SETUP WEBSOCKET EVENTS 
@socketio.on('json')
def handle_message(json):
  print("======")
  print('transition event: ' + str(json))
  print("======")
  source_url = json["href"]
  #welcome screen
  if source_url == "index.html":
    transition_url = "index2.html"

  #select painting screen
  elif source_url == "index2.html":
    #data is the image number
    data = json["data"]
    global image_number
    image_number = data
    transition_url = "index3.html"

  #take picture screen
  elif source_url == "index3.html":
    transition_url = "index4.html"

  #accept picture screen
  elif source_url == "index4.html":
    #data is a bool, accept or reject
    data = json["data"]
    if data:
      transition_url = "index4.html"
    else:
      transition_url = "index5.html"
  else:
    raise Exception("Unknown source: "%source)
  send(transition_url)

@socketio.on('transition event')
def handle_message(message):
  print('recived click event: ' + str(message))

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

print("================")
socketio.run(app)
print("================")
