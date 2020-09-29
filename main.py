import math
import sys
import time
import action
import device
import task
from log import LogTool
from parameters import BOSS, FARM_1_LEADER, FARM_2_LEADER, FARM_1_NAME, FARM_2_NAME, IS_NEW_DEV_LOGIN, LOGIN_PARAMETERS
from tkinter import messagebox, Tk
import ocrtool


def get_account(file: str) -> list:
    with open(file, 'r') as f:
        account_list = f.readlines()
    return [[str.strip(account.split(' ')[0]), str.strip(account.split(' ')[1])] for account in account_list]


def hint():
    account_quantity = len(account_list1)
    account_quantity2 = len(account_list2)
    init_info = '\n===============init_info===============' \
                '\n模拟器：数量%s  %s' % (len(device_list), str(device_list)) + \
                '\nIS_NEW_DEV_LOGIN=' + str(IS_NEW_DEV_LOGIN) + \
                '\nLOGIN_PARAMETERS=' + str(LOGIN_PARAMETERS) + \
                '\n大号：' + str(BOSS) + \
                '\n农场1会长：' + str(FARM_1_LEADER) + \
                '\n农场2会长：' + str(FARM_2_LEADER) + \
                '\n农场1：' + FARM_1_NAME + \
                '\n农场2：' + FARM_2_NAME + \
                '\naccountlist.txt内账号数量：' + str(account_quantity) + \
                '\naccountlist2.txt内账号数量：' + str(account_quantity2) + \
                '\n======================================='
    main_log.info(init_info)

    if len(device_list) == 0:
        messagebox.showinfo('错误', '模拟器数量为 0\n\n请重试')
        exit()

    if not messagebox.askokcancel("运行前检查", init_info + '\n如果有不符预期的内容请点[取消]终止运行，检查后重新运行'
                                                       '\n除了调试外，模拟器建议3个起步'):
        exit()

    if not messagebox.askokcancel("请注意",
                                  '*大号战力最高的干员的等级不能高出小号骑士君等级30以上（例如102级的干员，小号起码要72级才能借）'
                                  '\n\n*大号要处于未加入行会的状态'
                                  '\n\n*每日任务刷图用扫荡卷扫，要求已3星通关1-1普通和困难'
                                  '\n\n*农场小号不要上架支援'
                                  '\n\n*大号的全角色战力要是农场里最高的，切换农场默认踢掉全角色战力最高的玩家'
                                  '\n\n*大号战力最高的干员战力最好超过1万，防止地下城开头被秒导致流程卡死，而且mana收益=战力x5'
                                  '\n\n...'):
        exit()

    # check_time = 8
    # for i in range(0, check_time + 1):
    #     if i != check_time:
    #         print('\r脚本运行前倒计时:' + str(check_time - i), end=' ')
    #         time.sleep(1)
    #     else:
    #         print('\r开始执行设定任务...')


def check_log(file: str = None, info: str = None):
    # 用来找出刷mana任务中被标记登录失败的农场号、以及创建行会任务中没有成功加入行会的
    result = ''
    if file is None:
        file = log_tool.filename
    else:
        file = 'log\\' + file

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if line.find('错误[000]') != -1:
            print(line, end='')
            result += line

    if info is not None:
        result += info
    if result != '':
        messagebox.showinfo("请检查！", result)


if __name__ == '__main__':
    # -------------这些代码是脚本准备工作，不了解的情况下不要动---------------
    device.connect_ADB()
    start = time.time()
    Tk().withdraw()

    log_tool = LogTool()
    main_log = log_tool.get_logging('main_log')

    device.init_device_list(log_tool)
    device_list = device.get_device_list()
    account_list1 = get_account('accountlist.txt')
    account_list2 = get_account('accountlist2.txt')

    hint()  # 执行前检查账号
    device.start_priconne()  # 启动公主连结
    # ----------------------------------------------------------------

    # -----------创建农场行会
    # account_list1 代表accountlist.txt里的账号数据，account_list2 代表accountlist2.txt里的账号数据
    # *账号文件里第一行账号做为会长，会名有注意事项请看parameters.py
    # task.task_create_guild_and_join(device_list, account_list1, FARM_1_NAME)
    # task.task_create_guild_and_join(device_list, account_list2, FARM_2_NAME)

    # -----------账号批量通关1-1困难
    # is_buy_energy=True会买一管体力防止体力不够
    # *没做选人，打开编队默认配的是什么就用什么，干员等级太低可能会过不了
    # task.task_adventure_1_1_hard_3_stars(device_list, account_list1, is_buy_energy=True)
    # task.task_adventure_1_1_hard_3_stars(device_list, account_list2, is_buy_energy=True)

    # -----------40对1
    # 流程大号加入第一个农场上架支援，然后农场小号借支援轮巡完，踢出大号加第二个农场重复一遍
    # is_complete_dail完成每日任务用于升级，开启会增加约1倍的耗时
    # buy_energy_round买体次数，数值不能超过8，平时建议3~6用追等级，开了完成每日任务此项才会买体
    # *每日任务刷1-1是用扫荡卷扫的，要求已经3星通关普通和困难1-1
    # *农场行会内小号不要去上架支援，以免影响脚本对空支援的判断
    # *大号要求全角色战力是农场里最高的，切换农场会踢掉全角色战力最高的玩家
    # task.task_40_to_1(device_list, account_list1, account_list2, is_complete_daily=True, buy_energy_round=3)

    # -----------单农场刷mana完成每日
    # 流程大号加入第一个农场上架支援，然后农场小号借支援轮巡完，踢出大号
    # *注意事项参考40对1
    # *默认刷农场1，要刷农场2把函数参数account_list1, FARM_1_NAME, FARM_1_LEADER的1改成2
    # task.task_mana_and_daily(device_list, account_list1, FARM_1_NAME, FARM_1_LEADER, is_complete_daily=False,
    #                          buy_energy_round=3)

    # -----------扫荡普通1-1
    # buy_energy_round买体次数不能超过30
    # task.task_adventure_1_1_leve_up(device_list, account_list1, buy_energy_round=10)
    # task.task_adventure_1_1_leve_up(device_list, account_list2, buy_energy_round=10)

    # -----------刷每日
    # buy_energy_round买体次数，数值不能超过8，建议3~6
    # *每日任务刷1-1是用扫荡卷扫的，要求已经3星通关普通和困难1-1
    # task.task_complete_daily(device_list, account_list1, buy_energy_round=6)
    # task.task_complete_daily(device_list, account_list2, buy_energy_round=6)

    # 调试
    # d_l = device.get_device_list()
    # d_l[1].click_byCv('btn_aid_on')
    # d_l[0].click_and_input_byCv('et_guild', '233')
    # print(d_l[0].ocr_exists('朱诺'))
    # while True:
    #     if messagebox.askokcancel("截图", '点确定截一张图'):
    #         d_l[0].cv.screenshot()
    #     else:
    #         break
    # action.login(d_l[0], [])
    # task
    # check_log(file='')
    # result=d_l[0].ocr.identify_word('主菜单')
    # print(result)

    # -------------这些代码是脚本收尾工作，不了解的情况下不要动---------------
    device.quit_ADB()
    run_time = divmod(math.ceil(time.time() - start), 60)
    run_time_info = '本次运行耗时：%s分%s秒' % (run_time[0], run_time[1])
    check_log(info=run_time_info)
    # ----------------------------------------------------------------
