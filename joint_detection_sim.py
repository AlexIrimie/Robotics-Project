import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import time
import enum


import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Joint Movement Simulation")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Initial joint coordinates
joint1_x, joint1_y = width // 2, height // 2
joint2_x, joint2_y = joint1_x + 50, joint1_y  # Adjust the initial position of joint2
joint3_x, joint3_y = joint2_x + 50, joint2_y  # Adjust the initial position of joint3

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()



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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    success, img = cap.read()
    img= cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    try:
        new_landmarks = landmark_pb2.NormalizedLandmarkList()
        new_landmarks.landmark.append(results.pose_landmarks.landmark[PoseLandmark.LEFT_SHOULDER])
        new_landmarks.landmark.append(results.pose_landmarks.landmark[PoseLandmark.LEFT_ELBOW])
        new_landmarks.landmark.append(results.pose_landmarks.landmark[PoseLandmark.LEFT_WRIST])
    except:
        continue
    
    # print(new_landmarks)
    
    
    joint1_x, joint1_y = new_landmarks.landmark[0].x*frameWidth, new_landmarks.landmark[0].y*frameHeight  # Replace these values with your coordinates for joint 1
    joint2_x, joint2_y = new_landmarks.landmark[1].x*frameWidth, new_landmarks.landmark[1].y*frameHeight  # Replace these values with your coordinates for joint 2
    joint3_x, joint3_y = new_landmarks.landmark[2].x*frameWidth, new_landmarks.landmark[2].y*frameHeight # Replace these values with your coordinates for joint 3

    # Update display
    screen.fill(white)
    pygame.draw.circle(screen, black, (int(joint1_x), int(joint1_y)), 20)
    pygame.draw.circle(screen, black, (int(joint2_x), int(joint2_y)), 20)
    pygame.draw.circle(screen, black, (int(joint3_x), int(joint3_y)), 20)

    # Draw lines connecting the joints
    pygame.draw.line(screen, black, (int(joint1_x), int(joint1_y)), (int(joint2_x), int(joint2_y)), 5)
    pygame.draw.line(screen, black, (int(joint2_x), int(joint2_y)), (int(joint3_x), int(joint3_y)), 5)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
    

    # if results.pose_landmarks:
    #     # mpDraw.draw_landmarks(img, results.pose_landmarks, mpHands.POSE_CONNECTIONS)#drawing points and lines(=handconections)
    #     # mpDraw.draw_landmarks(img, new_landmarks, mpHands.POSE_CONNECTIONS)#drawing points and lines(=handconections)
    #     mpDraw.draw_landmarks(img, new_landmarks)#drawing points and lines(=handconections)
    #     # mpDraw.plot_landmarks(results.pose_landmarks, mpHands.POSE_CONNECTIONS)

    #Write frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 0), 1)
    # cv2.putText(img, "Points: " + str(int(results.pose_landmarks)), (20, 30), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,0),1)
    
    # cv2.imshow('image', img)
    # if cv2.waitKey(1)==27:
    #     break