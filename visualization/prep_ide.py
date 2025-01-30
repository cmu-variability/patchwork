import os
from config import *
import pandas as pd
import xml.etree.ElementTree as ET

if not os.path.exists(data_dir + "/csv"):
    os.makedirs(data_dir + "/csv")

ide_tracking_xml = ET.parse(data_dir + "/xml/ide_tracking.xml")
ide_tracking_df = pd.DataFrame(columns=['timestamp', 'id', 'element', 'info'])
root = ide_tracking_xml.getroot()

actions = []
for action in root.findall("actions/"):
    new_row = pd.DataFrame([{'timestamp': action.attrib['timestamp'], 'id': action.attrib['id'],
                                              'element': 'action', 'info': '-'}])
    ide_tracking_df = pd.concat([ide_tracking_df, new_row], ignore_index=True)

for typing in root.findall("typings/"):
    new_row = pd.DataFrame([{'timestamp': typing.attrib['timestamp'], 'id': '-', 'element': 'typing',
                                              'info': typing.attrib['character']}])
    ide_tracking_df = pd.concat([ide_tracking_df, new_row], ignore_index=True)

for file in root.findall("files/"):
    new_row = pd.DataFrame([{'timestamp': file.attrib['timestamp'], 'id': file.attrib['id'],
                                              'element': 'file', 'info': '-'}])
    ide_tracking_df = pd.concat([ide_tracking_df, new_row], ignore_index=True)

for mouse in root.findall("mouses/"):
    new_row = pd.DataFrame([{'timestamp': mouse.attrib['timestamp'], 'id': mouse.attrib['id'],
                                              'element': 'mouse', 'info': '-'}])
    ide_tracking_df = pd.concat([ide_tracking_df, new_row], ignore_index=True)

ide_tracking_df = ide_tracking_df[(ide_tracking_df.id != 'mouseClicked') &
                                  (ide_tracking_df.id != 'CodeVision.StartStopTrackingAction') &
                                  (ide_tracking_df.id != 'CodeVision.PauseResumeAction')]
ide_tracking_df = ide_tracking_df.sort_values(by=['timestamp'])

ide_tracking_df.to_csv(data_dir + "/csv/ide_tracking.csv", index=False)
