#import 
import cv2 
import mediapipe as mp 
import time
import math
import numpy as np

#載入mediapipe Pose
mpDraw = mp.solutions.drawing_utils 
mpPose = mp.solutions.pose 
pose = mpPose.Pose() 
PoseLmsStyle = mpDraw.DrawingSpec(color = (0,0,255), thickness=10)
PoseConStyle = mpDraw.DrawingSpec(color = (0,255,0), thickness=5)

#初始次數、狀態設定
squatcount = 0
squatstate = 'up'
ShoulderPushCount = 0
ShoulderPushState = 'down'
#初始次數、狀態設定
BicepsCurlcount = 0
BicepsCurlState = 'down'

#計算角度
def angle(point1,point2,point3):
    
    point1 = np.array(point1)
    point2 = np.array(point2)
    point3 = np.array(point3) 
    
    radians = np.arctan2(point3[1]-point2[1], point3[0]-point2[0]) - np.arctan2(point1[1]-point2[1], point1[0]-point2[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 


#開啟視訊鏡頭
cap = cv2.VideoCapture(0)

while True: 
    ret, img = cap.read() 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    results = pose.process(imgRGB)
    #imgHeight = img.shape[0]
    #imgWidth = img.shape[1]
    
    if results.pose_landmarks : 
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS, PoseLmsStyle, PoseConStyle)
        
    
        landmarks = results.pose_landmarks.landmark
        
        #深蹲
        right_hip = [landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].y]
        left_hip = [landmarks[mpPose.PoseLandmark.LEFT_HIP.value].x, landmarks[mpPose.PoseLandmark.LEFT_HIP.value].y]
        right_knee = [landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mpPose.PoseLandmark.RIGHT_KNEE.value].y]
        left_knee = [landmarks[mpPose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mpPose.PoseLandmark.LEFT_KNEE.value].y]
        #肩推
        right_elbow = [landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].y]
        left_elbow = [landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value].y]
        nose = [landmarks[mpPose.PoseLandmark.NOSE.value].x,landmarks[mpPose.PoseLandmark.NOSE.value].y]
        #二頭彎舉
        right_shoulder = [landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y]
        left_shoulder = [landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value].y]
        right_wrist = [landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y]
        left_wrist = [landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].y]
        
        
        #cv2.putText(img,f"right_hip: {int(right_hip[1] * imgHeight)}",(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),2)
        #cv2.putText(img,f"left_hip: {int(left_hip[1] * imgHeight)}",(30,60),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),2)
        #cv2.putText(img,f"right_knee: {int(right_knee[1] * imgHeight)}",(30,90),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),2)
        #cv2.putText(img,f"left_knee: {int(left_knee[1] * imgHeight)}",(30,120),cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),2)
        
        
        #深蹲
        if (right_hip[1] > right_knee[1] and left_hip[1] > left_knee[1]) and squatstate == 'up':
            squatstate = 'down'
            squatcount += 1
            #print(squatcount)
        
        if(right_hip[1] < right_knee[1] and left_hip[1] < left_knee[1]) and squatstate == 'down':
            squatstate = 'up'

        #肩推
        if (right_elbow[1] < nose[1] and left_elbow[1] < nose[1]) and ShoulderPushState == 'down':
            ShoulderPushState = 'up'
            ShoulderPushCount += 1
            
            
        if (right_elbow[1] > nose[1] and left_elbow[1] > nose[1]) and ShoulderPushState == 'up':
            ShoulderPushState = 'down'
        
        #二頭彎舉
        right_angle = angle(right_shoulder,right_elbow,right_wrist)
        left_angle = angle(left_shoulder,left_elbow,left_wrist)
        
        if right_angle > 150 and left_angle > 150:
            BicepsCurlState = "down"
        if right_angle < 45 and left_angle < 45 and BicepsCurlState =='down':
            BicepsCurlState="up"
            BicepsCurlcount +=1
    

    
    
    #顯示次數
    cv2.putText(img,"squat",(530,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    cv2.putText(img,str(squatcount),(600,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    
    cv2.putText(img,"ShoulderPush",(500,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    cv2.putText(img,str(ShoulderPushCount),(620,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    
    cv2.putText(img,"BicepsCurl",(515,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    cv2.putText(img,str(BicepsCurlcount),(610,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
            
    cv2.imshow("img", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):    
        break

cv2.destroyAllWindows()

