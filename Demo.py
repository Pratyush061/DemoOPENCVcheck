import streamlit as st
import cv2
import numpy as np
import mediapipe as mp

# Streamlit page configuration
st.set_page_config(page_title="Virtual Keyboard", layout="wide")
st.title("Interactive Virtual Keyboard")

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Streamlit webcam input
frame = st.camera_input("Take a picture")

if frame:
    # Convert the Streamlit image to an OpenCV format
    img = frame.to_image()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Convert the image to RGB (MediaPipe works with RGB images)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image and detect hands
    results = hands.process(rgb_img)

    # If hands are detected, draw landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Display the processed image with hand landmarks in Streamlit
    st.image(img, channels="BGR", use_column_width=True)
