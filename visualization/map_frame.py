from config import *
import pandas as pd
import tqdm

timestamps_df = pd.read_csv(data_dir + "/screen_recording/frames.csv")
timestamps_df = timestamps_df.rename(columns={'timestamp': 'Timestamp'})
ide_tracking_df = pd.read_csv(data_dir + "/csv/ide_tracking.csv")
eye_tracking_df = pd.read_csv(data_dir + "/csv/eye_tracking.csv")

mapped_df = pd.DataFrame(columns=['timestamp', 'id', 'path', 'x', 'y', 'line', 'col', 'type', 'token', 'remark'])
mapped_df['timestamp'] = timestamps_df['Timestamp']

for i in tqdm.tqdm(range(len(mapped_df))):
    timestamp = mapped_df['timestamp'][i]
    eye_tracking_row = eye_tracking_df[eye_tracking_df['timestamp'] <= timestamp].iloc[-1] if (
            len(eye_tracking_df[eye_tracking_df['timestamp'] <= timestamp]) != 0) else None
    if eye_tracking_row is not None and timestamp - eye_tracking_row['timestamp'] < 100:
        mapped_df['path'][i] = eye_tracking_row['path']
        # mapped_df['x'][i] = (eye_tracking_row['left_gaze_point_x'] + eye_tracking_row['right_gaze_point_x']) / 2
        # Make x/y ratio of the screen here. Choose left x (my dominant eye) and average y
        mapped_df['x'][i] = eye_tracking_row['left_gaze_point_x']
        mapped_df['y'][i] = (eye_tracking_row['left_gaze_point_y'] + eye_tracking_row['right_gaze_point_y']) / 2
        mapped_df['line'][i] = eye_tracking_row['line']
        mapped_df['col'][i] = eye_tracking_row['column']
        mapped_df['type'][i] = str(eye_tracking_row['type']).lower()
        mapped_df['token'][i] = eye_tracking_row['token'] if eye_tracking_row['type'] != 'WHITE_SPACE' else ''
        mapped_df['remark'][i] = eye_tracking_row['remark'] if eye_tracking_row['remark'] == '-' else (
            eye_tracking_row['remark'][7:])

ide_tracking_df['id'] = ide_tracking_df['id'].astype(str)
first_level = ide_tracking_df[((ide_tracking_df['element'] == 'action')
                               & (~ide_tracking_df['id'].str.startswith('Editor')))
                              | (ide_tracking_df['element'] == 'file')]
second_level = ide_tracking_df[(ide_tracking_df['id'].str.startswith('Editor'))
                               | (ide_tracking_df['element'] == 'typing')
                               | (ide_tracking_df['id'] == 'mousePressed')
                               | (ide_tracking_df['id'] == 'mouseReleased')]
second_level.loc[second_level['element'] == 'typing', 'id'] = 'Typing ' + second_level['info'].astype(str)
third_level = ide_tracking_df[(ide_tracking_df['id'] == 'mouseDragged') |
                              (ide_tracking_df['id'] == 'mouseMoved')]

for i in tqdm.tqdm(range(len(mapped_df))):
    timestamp = mapped_df['timestamp'][i]
    first_level_row = first_level[first_level['timestamp'] <= timestamp].iloc[-1] if (
            len(first_level[first_level['timestamp'] <= timestamp]) != 0) else None
    second_level_row = second_level[second_level['timestamp'] <= timestamp].iloc[-1] if (
            len(second_level[second_level['timestamp'] <= timestamp]) != 0) else None
    third_level_row = third_level[third_level['timestamp'] <= timestamp].iloc[-1] if (
            len(third_level[third_level['timestamp'] <= timestamp]) != 0) else None
    if first_level_row is not None and timestamp - first_level_row['timestamp'] < 2000:
        mapped_df['id'][i] = first_level_row['id']
    if second_level_row is not None and timestamp - second_level_row['timestamp'] < 500:
        mapped_df['id'][i] = second_level_row['id']
    if third_level_row is not None and timestamp - third_level_row['timestamp'] < 100:
        mapped_df['id'][i] = third_level_row['id']

mapped_df.to_csv(data_dir + "/csv/mapped.csv", index=False)

print(mapped_df.isna().sum())