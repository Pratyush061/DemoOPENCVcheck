# import streamlit as st
# import cv2
# import numpy as np
# from cvzone.HandTrackingModule import HandDetector
# from cvzone.SelfiSegmentationModule import SelfiSegmentation
# import os
# import time
# from streamlit_webrtc import webrtc_streamer, WebRtcMode
# from utils.webrtc_helpers import process_video_frame
# # Define RTC Configuration with STUN and TURN servers
# RTC_CONFIGURATION = {
#     "iceServers": [
#         {
#             "urls": [
#                 "turn:173.194.72.127:19305?transport=udp",
#                 "turn:[2404:6800:4008:C01::7F]:19305?transport=udp",
#                 "turn:173.194.72.127:443?transport=tcp",
#                 "turn:[2404:6800:4008:C01::7F]:443?transport=tcp"
#             ],
#             "username": "CKjCuLwFEgahxNRjuTAYzc/s6OMT",
#             "credential": "u1SQDR/SQsPQIxXNWQT7czc/G4c="
#         },
#         {
#             "urls": ["stun:stun.l.google.com:19302"]
#         }
#     ]
# }

# # Streamlit settings
# st.set_page_config(page_title="Virtual Keyboard", layout="wide")
# st.title("Interactive Virtual Keyboard")
# st.subheader('''
# Turn on the webcam and use hand gestures to interact with the virtual keyboard.
# Use 'a' and 'd' from the keyboard to change the background.
# ''')

# # Initialize
# detector = HandDetector(maxHands=1, detectionCon=0.8)
# segmentor = SelfiSegmentation()
# keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
#         ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
#         ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# listImg = os.listdir('street')
# imgList = [cv2.imread(f'street/{imgPath}') for imgPath in listImg]
# indexImg = 0

# # Shared state for output text
# if "output_text" not in st.session_state:
#     st.session_state["output_text"] = ""

# # Webcam stream via WebRTC
# webrtc_streamer(
#     key="virtual-keyboard",
#     mode=WebRtcMode.SENDRECV,
#     media_stream_constraints={"video": True, "audio": False},
#     video_frame_callback=lambda frame: process_video_frame(
#         frame, detector, segmentor, imgList, indexImg, keys, st.session_state
#     ),
# )

# # Output text display
# st.subheader("Output Text")
# st.text_area("Live Input:", value=st.session_state["output_text"], height=200)


2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import google.generativeai as genai
from PIL import Image
import streamlit as st
 
 
st.set_page_config(layout="wide")
st.image('MathGestures.png')
 
col1, col2 = st.columns([3,2])
with col1:
    run = st.checkbox('Run', value=True)
    FRAME_WINDOW = st.image([])
 
with col2:
    st.title("Answer")
    output_text_area = st.subheader("")
 
 
genai.configure(api_key="AIzaSyAu7w2tMO4kIAiB-RDMh8vywmF8OqBjpQk")
model = genai.GenerativeModel('gemini-1.5-flash')
 
# Initialize the webcam to capture video
# The '2' indicates the third camera connected to your computer; '0' would usually refer to the built-in camera
cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
 
# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)
 
 
def getHandInfo(img):
    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' parameter flips the image, making it easier for some detections
    hands, img = detector.findHands(img, draw=False, flipType=True)
 
    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand = hands[0]  # Get the first hand detected
        lmList = hand["lmList"]  # List of 21 landmarks for the first hand
        # Count the number of fingers up for the first hand
        fingers = detector.fingersUp(hand)
        print(fingers)
        return fingers, lmList
    else:
        return None
 
def draw(info,prev_pos,canvas):
    fingers, lmList = info
    current_pos= None
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lmList[8][0:2]
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas,current_pos,prev_pos,(255,0,255),10)
    elif fingers == [1, 0, 0, 0, 0]:
        canvas = np.zeros_like(img)
 
    return current_pos, canvas
 
def sendToAI(model,canvas,fingers):
    if fingers == [1,1,1,1,0]:
        pil_image = Image.fromarray(canvas)
        response = model.generate_content(["Solve this math problem", pil_image])
        return response.text
 
 
prev_pos= None
canvas=None
image_combined = None
output_text= ""
# Continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
 
    if canvas is None:
        canvas = np.zeros_like(img)
 
 
    info = getHandInfo(img)
    if info:
        fingers, lmList = info
        prev_pos,canvas = draw(info, prev_pos,canvas)
        output_text = sendToAI(model,canvas,fingers)
 
    image_combined= cv2.addWeighted(img,0.7,canvas,0.3,0)
    FRAME_WINDOW.image(image_combined,channels="BGR")
 
    if output_text:
        output_text_area.text(output_text)
 
    # # Display the image in a window
    # cv2.imshow("Image", img)
    # cv2.imshow("Canvas", canvas)
    # cv2.imshow("image_combined", image_combined)
 
 
    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)
