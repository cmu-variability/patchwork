import pyautogui
import time
import csv
import cv2
import os
import numpy as np
import keyboard
from screeninfo import get_monitors
from cursor import get_cursor
import ctypes, win32gui
from PIL import ImageGrab

out_dir = str(round(time.time() * 1000)) + "/raw"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with open(out_dir + '/timestamps.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Frame', 'Timestamp'])

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
screen_size = (get_monitors()[0].width, get_monitors()[0].height)
fps = 30.0
out = cv2.VideoWriter(out_dir + "/screen_record.mp4", fourcc, fps, screen_size)

should_stop = False


def stop_recording(e):
    global should_stop
    should_stop = True


keyboard.on_press_key('q', stop_recording)

last_time = time.time()

while True:
    if time.time() - last_time > 1 / fps:
        last_time = time.time()
        timestamp = round(time.time() * 1000)
        # screenshot = pyautogui.screenshot()

        frame = ImageGrab.grab(bbox=None, include_layered_windows=True)
        cursor = get_cursor()
        pos = pyautogui.position()
        frame.paste(cursor, pos, cursor)

        frame = np.array(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

        with open(out_dir + '/timestamps.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([f'frame_{timestamp}', timestamp])

    if should_stop:
        break

out.release()
cv2.destroyAllWindows()
