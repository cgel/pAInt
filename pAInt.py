import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
import random
import os
from operator import itemgetter

import pygame
import pygame.camera
from pygame.locals import *

import neuralStyle

pygame.init()
pygame.camera.init()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, ping_timeout=60*60*4)

# transition_flag = threading.Event()
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


@app.route('/index4.html')
def index4():
    return render_template('index4.html')


@app.route('/index5.html')
def index5():
    return render_template('index5.html')


def log(msg):
    print("======")
    print(msg)
    print("======")


# SETUP WEBSOCKET EVENTS
display_transition_data = ""


@socketio.on('transition event')
def handle_message(json):
    transition_url = server.handle_message(json)


class paintServer:

    def __init__(self,   ip="127.0.0.1", port=5000, log=False):
        self.ip = ip
        self.port = port
        self.log = log

    def start(self):
        self.event = threading.Event()
        print("starting server at", self.ip + ':' + str(self.port))
        socketio.run(app, host=self.ip, port=self.port,  log_output=self.log)

    def handle_message(self, json):
        source_name = json["source_name"]
        # welcome screen
        url_transition_dic = {"index.html": "index2.html",
                              "index2.html": "index3.html",
                              "index3.html": "index4.html",
                              "index4.html": "index5.html",
                              "index5.html": "index.html"}
        # the url that will be loaded by the browser once emit is called
        # try:
        target_url = url_transition_dic[source_name]
        # except KeyError:
        #    log("%s is not is url_transition_dic" % source_name)
        #    target_url = "index.html"
        # could try to catch KeyError

        # select painting screen
        if source_name == "index2.html":
            # data is the image number
            data = json["data"]
            display.set_style_number(data)
            display.set_display_target("webcam")

        # take picture screen
        elif source_name == "index3.html":
            # take picture in 3 secs and then call trigger_event
            display.set_display_target("take picture", self.event.set)
            # once trigger_event is called continue
            while not self.event.wait(.1):
                pass
            self.event.clear()

            # accept picture screen
        elif source_name == "index4.html":
            # data is a bool, accept or reject
            data = json["data"]
            # if repeat taking picture
            if data == 1:
                target_url = "index3.html"
                display.set_display_target("webcam")
            else:
                display.set_display_target(
                    "generate", self.event.set)

        elif source_name == "index5.html":
            while not self.event.wait(.1):
                pass
            self.event.clear()

        # take picture screen
        elif source_name == "index5.html":
            transition_name = "index.html"

        emit("load page", target_url)

    def __del_(self):
        socketio.stop()


class paintDisplay:

    def __init__(self):
        self.carrusel = pygame.image.load("carrusel.jpg")
        self.waiting = pygame.image.load("waiting.jpg")

        height = 1350
        width = 1080
        self.size = (width, height)
        #self.display = pygame.display.set_mode(self.size, pygame.FULLSCREEN, 0)
        self.display = pygame.display.set_mode(self.size, 0)

        self.cams = pygame.camera.list_cameras()
        if not self.cams:
            raise NameError("No cameras")
        self.cam_size = (1080, 720)
        self.cam = pygame.camera.Camera(self.cams[-1], self.cam_size)

        self.ratio = float(self.size[1]) / self.cam_size[1]
        self.cam_scale_size = (int(self.cam_size[0] * self.ratio), int( self.cam_size[1] * self.ratio))
        self.cam.start()

        self.event = threading.Event()

        self.style_number = 0
        self.neural = neuralStyle.neuralStyle()
        self.webcam_capture_name = "webcam_capture.jpg"

        # what should be displayed at every moment
        self.display_target = "carrusel"



    def set_style_number(self, number):
        self.style_number = number

    def default_callback(self):
        return
        raise NameError("No callback set, but it was called")

    def set_display_target(self, target, callback=default_callback):
        self.display_target = target
        self.callback = callback
        # set event so that the display transitions
        self.event.set()

    def display_webcam_frame(self):
        snapshot = self.cam.get_image()
        snapshot = pygame.transform.scale(snapshot, self.cam_scale_size)
        self.display.blit(snapshot, (-self.size[0]/2, 0))
        pygame.display.flip()

    def start(self):
        while True:
            if self.display_target == "carrusel":
                # load all generated images
                generated_list = os.listdir("generated")
                loaded_images = []
                for generated in generated_list:
                    loaded_images.append(pygame.image.load("generated/"+generated))

                if len(loaded_images) > 0:
                    #select the last image
                    index, loaded_image= max(enumerate(loaded_images), key=itemgetter(1))
                    self.display.blit(loaded_image, (0, 0))
                    pygame.display.flip()
                    last_change_t = time.time()
                    while not self.event.wait(.1):
                        # if time randomly display a new image
                        if time.time() - last_change_t > 20.:
                            last_change_t = time.time()
                            loaded_image = random.sample(loaded_images, 1)[0]
                            self.display.blit(loaded_image, (0, 0))
                            pygame.display.flip()
                else:
                    while not self.event.wait(.1):
                        pass
                self.event.clear()
                continue

            elif self.display_target == "generate":
                # show waiting screen
                self.display.blit(self.waiting, (0, 0))
                pygame.display.flip()

                # start generating
                log(self.style_number)
                self.neural.generate(self.style_number, self.webcam_capture_name)

                self.callback()
                self.display_target = "carrusel"
                continue

            elif self.display_target == "webcam":
                stop = False
                while(stop == False):
                    if self.event.isSet():
                        self.event.clear()
                        stop = True
                    self.display_webcam_frame()

            elif self.display_target == "take picture":
                start_time = time.time()
                delay = 3.
                while(time.time() - start_time < delay):
                    self.display_webcam_frame()

                self.callback()
                # save snapshot
                pygame.image.save(self.display, self.webcam_capture_name)

                while not self.event.wait(.1):
                    pass
                self.event.clear()

            else:
                raise NameError("Invalid display_target: %s" %
                                self.display_target)

    def __del__(self):
        log("deliting pAInt")

server = paintServer(ip="192.168.42.76")
#server = paintServer()
server_thread = threading.Thread(name="server thread",
                                 target=server.start)
server_thread.setDaemon(True)
server_thread.start()

display = paintDisplay()
display.start()

log("finishing")
