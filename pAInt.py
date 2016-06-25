import numpy as np
import cv2

class pAInt:
  def __init__(self):
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("fs_win", cv2.WND_PROP_FULLSCREEN)          
    cv2.setWindowProperty("fs_win", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

  def display_painting_carrusel():
    for 
    cv2.imshow("fs_win", painting)

  def display_webcam():
    while(True):
      ret, frame = cap.read()
      cv2.imshow('fs_win', gray)


  def display_photo():

  def display_waiting():
    pass

  def __del__():
    cv2.destroyAllWindows()
    cap.release()
