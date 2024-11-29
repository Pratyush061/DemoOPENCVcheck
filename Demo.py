import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# Define a video transformer class to process the video frames
class VideoProcessor(VideoTransformerBase):
    def transform(self, frame):
        # Perform frame processing here if needed (e.g., object detection, etc.)
        return frame

# Add a title to the app
st.title("WebRTC Streamlit Example")

# Use webrtc_streamer with the custom video processor
webrtc_streamer(
    key="sample",
    video_processor_factory=VideoProcessor,  # Assign the video processor
    media_stream_constraints={"video": True, "audio": False},  # Enable video, disable audio
)
