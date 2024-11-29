import streamlit as st
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import time
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from utils.webrtc_helpers import process_video_frame
# Define RTC Configuration with STUN and TURN servers
RTC_CONFIGURATION = {
    "iceServers": [
        {
            "urls": [
                "turn:173.194.72.127:19305?transport=udp",
                "turn:[2404:6800:4008:C01::7F]:19305?transport=udp",
                "turn:173.194.72.127:443?transport=tcp",
                "turn:[2404:6800:4008:C01::7F]:443?transport=tcp"
            ],
            "username": "CKjCuLwFEgahxNRjuTAYzc/s6OMT",
            "credential": "u1SQDR/SQsPQIxXNWQT7czc/G4c="
        },
        {
            "urls": ["stun:stun.l.google.com:19302"]
        }
    ]
}

# Streamlit settings
st.set_page_config(page_title="Virtual Keyboard", layout="wide")
st.title("Interactive Virtual Keyboard")
st.subheader('''
Turn on the webcam and use hand gestures to interact with the virtual keyboard.
Use 'a' and 'd' from the keyboard to change the background.
''')

# Initialize
detector = HandDetector(maxHands=1, detectionCon=0.8)
segmentor = SelfiSegmentation()
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

listImg = os.listdir('street')
imgList = [cv2.imread(f'street/{imgPath}') for imgPath in listImg]
indexImg = 0

# Shared state for output text
if "output_text" not in st.session_state:
    st.session_state["output_text"] = ""

# Webcam stream via WebRTC
webrtc_streamer(
    key="virtual-keyboard",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={"video": True, "audio": False},
    video_frame_callback=lambda frame: process_video_frame(
        frame, detector, segmentor, imgList, indexImg, keys, st.session_state
    ),
)

# Output text display
st.subheader("Output Text")
st.text_area("Live Input:", value=st.session_state["output_text"], height=200)
