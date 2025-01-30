import cv2
import pandas as pd
from config import *

total_time = 10
start_time = 0.01
end_time = total_time - 0.01

cap = cv2.VideoCapture(data_dir + "/raw/screen_record.mp4")
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
start_frame = int(start_time / total_time * total_frames)
end_frame = int(end_time / total_time * total_frames)

timestamps = pd.read_csv(data_dir + "/raw/timestamps.csv")
start_timestamp = timestamps.iloc[start_frame, 1]
end_timestamp = timestamps.iloc[end_frame, 1]

if __name__ == '__main__':
    print("start timestamp: " + str(start_timestamp) + " frame: " + str(start_frame))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    ret, frame = cap.read()
    cv2.imshow("start frame", cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))))
    cv2.waitKey(0)

    print("end timestamp: " + str(end_timestamp) + " frame: " + str(end_frame))
    cap.set(cv2.CAP_PROP_POS_FRAMES, end_frame)
    ret, frame = cap.read()
    cv2.imshow("end frame", cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))))
    cv2.waitKey(0)
