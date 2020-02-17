# import numpy as np
# import cv2
# #from iomanager.py import get_videos
#
# cap = cv2.VideoCapture('mouse.mpg') # WORKS
# #cap = cv2.VideoCapture("Desktop\20080321162447.mpg")
# #cap = get_videos(multiple)
#
#
# while(cap.isOpened()):
#     ret, frame = cap.read()
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "yolo-tiny.h5"))
detector.loadModel()

video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "mouse.mpg"),
                                output_file_path=os.path.join(execution_path, "mousetracked")
                                , frames_per_second=20, log_progress=True)
print(video_path)
