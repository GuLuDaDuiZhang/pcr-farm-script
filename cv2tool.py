import os
import cv2
import numpy as np
from time import sleep
from parameters import IDENTIFY_THRESHOLD, SCREENSHOT_DELAY, SCREEN_RESOLUTION, ADB_PATH


class Cv2Tool:
    def __init__(self, device_name: str):
        self.device_name = device_name
        self.screenshot_name = '%s_screenshot.png' % device_name
        if not os.path.exists('screenshot'):
            os.mkdir('screenshot')

    def screenshot(self):
        sleep(SCREENSHOT_DELAY)
        path = os.path.abspath('screenshot') + '\\' + self.screenshot_name
        os.system(ADB_PATH + 'adb -s ' + self.device_name + ' shell screencap /data/screen.png')
        os.system(ADB_PATH + 'adb -s ' + self.device_name + ' pull /data/screen.png %s' % path)

    def get_img_size(self, img_path: str):
        img = cv2.imread(img_path, 0)
        screen = cv2.imread('screenshot/' + self.screenshot_name, 0)
        height, width = img.shape[:2]
        ratio = int(SCREEN_RESOLUTION) / screen.shape[1]
        size = (int(width / ratio), int(height / ratio))
        return cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    def get_coordinate(self, image: str, select_upper_left: bool) -> dict:
        self.screenshot()
        image_path = 'images/' + SCREEN_RESOLUTION + '/' + image + '.png'
        screen = cv2.imread('screenshot/' + self.screenshot_name, 0)
        template = self.get_img_size(image_path)
        image_x, image_y = template.shape[:2]
        data = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(data)
        if max_val < IDENTIFY_THRESHOLD:
            return {'image': image, 'max_val': max_val, 'min_val': min_val}

        if select_upper_left is False:
            coordinate = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
            return {'image': image, 'coordinate': coordinate, 'max_val': max_val, 'min_val': min_val}
        else:
            result = [list(coordinate) for coordinate in zip(*np.where(data > IDENTIFY_THRESHOLD)[::-1])]
            result_upper_left = min(result)
            coordinate = (result_upper_left[0] + image_y / 2, result_upper_left[1] + image_x / 2)
            return {'image': image, 'coordinate': coordinate, 'all_coordinate': result, 'max_val': max_val,
                    'min_val': min_val}
