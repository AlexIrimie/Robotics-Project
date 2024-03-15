import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import enum

import PhantomFuncs as pf


class PoseLandmark(enum.IntEnum):
    LEFT_SHOULDER = 11
    LEFT_ELBOW = 13
    LEFT_WRIST = 15

frameWidth = 1280
frameHeight = 720
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)
cap1.set(3, frameWidth)
cap1.set(4, frameHeight)
cap2.set(3, frameWidth)
cap2.set(4, frameHeight)
mpPose=mp.solutions.pose
pose=mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

# Initialize 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

while True:
    success1, img1 = cap1.read()
    success2, img2 = cap2.read()
    img1 = cv2.flip(img1, 1)
    img2 = cv2.flip(img2, 1)
    imgRGB1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    imgRGB2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    try:
        
        results1 = pose.process(imgRGB1)
        results2 = pose.process(imgRGB2)


        new_landmarks1 = landmark_pb2.NormalizedLandmarkList()
        new_landmarks1.landmark.append(results1.pose_landmarks.landmark[PoseLandmark.LEFT_SHOULDER])
        new_landmarks1.landmark.append(results1.pose_landmarks.landmark[PoseLandmark.LEFT_ELBOW])
        new_landmarks1.landmark.append(results1.pose_landmarks.landmark[PoseLandmark.LEFT_WRIST])

        new_landmarks2 = landmark_pb2.NormalizedLandmarkList()
        new_landmarks2.landmark.append(results2.pose_landmarks.landmark[PoseLandmark.LEFT_SHOULDER])
        new_landmarks2.landmark.append(results2.pose_landmarks.landmark[PoseLandmark.LEFT_ELBOW])
        new_landmarks2.landmark.append(results2.pose_landmarks.landmark[PoseLandmark.LEFT_WRIST])

        # Extract x-coordinates from new_landmarks2 for depth estimation
        # x_coordinate_camera2 = new_landmarks2.landmark[1].x  # Use the appropriate index

        # Estimate depth using triangulation (replace this with your depth estimation logic)
        # baseline = 10.0  # Adjust this based on your setup
        # depth = (baseline * new_landmarks1.landmark[1].x) / (new_landmarks1.landmark[1].x - x_coordinate_camera2)

        # print("Depth:", depth)
        
        
        joint1_x, joint1_y, joint1_z = pf.depth_estimate(new_landmarks1.landmark[0].x, new_landmarks1.landmark[0].y, new_landmarks2.landmark[0].x, new_landmarks2.landmark[0].y)
        joint2_x, joint2_y, joint2_z = pf.depth_estimate(new_landmarks1.landmark[1].x, new_landmarks1.landmark[1].y, new_landmarks2.landmark[1].x, new_landmarks2.landmark[1].y)
        joint3_x, joint3_y, joint3_z = pf.depth_estimate(new_landmarks1.landmark[2].x, new_landmarks1.landmark[2].y, new_landmarks2.landmark[2].x, new_landmarks2.landmark[2].y)
        
        
        
        

        # Plot 3D arm visualization
        ax.cla()
        ax.set_xlim([0, 5])
        ax.set_ylim([0, 5])
        ax.set_zlim([0, 5])  # Adjust the Z-axis limits based on your scene
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Plot the arm
        ax.plot([3 * joint1_x, 3 * joint2_x],
                [3 * joint1_y, 3 * joint2_y],
                [3 * joint1_z, 3 * joint2_z], label='Joint 1 to Joint 2')

        ax.plot([3 * joint2_x, 3 * joint3_x],
                [3 * joint2_y, 3 * joint3_y],
                [3 * joint2_z, 3 * joint3_z], label='Joint 2 to Joint 3')

        # ax.plot([new_landmarks1.landmark[1].x * frameWidth, new_landmarks2.landmark[1].x * frameWidth],
        #         [new_landmarks1.landmark[1].y * frameHeight, new_landmarks2.landmark[1].y * frameHeight],
        #         [depth, depth], label='Joint 3 to End Effector')

        # # Plot joints
        # ax.scatter([new_landmarks1.landmark[0].x * frameWidth, new_landmarks1.landmark[1].x * frameWidth,
        #             new_landmarks2.landmark[1].x * frameWidth],
        #            [new_landmarks1.landmark[0].y * frameHeight, new_landmarks1.landmark[1].y * frameHeight,
        #             new_landmarks2.landmark[1].y * frameHeight],
        #            [depth, depth, depth], c='r', marker='o', label='Joints')
        
        
        # ax.scatter([joint1_x * frameWidth, joint1_y * frameHeight,
        #             joint1_z * frameWidth],
        #            [joint2_x * frameWidth, joint2_y * frameHeight,
        #             joint2_z * frameWidth],
        #            [joint3_x * frameWidth, joint3_y * frameHeight, joint3_z * frameWidth], c='r', marker='o', label='Joints')
        
        
        joint1_coords =  [3 * joint1_x, 3 * joint1_y, 3 * joint1_z]
        joint2_coords = [3 * joint2_x, 3 * joint2_y, 3 * joint2_z]
        joint3_coords = [3 * joint3_x, 3 * joint3_y, 3 * joint3_z]
        
        print("Joints seen")
        

        # ax.scatter([joint1_x, joint1_y,
        #             joint1_z],
        #            [joint2_x, joint2_y,
        #             joint2_z],
        #            [joint3_x, joint3_y, joint3_z], c='r', marker='o', label='Joints')
        
        # Plot joints
        ax.scatter(*joint1_coords, c='r', marker='o', label='Shoulder')
        ax.scatter(*joint2_coords, c='g', marker='o', label='Elbow')
        ax.scatter(*joint3_coords, c='b', marker='o', label='Wrist')

        # Add legend
        ax.legend()

        plt.pause(0.01)  # Adjust the pause time as needed
    
    except:
        print("Joints not seen")
