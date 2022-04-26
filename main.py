import cv2
import mediapipe as mp
from morse_code_table import morse_code_table
from toolbox import *
import time

'''
Initiate video feed
'''
capture = cv2.VideoCapture(0)

mp_drawing_utilities = mp.solutions.drawing_utils
mp_facemesh = mp.solutions.face_mesh
facemesh = mp_facemesh.FaceMesh(max_num_faces = 2)
drawing_spec = mp_drawing_utilities.DrawingSpec(thickness = 1, circle_radius = 2)
    
'''
Variables required within the while loop
'''
left_ear_prev = []
right_ear_prev = []
word = []
interpretable_blink = False
blink_duration = 0
no_blink_duration = 0
blink_detected = False
morse_sequence = ""
parsed_letter = ""
prev_time = 0


'''
Main program while loop
'''
while True:
    
    success, feed = capture.read()
    scaled = rescale_frame(feed, 150)

    image_RGB = cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB)
    results = facemesh.process(image_RGB)

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    count = 0
    if (results.multi_face_landmarks):
        for face_landmark in results.multi_face_landmarks:
            mp_drawing_utilities.draw_landmarks(scaled, face_landmark, mp_facemesh.FACEMESH_CONTOURS, drawing_spec, drawing_spec)

            '''
            In order to detect a blink, the 'eye aspect ratio' or 'ear' value needs to be calculated for each eye.
            '''
            left_ear = abs((face_landmark.landmark[160].x - face_landmark.landmark[144].x) ** 2 - (face_landmark.landmark[160].y - face_landmark.landmark[144].y) ** 2) + abs((face_landmark.landmark[158].x - face_landmark.landmark[153].x) ** 2 - (face_landmark.landmark[158].y - face_landmark.landmark[153].y) ** 2) / abs(((face_landmark.landmark[33].x - face_landmark.landmark[133].x) ** 2) - ((face_landmark.landmark[33].y - face_landmark.landmark[133].y) ** 2)) 
            right_ear = abs((face_landmark.landmark[385].x - face_landmark.landmark[380].x) ** 2 - (face_landmark.landmark[385].y - face_landmark.landmark[380].y) ** 2 ) + abs((face_landmark.landmark[387].x - face_landmark.landmark[373].x) ** 2- (face_landmark.landmark[387].y - face_landmark.landmark[373].y) ** 2 ) / abs(((face_landmark.landmark[362].x - face_landmark.landmark[263].x) ** 2) - ((face_landmark.landmark[362].y - face_landmark.landmark[263].y) ** 2)) 

            count = 0 if (count > 10) else (count + 1)
          
            if (len(left_ear_prev) > 10):
                left_ear_prev[count] = left_ear
                interpretable_blink = True
            else:
                left_ear_prev.append(left_ear)
                
            if (len(right_ear_prev) > 10):
                right_ear_prev[count] = right_ear
                interpretable_blink = True
            else:
                right_ear_prev.append(right_ear)

            if (interpretable_blink):
                if (((left_ear_prev[abs(count-9)] * 0.70) > left_ear) and ((right_ear_prev[abs(count-9)] * 0.70) > right_ear)):
                    blink_detected = True
                    blink_duration += 1
                else:
                    if (blink_duration > (fps * 0.6)):
                        print(fps)
                        morse_sequence += "_"
                        blink_duration = 0
                        
                    elif (blink_duration > int(fps / 8)):
                        morse_sequence += "."
                        blink_duration = 0
                        
                    else:
                        no_blink_duration += 1
                        if(no_blink_duration > (fps * 3)):
                            print(morse_sequence)
                            if morse_sequence in morse_code_table:
                                parsed_letter = morse_code_table[morse_sequence]
                                word.append(parsed_letter)
                                morse_sequence = ""
                            morse_sequence = ""
                            no_blink_duration = 0                            

    complete_word = ''.join(word)
    cv2.putText(scaled, str(int(fps)), (50,50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)
    cv2.putText(scaled, str(complete_word), (80,100),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
    cv2.imshow("Image", scaled)
    key = cv2.waitKey(1)

    '''
    Keyboard interrupt
    '''
    if (key == ord('q')):
        break