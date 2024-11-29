import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, text, size=[100, 100]):
        self.pos = pos
        self.size = size
        self.text = text

def process_video_frame(frame, detector, segmentor, imgList, indexImg, keys, session_state):
    image = frame.to_ndarray(format="bgr24")
    imgOut = segmentor.removeBG(image, imgList[indexImg])

    hands, img = detector.findHands(imgOut, flipType=False)
    keyboard_canvas = np.zeros_like(img)
    buttonList = []

    for key in keys[0]:
        buttonList.append(Button([30 + keys[0].index(key) * 105, 30], key))
    for key in keys[1]:
        buttonList.append(Button([30 + keys[1].index(key) * 105, 150], key))
    for key in keys[2]:
        buttonList.append(Button([30 + keys[2].index(key) * 105, 260], key))

    for button in buttonList:
        x, y = button.pos
        cv2.rectangle(keyboard_canvas, (x, y), (x + button.size[0], y + button.size[1]), (255, 255, 255), -1)
        cv2.putText(keyboard_canvas, button.text, (x + 20, y + 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 3)

    # Handle input and gestures
    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            if lmList:
                x8, y8 = lmList[8][0], lmList[8][1]
                for button in buttonList:
                    bx, by = button.pos
                    bw, bh = button.size
                    if bx < x8 < bx + bw and by < y8 < by + bh:
                        cv2.rectangle(img, (bx, by), (bx + bw, by + bh), (0, 255, 0), -1)
                        cv2.putText(img, button.text, (bx + 20, by + 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 3)
                        session_state["output_text"] += button.text

    return frame.from_ndarray(img, format="bgr24")
