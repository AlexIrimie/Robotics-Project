import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import time
import enum

import PhantomFuncs as pf

class PoseLandmark(enum.IntEnum):
  """The 33 pose landmarks."""
  NOSE = 0
  LEFT_EYE_INNER = 1
  LEFT_EYE = 2
  LEFT_EYE_OUTER = 3
  RIGHT_EYE_INNER = 4
  RIGHT_EYE = 5
  RIGHT_EYE_OUTER = 6
  LEFT_EAR = 7
  RIGHT_EAR = 8
  MOUTH_LEFT = 9
  MOUTH_RIGHT = 10
  LEFT_SHOULDER = 11
  RIGHT_SHOULDER = 12
  LEFT_ELBOW = 13
  RIGHT_ELBOW = 14
  LEFT_WRIST = 15
  RIGHT_WRIST = 16
  LEFT_PINKY = 17
  RIGHT_PINKY = 18
  LEFT_INDEX = 19
  RIGHT_INDEX = 20
  LEFT_THUMB = 21
  RIGHT_THUMB = 22
  LEFT_HIP = 23
  RIGHT_HIP = 24
  LEFT_KNEE = 25
  RIGHT_KNEE = 26
  LEFT_ANKLE = 27
  RIGHT_ANKLE = 28
  LEFT_HEEL = 29
  RIGHT_HEEL = 30
  LEFT_FOOT_INDEX = 31
  RIGHT_FOOT_INDEX = 32
  
  
frameWidth = 1280
frameHeight = 720
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
cap1.set(3, frameWidth)
cap1.set(4, frameHeight)
cap2.set(3, frameWidth)
cap2.set(4, frameHeight)
mpHands=mp.solutions.pose
hands=mpHands.Pose()
mpDraw = mp.solutions.drawing_utils


while True:
    success1, img1 = cap1.read()
    success2, img2 = cap2.read()
    img1= cv2.flip(img1,1)
    img2= cv2.flip(img2,1)
    imgRGB1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    imgRGB2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    results1 = hands.process(imgRGB1)
    results2 = hands.process(imgRGB2)
    
    
    new_landmarks1 = landmark_pb2.NormalizedLandmarkList()
    new_landmarks1.landmark.append(results1.pose_landmarks.landmark[PoseLandmark.LEFT_SHOULDER])
    new_landmarks1.landmark.append(results1.pose_landmarks.landmark[PoseLandmark.LEFT_ELBOW])
    new_landmarks1.landmark.append(results1.pose_landmarks.landmark[PoseLandmark.LEFT_WRIST])
    new_landmarks2 = landmark_pb2.NormalizedLandmarkList()
    new_landmarks2.landmark.append(results2.pose_landmarks.landmark[PoseLandmark.LEFT_SHOULDER])
    new_landmarks2.landmark.append(results2.pose_landmarks.landmark[PoseLandmark.LEFT_ELBOW])
    new_landmarks2.landmark.append(results2.pose_landmarks.landmark[PoseLandmark.LEFT_WRIST])
    
    mpDraw.draw_landmarks(img1, new_landmarks1)
    mpDraw.draw_landmarks(img2, new_landmarks2)
    
    print("Camera 1: " + str(new_landmarks1.landmark[0]))
    print("Camera 2: " + str(new_landmarks1.landmark[1]))
    
    # cv2.imshow('Camera 1', img1)
    # cv2.imshow('Camera 2', img2)
    
    # if cv2.waitKey(1)==27:
    #     break