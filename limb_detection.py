import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import time
import enum



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
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
mpHands=mp.solutions.pose
hands=mpHands.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    img= cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    new_landmarks = landmark_pb2.NormalizedLandmarkList()
    new_landmarks.landmark.append(results.pose_landmarks.landmark[PoseLandmark.LEFT_SHOULDER])
    new_landmarks.landmark.append(results.pose_landmarks.landmark[PoseLandmark.LEFT_ELBOW])
    new_landmarks.landmark.append(results.pose_landmarks.landmark[PoseLandmark.LEFT_WRIST])
    
    
    
    print(new_landmarks)

    if results.pose_landmarks:
        # mpDraw.draw_landmarks(img, results.pose_landmarks, mpHands.POSE_CONNECTIONS)#drawing points and lines(=handconections)
        # mpDraw.draw_landmarks(img, new_landmarks, mpHands.POSE_CONNECTIONS)#drawing points and lines(=handconections)
        mpDraw.draw_landmarks(img, new_landmarks)#drawing points and lines(=handconections)
        # mpDraw.plot_landmarks(results.pose_landmarks, mpHands.POSE_CONNECTIONS)

    #Write frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 0), 1)
    # cv2.putText(img, "Points: " + str(int(results.pose_landmarks)), (20, 30), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,0),1)
    
    cv2.imshow('image', img)
    if cv2.waitKey(1)==27:
        break