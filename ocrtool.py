import os
import random
from time import sleep
from tkinter import messagebox
import requests
import base64
from requests.exceptions import ProxyError
from parameters import BAIDU_API_KEY, BAIDU_SECRET_KEY, ADB_PATH, OPDELAY


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
        sleep(OPDELAY)
        path = os.path.abspath('screenshot') + '\\' + self.screenshot_name
        os.system(ADB_PATH + 'adb -s ' + self.device_name + ' shell screencap /data/screen.png')
        os.system(ADB_PATH + 'adb -s ' + self.device_name + ' pull /data/screen.png %s' % path)

    def word_exists(self, target_word, is_full_matching: bool, is_accurate: bool = False,
                    re_screenshot: bool = True):
        if re_screenshot:
            self.screenshot()
        if is_accurate:
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        else:
            request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
        img = base64.b64encode(open('screenshot/' + self.screenshot_name, 'rb').read())

        params = {"image": img}
        request_url = request_url + "?access_token=" + self.token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(request_url, data=params, headers=headers)
            response_json = response.json()
        except Exception as e:
            return self.word_exists(target_word, is_full_matching, is_accurate, re_screenshot)

        words_list = list()
        exists = False
        if response_json.get('error_code') is not None:
            sleep(random.uniform(1.5, 3))
            return self.word_exists(target_word, is_full_matching)

        for res in response_json['words_result']:
            word: str = res['words']
            word_index = word.find(target_word)
            if (not exists) and word.find(target_word) != -1:
                if is_full_matching:
                    if word_index == 0:
                        exists = True
                else:
                    exists = True
            words_list.append(word)
        return {'exists': exists, 'words': words_list}

    def word_matching(self, target_word: str, is_full_matching: bool, is_accurate: bool = False,
                      re_screenshot: bool = True):
        if re_screenshot:
            self.screenshot()
        if is_accurate:
            request_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate'
        else:
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
        img = base64.b64encode(open('screenshot/' + self.screenshot_name, 'rb').read())

        params = {"image": img}
        request_url = request_url + "?access_token=" + self.token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(request_url, data=params, headers=headers)
            response_json = response.json()
        except Exception as e:
            return self.word_exists(target_word, is_full_matching, is_accurate, re_screenshot)

        words_list = list()
        words_location_list = list()
        exists = False
        target_coordinate = None
        if response_json.get('error_code') is not None:
            sleep(random.uniform(1.5, 3))
            return self.word_matching(target_word, is_full_matching, is_accurate)

        for res in response_json['words_result']:
            word: str = res['words']
            location = res['location']
            coordinate = [location['left'] + location['width'] / 2, location['top'] + location['height'] / 2]

            word_index = word.find(target_word)
            if (not exists) and word_index != -1:
                if is_full_matching:
                    if word_index == 0:
                        exists = True
                        target_coordinate = coordinate
                else:
                    exists = True
                    target_coordinate = coordinate

            words_list.append(word)
            words_location_list.append(coordinate)

        return {'exists': exists,
                'coordinate': target_coordinate,  # 匹配到多个目标取最靠左上位置的目标坐标
                'words': words_list,
                'words_location': words_location_list}
