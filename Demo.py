import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

webrtc_streamer(key="sample")
# Streamlit page configuration
st.set_page_config(page_title="Virtual Keyboard", layout="wide")
st.title("Interactive Virtual Keyboard")

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Define the video transformer class
class HandDetectionVideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

    def transform(self, frame):
        # Convert the frame to an OpenCV format
        img = frame.to_ndarray(format="bgr24")
        
        # Convert the image to RGB (MediaPipe works with RGB images)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect hands
        results = self.hands.process(rgb_img)

        # If hands are detected, draw landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        return img

# Streamlit WebRTC video streamer
webrtc_streamer(key="hand-detection", video_transformer_factory=HandDetectionVideoTransformer)
