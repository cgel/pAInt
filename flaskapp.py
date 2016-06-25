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

def log(msg):
  print("======")
  print(msg)
  print("======")


# SETUP WEBSOCKET EVENTS 
@socketio.on('transition event')
def handle_message(json):
  print("======")
  print('transition event: ' + str(json))
  print("======")
  source_name = json["source_name"]
  #welcome screen
  if source_name == "index.html":
    log("transition from index.html")
    transition_name = "index2.html"

  #select painting screen
  elif source_name == "index2.html":
    #data is the image number
    data = json["data"]
    global image_number
    image_number = data
    transition_name = "index3.html"

  #take picture screen
  elif source_name == "index3.html":
    transition_name = "index4.html"

  #accept picture screen
  elif source_name == "index4.html":
    #data is a bool, accept or reject
    data = json["data"]
    if data:
      transition_name = "index4.html"
    else:
      transition_name = "index5.html"
  else:
    raise Exception("Unknown source: "%source)

  log("emiting")
  emit("load page", transition_name)
  print('recived click event: ' + str(json))

try:
  socketio.run(app)
  socketio.stop()
except:
  socketio.stop()
