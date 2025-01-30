from config import *
import pandas as pd
import xml.etree.ElementTree as ET

eye_tracking_xml = ET.parse(data_dir + "/xml/eye_tracking.xml")
eye_tracking_df = pd.DataFrame(columns=['timestamp', 'left_gaze_point_x', 'left_gaze_point_y',
                                        'right_gaze_point_x', 'right_gaze_point_y',
                                        'left_pupil_diameter', 'right_pupil_diameter',
                                        'path', 'line', 'column', 'token', 'type', 'remark'])
root = eye_tracking_xml.getroot()

for gaze in root.findall("gazes/"):
    new_row = pd.DataFrame([{'timestamp': gaze.attrib['timestamp'],
         'left_gaze_point_x': gaze.find('left_eye').attrib['gaze_point_x'],
         'left_gaze_point_y': gaze.find('left_eye').attrib['gaze_point_y'],
         'right_gaze_point_x': gaze.find('right_eye').attrib['gaze_point_x'],
         'right_gaze_point_y': gaze.find('right_eye').attrib['gaze_point_y'],
         'left_pupil_diameter': gaze.find('left_eye').attrib['pupil_diameter'],
         'right_pupil_diameter': gaze.find('right_eye').attrib['pupil_diameter'],
         'path': gaze.find('location').attrib['path'] if gaze.find('location') is not None else '-',
         'line': gaze.find('location').attrib['line'] if gaze.find('location') is not None else '-',
         'column': gaze.find('location').attrib['column'] if gaze.find('location') is not None else '-',
         'token': (gaze.find('ast_structure').attrib['token'])[:10] if gaze.find('ast_structure') is not None else '-',
         'type': gaze.find('ast_structure').attrib['type'] if gaze.find('ast_structure') is not None else '-',
         'remark': gaze.attrib['remark'] if 'remark' in gaze.attrib.keys() else '-'}])
    eye_tracking_df = pd.concat([eye_tracking_df, new_row], ignore_index=True)

eye_tracking_df = eye_tracking_df.sort_values(by=['timestamp'])
eye_tracking_df.to_csv(data_dir + "/csv/eye_tracking.csv", index=False)
