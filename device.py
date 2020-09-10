import os
import sys
from time import sleep
from cv2tool import Cv2Tool
from log import LogTool
from ocrtool import OcrTool
from parameters import OPDELAY, IDENTIFY_ROUND, IS_NEW_DEV_LOGIN, ADB_PATH

KEYCODE_FORWARD_DEL = 112
device_list = []


def connect_ADB():
    try:
        os.system(ADB_PATH + 'adb connect 127.0.0.1:5554')
    except Exception as e:
        print(e)


def quit_ADB():
    os.system(ADB_PATH + 'adb kill-server')


def init_device_list(log_tool: LogTool):
    name_list = os.popen(ADB_PATH + 'adb devices').read().splitlines()[1:-1]
    for i in range(0, len(name_list)):
        device_name = name_list[i].split('\t')[0]
        device_list.append(Device(device_name, log_tool.get_logging(device_name)))


def get_device_list():
    return device_list


def start_priconne():
    for dev in device_list:
        dev.reset_priconne(start_delay=0, end_sleep=0)
    sleep(4)


class DeviceADB:
    @staticmethod
    def click(device_name: str, x: float, y: float):
        os.system(ADB_PATH + 'adb -s ' + device_name + ' shell input tap %s %s' % (x, y))

    @staticmethod
    def input(device_name: str, text: str):
        os.system(ADB_PATH + 'adb -s ' + device_name + ' shell input text "' + text + '"')
        # 要使用ADBKeyboard支持中文输入，则使用下面这行代码
        # os.system('adb -s ' + device_name + ' shell am broadcast -a ADB_INPUT_TEXT --es msg "' + text + '"')

    @staticmethod
    def swipe(device_name: str, start_x: float, start_y: float, end_x: float, end_y: float, duration: float):
        os.system(ADB_PATH + 'adb -s ' + device_name + ' shell input swipe %s %s %s %s %s' % (
            start_x, start_y, end_x, end_y, duration))

    @staticmethod
    def key_event(device_name: str, keycode: int):
        os.system(ADB_PATH + 'adb -s ' + device_name + ' shell input keyevent %s' % keycode)


class Device(DeviceADB):
    def __init__(self, device_name: str, log):
        self.log = log
        self.cv = Cv2Tool(device_name)
        self.ocr = OcrTool(device_name)
        self.device_name = device_name

    def __str__(self):
        return self.device_name

    __repr__ = __str__

    def reset_priconne(self, start_delay: float = 2, end_sleep: float = 6):
        sleep(start_delay)
        os.system(ADB_PATH + 'adb -s ' + self.device_name +
                  ' shell am start -S -n  com.bilibili.priconne/com.bilibili.princonne.bili.MainActivity')
        self.log.warning(sys._getframe(1).f_code.co_name + ' reset priconne')
        sleep(end_sleep)

    def click(self, x: float, y: float, click_round: int = 1, click_delay: float = OPDELAY):
        for r in range(click_round):
            sleep(click_delay)
            self.log.info('click x=%s,y=%s,sleep=%s(s),round=%s' % (x, y, click_delay, r))
            DeviceADB.click(self.device_name, x, y)

    def input(self, text: str):
        self.log.info('input text:%s' % text)
        DeviceADB.input(self.device_name, text)

    def swipe(self, start_x: float, start_y: float, end_x: float, end_y: float, duration: float):
        self.log.info(
            'swipe start_x=%s,start_y=%s,end_x=%s,end_y=%s,duration=%s(ms)' % (
                start_x, start_y, end_x, end_y, duration))
        DeviceADB.swipe(self.device_name, start_x, start_y, end_x, end_y, duration)

    def key_event(self, keycode):
        self.log.info('input keyevent:%s' % keycode)
        DeviceADB.key_event(self.device_name, keycode)

    def long_press(self, x: float, y: float, duration: float):
        DeviceADB.swipe(self.device_name, x, y, x, y, duration)

    def click_byCv(self, *image: str, identify_round: int = IDENTIFY_ROUND, click_round: int = 1,
                   click_delay: float = OPDELAY, no_result_click_screen: bool = False,
                   select_upper_left: bool = False):
        for img in image:
            for _ in range(identify_round):
                coordinate = self.cv_get_coordinate(img, fun_info=sys._getframe(1).f_code.co_name + ' '
                                                                  + sys._getframe(0).f_code.co_name,
                                                    select_upper_left=select_upper_left)
                if coordinate is not None:
                    self.click(coordinate[0], coordinate[1], click_round=click_round, click_delay=click_delay)
                    break
                if no_result_click_screen:
                    # 没匹配到素材坐标的情况，会点击一下左上角，按需使用
                    self.click_screen_upper_left_corner(1, is_open=True, click_delay=0.5)

    def click_and_input_byCv(self, image: str, text: str):
        self.click_byCv(image)
        self.input(text)

    def long_press_byCv(self, image: str, duration: float, identify_round: int = IDENTIFY_ROUND,
                        select_upper_left: bool = False):
        for _ in range(identify_round):
            coordinate = self.cv_get_coordinate(image, fun_info=sys._getframe(1).f_code.co_name + ' '
                                                                + sys._getframe(0).f_code.co_name,
                                                select_upper_left=select_upper_left)
            if coordinate is not None:
                self.long_press(coordinate[0], coordinate[1], duration)
                break

    def click_screen_upper_left_corner(self, click_round: int, click_delay: float = OPDELAY,
                                       is_open: bool = IS_NEW_DEV_LOGIN):
        # 点击左上角位置，用来跳过对话和动画页面
        if is_open:
            self.click(1, 1, click_round=click_round, click_delay=click_delay)

    def cv_get_coordinate(self, image: str, fun_info: str = None, select_upper_left: bool = False):
        if fun_info is None:
            fun_info = sys._getframe(1).f_code.co_name + ' ' + sys._getframe(0).f_code.co_name

        result = self.cv.get_coordinate(image, select_upper_left)
        if result['exists']:
            self.log.info(fun_info + ' ' + str(result))
            return result['coordinate']
        self.log.warning(fun_info + ' ' + str(result))
        return None

    def click_byOcr(self, *words: str, identify_round: int = IDENTIFY_ROUND, click_round: int = 1,
                    click_delay: float = OPDELAY, no_result_click_screen: bool = False,
                    is_full_matching: bool = False, is_accurate: bool = False):
        for word in words:
            fun_info = sys._getframe(1).f_code.co_name + ' ' + sys._getframe(0).f_code.co_name
            for _ in range(identify_round):
                result = self.ocr.word_matching(word, is_full_matching=is_full_matching, is_accurate=is_accurate)
                coordinate = result.get('coordinate')
                self.log.info(fun_info + ' ' + str(result))
                if coordinate is not None:
                    self.click(coordinate[0], coordinate[1], click_round=click_round, click_delay=click_delay)
                    break
                if no_result_click_screen:
                    # 没匹配到素材坐标的情况，会点击一下左上角，按需使用
                    self.click_screen_upper_left_corner(1, is_open=True, click_delay=0.5)

    def cv_exists(self, image: str):
        fun_info = sys._getframe(1).f_code.co_name + ' ' + sys._getframe(0).f_code.co_name
        result = self.cv.get_coordinate(image, select_upper_left=False)
        self.log.info(fun_info + ' ' + str(result))
        return result['exists']

    def ocr_exists(self, word, is_full_matching: bool = False, is_accurate: bool = False):
        fun_info = sys._getframe(1).f_code.co_name + ' ' + sys._getframe(0).f_code.co_name
        if is_accurate:
            result = self.ocr.word_exists_accurate(word, is_full_matching)
        else:
            result = self.ocr.word_matching(word, is_full_matching)
        self.log.info(fun_info + ' ' + str(result))
        return result['exists']
