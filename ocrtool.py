import os
import random
from time import sleep
from tkinter import messagebox
import requests
import base64
from requests.exceptions import ProxyError
from parameters import BAIDU_API_KEY, BAIDU_SECRET_KEY, ADB_PATH, SCREENSHOT_DELAY


class OcrTool:
    def __init__(self, device_name):
        self.token = None
        self.device_name = device_name
        self.screenshot_name = '%s_screenshot.png' % device_name
        if not os.path.exists('screenshot'):
            os.mkdir('screenshot')

        request_token_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
                             '&client_id=%s&client_secret=%s' % (BAIDU_API_KEY, BAIDU_SECRET_KEY)

        try:
            response = requests.get(request_token_host).json()
            if response is None:
                messagebox.showerror('初始化百度ocr失败', '代码异常，请求获得的响应为 None')
                exit(1)
            elif response.get('error') is not None:
                messagebox.showerror('初始化百度ocr失败', '请填写正确的API_KEY和SECRET_KEY')
                exit(1)
            elif response.get('access_token') is None:
                messagebox.showerror('初始化百度ocr失败', '请求获得的响应里没有token')
                exit(1)
            self.token = response['access_token']
        except ProxyError as e:
            messagebox.showerror('初始化百度ocr失败', '请检查网络连结')
            print(e)
            exit(1)

    def screenshot(self):
        sleep(SCREENSHOT_DELAY)
        path = os.path.abspath('screenshot') + '\\' + self.screenshot_name
        os.system(ADB_PATH + 'adb -s ' + self.device_name + ' shell screencap /data/screen.png')
        os.system(ADB_PATH + 'adb -s ' + self.device_name + ' pull /data/screen.png %s' % path)

    def identify_word(self, target_word: str):
        self.screenshot()
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
        img = base64.b64encode(open('screenshot/' + self.screenshot_name, 'rb').read())

        params = {"image": img}
        access_token = self.token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers).json()

        words_list = list()
        words_location_list = list()
        exists = False
        target_coordinate = None
        if response['error_code'] == 18:
            sleep(random.uniform(1.5, 3))
            return self.identify_word(target_word)

        for res in response['words_result']:
            word: str = res['words']
            location = res['location']
            coordinate = [location['left'] + location['width'] / 2, location['top'] + location['height'] / 2]

            if exists is False and word.find(target_word) != -1:
                exists = True
                target_coordinate = coordinate

            words_list.append(word)
            words_location_list.append(coordinate)

        return {'exists': exists,
                'coordinate': target_coordinate,
                'words': words_list,
                'words_location': words_location_list}
