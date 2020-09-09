import math
from time import sleep
import device
from device import Device
from parameters import LOADING_TIME, LOGIN_PARAMETERS, BOSS, IS_NEW_DEV_LOGIN

fail = 'Fail'
success = 'Success'


def login(dev: Device, account: list, login_parameters: int = LOGIN_PARAMETERS):
    dev.click(893, 37, click_round=4)  # touch屏幕后,点击切换账号按钮
    if not dev.cv_exists('et_id'):
        dev.long_press(360, 205, duration=1500)
        dev.key_event(device.KEYCODE_FORWARD_DEL)
        dev.long_press(360, 250, duration=1500)
        dev.key_event(device.KEYCODE_FORWARD_DEL)
    dev.click_and_input_byCv('et_id', account[0])
    dev.click_and_input_byCv('et_password', account[1])
    dev.click_byCv('btn_login')

    _sleep(is_open=True)  # 等待登录读条
    while True:
        if dev.cv_exists('iv_data_load'):
            _sleep(is_open=True)
        else:
            break
    if dev.cv_exists('btn_register'):
        dev.log.warning('错误[000]登录失败 账号：%s' % account[0])
        return fail

    if dev.cv_exists('iv_data_download'):
        dev.click_byCv('btn_ok_blue')
        while True:
            if not dev.ocr_exists('数据下载'):
                break
            _sleep(time=15, is_open=True)

    _sleep(is_open=True)
    if dev.cv_exists('btn_close'):
        dev.click_byCv('btn_close')
    else:
        if login_parameters == 0:
            dev.click_byCv('ib_skip', no_result_click_screen=True)  # 跳过每日盖章
        elif login_parameters == 1:
            pass
            # dev.click_byCv('iv_four_red_flag', 'btn_game_start', 'ib_skip') # 待换图源

    _sleep(is_open=True)
    # dev.click_byCv('btn_close')

    while True:
        if not dev.cv_exists('tb_adventure'):
            dev.click_screen_upper_left_corner(1, is_open=True)
            continue
        _sleep(time=3, is_open=True)
        if not dev.cv_exists('tb_main_menu'):
            dev.click_screen_upper_left_corner(1, is_open=True)
            continue
        else:
            break


def underground_city_battle_and_logout(dev: Device, account_list: list, is_complete_daily: bool, buy_energy_round: int):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        if is_complete_daily:
            complete_daily(dev, account, buy_energy_round)
        dev.click_byCv('tb_adventure')
        _sleep()  # 防止解锁团队战动画卡掉后续点击
        dev.click_byCv('iv_underground_city')
        _sleep()  # 等待解锁地下城
        dev.click_screen_upper_left_corner(6, click_delay=0.5)  # 跳过对话

        if dev.cv_exists('tv_first_floor'):
            pass
        else:
            dev.click_byCv('iv_cloudy_Mountains')
            if not dev.cv_exists('btn_ok_blue'):
                logout(dev)
                continue
            dev.click_byCv('btn_ok_blue')
            _sleep(is_open=True)
            _sleep(time=10)  # 第一次进地下城有过场动画

        if IS_NEW_DEV_LOGIN and dev.cv_exists('ib_menu'):
            dev.click_byCv('ib_menu', 'ib_menu_skip', 'btn_skip')
        dev.click_byCv('tv_first_floor', 'btn_underground_city_challenge', 'btn_aid')
        if not dev.cv_exists('btn_aid_on'):
            dev.log.warning('行会内没有支援')
            exit()
        # select_role(dev, 'iv_aid')
        select_combat_highest_role(dev)
        if dev.cv_exists('iv_team_null'):
            select_combat_highest_role(dev)
        dev.click_byCv('btn_battle_begins', 'btn_ok_blue', 'btn_menu_small', 'btn_give_up_white', 'btn_give_up_blue',
                       'btn_retreat', 'btn_ok_blue')  # 开始战斗后马上退出战斗，然后退出当前地下城

        dev.click_byCv('iv_cloudy_Mountains')
        if dev.cv_exists('btn_ok_blue'):
            dev.click_byCv('btn_ok_blue', 'tv_first_floor', 'btn_underground_city_challenge', 'btn_aid')
            select_combat_highest_role(dev)
            if dev.cv_exists('iv_team_null'):
                select_combat_highest_role(dev)
            dev.click_byCv('btn_battle_begins', 'btn_ok_blue', 'btn_menu_small', 'btn_give_up_white',
                           'btn_give_up_blue', 'btn_retreat', 'btn_ok_blue')
        logout(dev)


def select_combat_highest_role(dev: Device):
    if dev.cv_exists('btn_team_ascending'):
        dev.click_byCv('btn_team_ascending')
    if not dev.cv_exists('btn_team_combat_power'):
        dev.click_byCv('btn_team_classify_setting', 'tv_combat_power', 'btn_ok_blue')
    dev.click(105, 175)  # 选择位置在第一位的干员


def complete_daily(dev: Device, account: list, buy_energy_round: int = 0):
    dev.click_byCv('tb_twisted_egg')
    if IS_NEW_DEV_LOGIN:
        dev.click_byCv('btn_set_blue')
    dev.click_byCv('btn_ordinary', 'iv_10_free', 'btn_ok_blue', 'btn_ok_white', no_result_click_screen=True)
    if IS_NEW_DEV_LOGIN:
        dev.click_byCv('btn_set_blue')
    dev.click_byCv('tb_home_page')

    dev.click_byCv('btn_add_tiny')
    dev.click_byCv('btn_Buy_for_10_mana', no_result_click_screen=True)
    dev.click_byCv('btn_ok_blue')
    dev.click_screen_upper_left_corner(3, is_open=True)  # 退出购买mana小窗口

    for _ in range(buy_energy_round):  # 碎钻买体力
        dev.click_byCv('iv_home_add_energy', no_result_click_screen=True)
        dev.click_byCv('btn_ok_blue', 'btn_ok_white')
    dev.click_byCv('tb_adventure', no_result_click_screen=True)
    _sleep()
    if not dev.cv_exists('iv_main_adventure'):
        dev.reset_priconne()
        login(dev, account)
        dev.click_byCv('tb_adventure')
    dev.click_byCv('iv_main_adventure')
    adventure_1_1(dev, is_hard=True)
    adventure_1_1(dev)

    dev.click_byCv('tb_home_page', 'iv_task_button', 'btn_task_charge')
    dev.click_screen_upper_left_corner(5, is_open=True)  # 跳过可能出现的升级窗口
    dev.click_byCv('tb_home_page', no_result_click_screen=True)
    dev.click_byCv('iv_gift_button', 'btn_gift_charge', 'btn_ok_blue')
    dev.click_screen_upper_left_corner(5, is_open=True)  # 退出礼物小窗口


def adventure_1_1(dev: Device, is_hard: bool = False):
    if is_hard:
        dev.click_byCv('btn_hard')
    else:
        dev.click_byCv('btn_normal')

    for _ in range(20):
        if dev.ocr_exists('朱诺'):
            if is_hard:
                dev.click(245, 330)
                dev.click_byCv('ib_add_sweeping', click_round=2)
            else:
                dev.click(105, 275)
                _sleep(time=3, is_open=True)
                dev.long_press_byCv('ib_add_sweeping', duration=15000)
            dev.click(750, 330)
            dev.click_byCv('btn_ok_blue', 'btn_skip')
            dev.click_screen_upper_left_corner(5, is_open=True)  # 退出关卡详情小窗口，点5次跳过可能的升级窗口
            break
        else:
            dev.click(35, 270)  # 返回上一地区
            continue


def boss_go_to_second_farm(dev: Device, leader: list, target_farm: str):
    fire_role(dev, leader)
    boss_join_guild_and_set_aid(dev, target_farm)


def boss_join_guild_and_set_aid(dev: Device, guild_name: str, boss: list = BOSS):
    login(dev, boss)
    if join_guild(dev, guild_name) is fail:
        dev.log.warning('大号已加入行会')
        return fail
    dev.click_byCv('btn_aid_set')
    dev.click_byCv('iv_add_aid_city', select_upper_left=True)
    # select_role(dev, 'iv_aid')  # 大号上架支援
    select_combat_highest_role(dev)
    dev.click_byCv('btn_set_blue_small', 'btn_ok_blue')
    logout(dev)


def join_guild(dev: Device, guild_name: str):
    dev.click_byCv('iv_guild_button')
    dev.click_screen_upper_left_corner(3)  # 点掉对话
    if dev.cv_exists('btn_member_info'):
        logout(dev)  # 如果已经加入行会，退出这个账号
        return fail
    dev.click_byCv('btn_set_white_tiny', no_result_click_screen=True)
    dev.click_and_input_byCv('et_guild_name', guild_name)
    dev.click_byCv('tv_yes', 'btn_search')
    _sleep(is_open=True)  # 搜索需要一点时间
    dev.click_byCv('iv_choose_guild', select_upper_left=True)
    dev.click_byCv('btn_join', 'btn_ok_blue', 'btn_ok_blue')
    _sleep()  # 防止解锁团队战动画卡掉后续点击


def fire_role(dev: Device, leader: list):
    login(dev, leader)
    dev.click_byCv('iv_guild_button')
    _sleep()  # 防止解锁团队战动画卡掉后续点击
    dev.click_byCv('btn_member_info')
    if not dev.cv_exists('btn_guild_combat_power'):
        dev.click_byCv('btn_guild_classify_setting', 'tv_all_combat_power', 'btn_ok_blue')
    dev.click_byCv('btn_guild_ascending', identify_round=1)  # 如果排序是升序，点一下让它变成降序
    dev.click_byCv('btn_member_manage', select_upper_left=True)
    dev.click_byCv('btn_fire', 'btn_ok_blue', 'btn_ok_white')  # 踢出战力最高的玩家
    logout(dev)


def complete_daily_task(dev: Device, account_list: list, buy_energy_round: int = 0):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        complete_daily(dev, account, buy_energy_round)
        logout(dev)


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


def adventure_1_1_hard_3_stars(dev: Device, account_list: list, is_buy_energy: bool):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        if is_buy_energy:
            dev.click_byCv('iv_home_add_energy', 'btn_ok_blue', 'btn_ok_white')  # 买体力
        dev.click_byCv('tb_adventure')
        _sleep()
        dev.click_byCv('iv_main_adventure', 'btn_hard')

        for _ in range(20):
            if dev.ocr_exists('朱诺'):
                # dev.click_byOcr('1-1', is_full_matching=True, is_accurate=True)
                dev.click(245, 330)
                _sleep(time=3, is_open=True)
                dev.click_byCv('btn_adventure_challenge', 'btn_battle_begins', 'ib_battle_auto', 'ib_battle_speed_up')
                dev.click_byCv('btn_next_step', identify_round=300, no_result_click_screen=True)
                dev.click_byCv('btn_next_step_small')
                dev.click_screen_upper_left_corner(5, is_open=True)  # 退出关卡详情小窗口，点5次跳过可能的升级窗口
                break
            else:
                dev.click(35, 270)  # 返回上一地区
                continue
        logout(dev)


def join_guild_and_logout(dev: Device, account_list: list, guild_name: str):
    for account in account_list:
        if login(dev, account) is fail:
            continue
        if join_guild(dev, guild_name) is fail:
            dev.log.warning('错误[000]加入行会失败，该账号已加入行会 账号：%s' % account[0])
            continue
        logout(dev)


def create_guild(dev: Device, leader: list, guild_name: str):
    login(dev, leader)
    dev.click_byCv('iv_guild_button')
    dev.click_screen_upper_left_corner(3)  # 点掉对话
    dev.click_byCv('btn_create_guild', no_result_click_screen=True)  # =True跳过对话
    dev.click_and_input_byCv('et_guild_name', guild_name)
    dev.click_byCv('tv_yes', 'btn_create', 'btn_ok_blue')
    logout(dev)


def logout(dev: Device):
    dev.reset_priconne()


# def select_role(dev: Device, role_img: str):
#     for _ in range(15):
#         coordinate = dev.cv_get_coordinate(role_img, fun_info='select_role')
#         if coordinate is None:
#             dev.swipe(900, 335, 900, 120, duration=4000)  # 下拉一页
#             continue
#         dev.click(coordinate[0], coordinate[1])
#         break

def _sleep(time: float = LOADING_TIME, is_open: bool = IS_NEW_DEV_LOGIN):
    if is_open:
        sleep(time)
