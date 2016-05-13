# Brian Emo
# =========
# by David Su http://usdivad.com/
# 
# Usage: python emo.py
# 
# :D :P :) :| :( :O
# 
# Adapted from EyeSpy https://github.com/usdivad/EyeSpy,
# (in turn adapted from https://github.com/shantnu/Webcam-Face-Detect by Shantnu Tiwari)
# as well as the PyStasm minimal example https://github.com/mjszczep/PyStasm/blob/master/doc/index.rst by Stephen Milborrow

import cv2
import OSC
import stasm

import math
import sys 

if __name__ == '__main__':
    # OSC client setup
    client = OSC.OSCClient()
    client.connect(('127.0.0.1', 6448))

    # Webcam capture using OpenCV
    video_capture = cv2.VideoCapture(0)
    num_frames = 0

    # Capture, analyze, and send OSC messages in a loop
    # until 'q' key is pressed
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Convert to grayscale
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get landmarks using PyStasm
        landmarks = stasm.search_single(img)
        if len(landmarks) == 0:
            print("No face found in frame #", num_frames)
        else:
            landmarks = stasm.force_points_into_image(landmarks, img)
            for point in landmarks:
                img[round(point[1])][round(point[0])] = 255

        # print landmarks

        # Show it!
        cv2.imshow("Brian Emo", img)

        # Increment frame count
        num_frames += 1

        # Break if 'q' key pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()