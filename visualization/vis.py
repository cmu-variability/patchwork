from config import *
import cv2
import tqdm
import os
import pandas as pd
import numpy as np

out_dir = data_dir + "/final"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

mapped_df = pd.read_csv(data_dir + "/csv/mapped.csv")

cap = cv2.VideoCapture(data_dir + "/screen_recording/clip_1.mp4")
fourcc = cv2.VideoWriter_fourcc(*'H264')
fps = cap.get(cv2.CAP_PROP_FPS)
screen_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(out_dir + "/screen_record.mp4", fourcc, fps, screen_size)

for frame_num in tqdm.tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
    ret, frame = cap.read()
    data = mapped_df.iloc[frame_num]
    if ret:
        cv2.rectangle(frame, (int(screen_size[0] * 0.7), 0),
                      (screen_size[0], 50 * 8), (255, 255, 255), cv2.FILLED)
        cv2.rectangle(frame, (int(screen_size[0] * 0.7), 0),
                      (screen_size[0], 50 * 8), (0, 0, 0), thickness=1,
                      lineType=cv2.LINE_AA)
        cv2.putText(frame, text=f"[Timestamp] {data['timestamp']}",
                    org=(int(screen_size[0] * 0.71), 5 + 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    thickness=2, color=[0, 0, 0])
        cv2.putText(frame,
                    text=f"[Path] {data['path'] if str(data['path']) != 'nan' and str(data['path']) != '-' else ''}",
                    org=(int(screen_size[0] * 0.71), 5 + 50 * 2), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, thickness=2, color=[0, 0, 0])
        cv2.putText(frame, text=f"[IDE Tracking] {data['id'] if str(data['id']) != 'nan' else ''}",
                    org=(int(screen_size[0] * 0.71), 5 + 50 * 3), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, thickness=2, color=[0, 0, 0])
        if data['remark'] == '-' or str(data['remark']) == 'nan':
            cv2.putText(frame, text=f"[Eye Tracking] Line: {data['line'] if str(data['type']) != 'nan' else ''} "
                                    f"Col: {data['col'] if str(data['type']) != 'nan' else ''}",
                        org=(int(screen_size[0] * 0.71), 5 + 50 * 4), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, thickness=2, color=[0, 0, 0])
            cv2.putText(frame, text=f"    Type: {data['type'] if str(data['type']) != 'nan' else ''}",
                        org=(int(screen_size[0] * 0.71), 5 + 50 * 5), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, thickness=2, color=[0, 0, 0])
            cv2.putText(frame, text=f"    Token: {data['token'] if str(data['token']) != 'nan' else ''}",
                        org=(int(screen_size[0] * 0.71), 5 + 50 * 6), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, thickness=2, color=[0, 0, 0])
        else:
            cv2.putText(frame, text=f"[Eye Tracking] {data['remark']}",
                        org=(int(screen_size[0] * 0.71), 5 + 50 * 4), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, thickness=2, color=[0, 0, 0])
        if not np.isnan(data['x']) and not np.isnan(data['y']):
            cv2.circle(frame, center=(int(data['x'] * screen_size[0]), int(data['y'] * screen_size[1])),
                    radius=10, color=[0, 0, 255], thickness=5, lineType=8, shift=0)
        elif str(data['remark']) == 'nan':
            cv2.putText(frame, text="TRACKING PAUSED",
                        org=(int(screen_size[0] * 0.77), 5 + 50 * 7), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, thickness=2, color=[0, 0, 255])

        out.write(frame)
        # store frame
        # cv2.imwrite(out_dir + "/frame%d.jpg" % frame_num, frame)
        # if frame_num > 100:
        #     break

out.release()
