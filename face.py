# Brian Emo
# =========
# by David Su http://usdivad.com/
# 
# This is the input program that extracts facial landmarks and
# sends them to Wekinator.
#
# Usage: python face.py
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
    font = cv2.FONT_HERSHEY_PLAIN
    num_frames = 0

    # Capture, analyze, and send OSC messages in a loop
    # until 'q' key is pressed
    while True:
        # Increment frame count
        num_frames += 1

        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Convert to grayscale
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get landmarks using PyStasm
        landmarks = stasm.search_single(img)
        if len(landmarks) == 0:
            print "No face found in frame #{}".format(num_frames)
            continue
        else:
            landmarks = stasm.force_points_into_image(landmarks, img)
            for i,point in enumerate(landmarks):
                # img[round(point[1])][round(point[0])] = 255
                cv2.putText(img, str(i), (int(round(point[0])), int(round(point[1]))), font, 1, 255)

        # print landmarks

        # Show it!
        cv2.imshow("", img)

        # Construct and send OSC message
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress('/wek/inputs')

        for landmark in landmarks:
            oscmsg.append(landmark[0]) # x-position
            oscmsg.append(landmark[1]) # y-position

        client.send(oscmsg)

        # Break if 'q' key pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()