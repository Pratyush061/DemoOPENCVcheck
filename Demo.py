# Use Streamlit's webcam widget instead of OpenCV
import streamlit as st

st.set_page_config(page_title="Virtual Keyboard", layout="wide")
st.title("Interactive Virtual Keyboard")

# Streamlit webcam input
frame = st.camera_input("Take a picture")

if frame:
    # Convert the Streamlit image to an OpenCV format
    img = frame.to_image()
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
