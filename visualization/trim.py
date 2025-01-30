import os
import cv2
import pandas as pd
import tqdm
from config import *
from guess import start_frame, end_frame, start_timestamp, end_timestamp

out_dir = data_dir + "/trimmed"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# trim timestamps
timestamps_raw = pd.read_csv(data_dir + "/raw/timestamps.csv")
timestamps_trimmed = timestamps_raw[(timestamps_raw.Timestamp >= start_timestamp)
                                    & (timestamps_raw.Timestamp <= end_timestamp)]
timestamps_trimmed.to_csv(out_dir + "/timestamps.csv", index=False)

# trim screen record
cap = cv2.VideoCapture(data_dir + "/raw/screen_record.mp4")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
screen_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(out_dir + "/screen_record.mp4", fourcc, fps, screen_size)
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
for frame_num in tqdm.tqdm(range(start_frame, min(end_frame, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))):
    ret, frame = cap.read()
    if ret:
        out.write(frame)
out.release()
