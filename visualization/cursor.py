import ctypes, win32gui, win32ui
from PIL import Image, ImageGrab


# hand: 65567
# I: 65541
# triangle: 65535
# bi-arrow: 65553, 65555


def get_cursor():
    hcursor = win32gui.GetCursorInfo()[1]
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 36, 36)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), hcursor)

    bmpinfo = hbmp.GetInfo()
    bmpstr = hbmp.GetBitmapBits(True)
    cursor = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1).convert(
        "RGBA")

    pixdata = cursor.load()
    width, height = cursor.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (0, 0, 0, 0)
            if hcursor == 65541 and pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (0, 0, 0, 255)
    return cursor


if __name__ == '__main__':
    cursor, (hotspotx, hotspoty) = get_cursor()

    ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

    img = ImageGrab.grab(bbox=None, include_layered_windows=True)

    pos_win = win32gui.GetCursorPos()
    pos = (round(pos_win[0] * ratio - hotspotx), round(pos_win[1] * ratio - hotspoty))

    img.paste(cursor, pos, cursor)
