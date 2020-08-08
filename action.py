import math
from time import sleep
import device
from device import Device
from parameters import LOADING_TIME, LOGIN_PARAMETERS, BOSS, IS_NEW_DEV_LOGIN, BACK_TO_JUNO

fail = 'Fail'


def _sleep(time: float = LOADING_TIME, is_open: bool = IS_NEW_DEV_LOGIN):
    if is_open:
        sleep(time)


def login(dev: Device, account: list, login_parameters: int = LOGIN_PARAMETERS):
    dev.click(893, 37, click_round=4)  # 切换账号按钮浮动显示4s，识图的话会来不及，故使用绝对坐标定位。touch屏幕后,点击切换账号按钮
    if dev.cv_get_coordinate('et_id', fun_info='login') is None:
        dev.long_press(360, 205, duration=1500)
        dev.key_event(device.KEYCODE_FORWARD_DEL)  # 长按删除账号
        dev.long_press(360, 250, duration=1500)
        dev.key_event(device.KEYCODE_FORWARD_DEL)  # 长按删除密码
    dev.click_and_input_byCv('et_id', account[0])
    dev.click_and_input_byCv('et_password', account[1])
    dev.click_byCv('btn_login')

    _sleep(is_open=True)  # 等待登录读条
    if dev.cv_get_coordinate('iv_data_load', fun_info='login') is not None:
        _sleep(is_open=True, time=10)
    if dev.cv_get_coordinate('btn_register', fun_info='login') is not None:
        dev.log.warning('登录失败login Fail 账号：%s' % account)
        return fail

    if login_parameters == 0:
        dev.click_byCv('ib_skip', no_result_click_screen=True)  # 跳过每日盖章动画
    if login_parameters == 1:
        dev.click_byCv('iv_four_red_flag', 'btn_game_start', 'ib_skip')
        dev.click_screen_upper_left_corner(1, is_open=True)
    dev.click_byCv('btn_close', no_result_click_screen=True)  # 退出通知弹窗


def logout(dev: Device):
    dev.click_byCv('tb_main_menu', 'btn_back_title', 'btn_ok_blue')
    _sleep(time=2, is_open=True)  # 登出后等一下防止点击点在白屏上


def select_role(dev: Device, role_img: str):
    for _ in range(15):
        coordinate = dev.cv_get_coordinate(role_img, fun_info='select_role')
        if coordinate is None:
            dev.swipe(900, 335, 900, 120, duration=4000)  # 下拉一页
            continue
        dev.click(coordinate[0], coordinate[1])
        break


def join_guild(dev: Device, guild_name: str):
    dev.click_byCv('iv_guild_button')
    dev.click_screen_upper_left_corner(3)  # 点掉对话
    dev.click_byCv('btn_set_white_tiny', no_result_click_screen=True)
    dev.click_and_input_byCv('et_guild', guild_name)
    dev.click_byCv('tv_yes', 'btn_search')
    _sleep(is_open=True)  # 搜索需要一点时间
    dev.click_byCv('iv_choose_guild', select_upper_left=True)
    dev.click_byCv('btn_join', 'btn_ok_blue', 'btn_ok_blue')
    _sleep()  # 防止解锁团队战动画卡掉后续点击


def join_guild_and_logout(dev: Device, account_list: list, guild_name: str):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        join_guild(dev, guild_name)
        logout(dev)


def underground_city_battle_and_logout(dev: Device, account_list: list, is_complete_daily: bool,
                                       buy_energy_round: int):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        if is_complete_daily:
            complete_daily(dev, buy_energy_round)
        dev.click_byCv('tb_adventure')
        _sleep()  # 防止解锁团队战动画卡掉后续点击
        dev.click_byCv('iv_underground_city')
        _sleep()  # 等待解锁地下城
        dev.click_screen_upper_left_corner(6, click_delay=0.5)  # 跳过对话
        dev.click_byCv('iv_cloudy_Mountains', 'btn_ok_blue')  # 进入地下城云海的山脉进入第一层
        _sleep(time=10)  # 第一次进地下城有过场动画
        if IS_NEW_DEV_LOGIN and (dev.cv_get_coordinate('ib_menu',
                                                       fun_info='underground_city_battle_and_logout') is not None):
            dev.click_byCv('ib_menu', 'ib_menu_skip', 'btn_skip')
        dev.click_byCv('tv_first_floor', 'btn_challenge', 'btn_aid')
        select_role(dev, 'iv_aid')
        dev.click_byCv('btn_battle_begins', 'btn_ok_blue', 'btn_menu_small', 'btn_give_up_white', 'btn_give_up_blue',
                       'btn_retreat', 'btn_ok_blue')  # 开始战斗后马上退出战斗，然后退出当前地下城
        logout(dev)


def fire_role(dev: Device, leader: list):
    login(dev, leader, login_parameters=-1)
    dev.click_byCv('iv_guild_button')
    _sleep()  # 防止解锁团队战动画卡掉后续点击
    dev.click_byCv('btn_member_info', 'btn_classify_setting', 'tv_combat_power', 'btn_ok_blue')  # 按角色战力排序
    dev.click_byCv('btn_ascending', identify_round=1)  # 如果排序是升序，点一下让它变成降序
    dev.click_byCv('btn_member_manage', select_upper_left=True)
    dev.click_byCv('btn_fire', 'btn_ok_blue', 'btn_ok_white')  # 踢出战力最高的玩家
    logout(dev)


def boss_go_to_second_farm(dev: Device, leader: list, target_farm: str):
    fire_role(dev, leader)
    boss_join_guild_and_set_aid(dev, target_farm)


def boss_join_guild_and_set_aid(dev: Device, guild_name: str, boss: list = BOSS):
    login(dev, boss, login_parameters=-1)
    join_guild(dev, guild_name)
    dev.click_byCv('btn_aid_set')
    dev.click_byCv('iv_add_aid_city', select_upper_left=True)
    select_role(dev, 'iv_aid')  # 大号上架支援
    dev.click_byCv('btn_set_blue_small', 'btn_ok_blue')
    logout(dev)


def create_guild(dev: Device, leader: list, guild_name: str):
    login(dev, leader)
    dev.click_byCv('iv_guild_button')
    dev.click_screen_upper_left_corner(3)  # 点掉对话
    dev.click_byCv('btn_create_guild', no_result_click_screen=True)  # =True跳过对话
    dev.click_and_input_byCv('et_create_guild', guild_name)
    dev.click_byCv('tv_yes', 'btn_create', 'btn_ok_blue')
    _sleep()  # 防止解锁团队战动画卡掉后续点击
    logout(dev)


def adventure_1_1(dev: Device):
    dev.click_byCv('btn_normal')  # 选择正常难度
    dev.click(35, 270, BACK_TO_JUNO)  # 点击后退按钮，有多少个图点多少次
    dev.click(105, 270)  # 固定坐标点击1-1
    _sleep(is_open=True)  # 按压操作没有加延迟，这里需要补个等待时间
    dev.long_press(880, 330, 15000)  # 按压15s把扫荡卷拉满
    dev.click(750, 330)  # 点击使用扫荡卷
    dev.click_byCv('btn_ok_blue', 'btn_skip')
    dev.click_screen_upper_left_corner(5, is_open=True)  # 退出关卡详情小窗口，点5次跳过可能的升级窗口


def adventure_1_1_hard(dev: Device):
    dev.click_byCv('btn_hard')  # 选择困难难度
    dev.click(35, 270, BACK_TO_JUNO)  # 点击后退按钮，有多少个图点多少次
    dev.click(250, 335)  # 固定坐标点击1-1
    dev.click(880, 330, click_round=2)
    dev.click(750, 330)  # 点击使用扫荡卷
    dev.click_byCv('btn_ok_blue', 'btn_skip')
    dev.click_screen_upper_left_corner(5, is_open=True)  # 退出关卡详情小窗口，点5次跳过可能的升级窗口


def adventure_1_1_leve_up(dev: Device, account_list: list, buy_energy_round: int):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        round_chunks = math.ceil(buy_energy_round / 6)
        round_num = 6

        for r in range(round_chunks):
            if buy_energy_round <= 6:
                round_num = buy_energy_round
            elif (r == round_chunks - 1) and (buy_energy_round % 6 != 0):
                round_num = buy_energy_round % 6
            for _ in range(round_num):
                dev.click_byCv('iv_home_add_energy', 'btn_ok_blue', 'btn_ok_white')

            dev.click_byCv('tb_adventure')
            _sleep()
            dev.click_byCv('iv_main_adventure')
            adventure_1_1(dev)
            dev.click_byCv('tb_home_page')
        logout(dev)


def adventure_1_1_hard_3_stars(dev: Device, account_list: list):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        dev.click_byCv('iv_home_add_energy', 'btn_ok_blue', 'btn_ok_white')  # 买体力
        dev.click_byCv('tb_adventure')
        _sleep()
        dev.click_byCv('iv_main_adventure')
        dev.click_byCv('btn_hard')  # 选择困难难度
        dev.click(35, 270, BACK_TO_JUNO)  # 点击后退按钮
        dev.click(250, 335)  # 固定坐标点击1-1
        dev.click_byCv('btn_challenge', 'btn_battle_begins', 'ib_battle_auto', 'ib_battle_speed_up')
        _sleep(time=30, is_open=True)  # 战斗过图
        dev.click_screen_upper_left_corner(18, is_open=True)  # 对话
        _sleep(time=20, is_open=True)  # 战斗过图
        dev.click_screen_upper_left_corner(20, is_open=True)  # 对话
        dev.click_byCv('btn_next_step', 'btn_next_step_small')
        dev.click_screen_upper_left_corner(3, is_open=True)
        logout(dev)


def complete_daily(dev: Device, buy_energy_round: int = 0):
    dev.click_byCv('tb_twisted_egg')
    if IS_NEW_DEV_LOGIN:
        dev.click_byCv('btn_set_blue')
    dev.click_screen_upper_left_corner(2, is_open=True)  # 点掉可能出现的tp交换弹窗
    dev.click_byCv('btn_ordinary', 'iv_10_free', 'btn_ok_blue', 'btn_ok_white')
    if IS_NEW_DEV_LOGIN:
        dev.click_byCv('btn_set_blue')
    dev.click_byCv('tb_home_page')

    dev.click_byCv('btn_add_tiny')
    dev.click_byCv('btn_Buy_for_10_mana', no_result_click_screen=True)
    dev.click_byCv('btn_ok_blue')
    dev.click_screen_upper_left_corner(2, is_open=True)  # 退出购买mana小窗口

    for _ in range(buy_energy_round):  # 碎钻买体力
        dev.click_byCv('iv_home_add_energy', 'btn_ok_blue', 'btn_ok_white')
    dev.click_byCv('tb_adventure')
    _sleep()
    dev.click_byCv('iv_main_adventure')
    adventure_1_1_hard(dev)
    adventure_1_1(dev)

    dev.click_byCv('tb_home_page')
    dev.click_byCv('iv_task_button', 'btn_all_charge', 'btn_close', 'tb_home_page')
    dev.click_screen_upper_left_corner(2, is_open=True)  # 跳过可能出现的升级窗口
    dev.click_byCv('iv_gift_button', 'btn_all_charge', 'btn_ok_blue')
    dev.click_screen_upper_left_corner(3, is_open=True)  # 退出礼物小窗口
