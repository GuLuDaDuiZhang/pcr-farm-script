import math
import time
import action
import device
import task
from log import LogTool
import parameters
from tkinter import messagebox, Tk


def get_account(file: str) -> list:
    with open(file, 'r') as f:  # "r"方式读时，文件中的'\r\n'会被系统替换为'\n'
        account_list = f.readlines()
    return [[str.strip(account.split(' ')[0]), str.strip(account.split(' ')[1])] for account in account_list]


def hint():
    device_quantity = len(device_list)
    account_quantity = len(account_list1)
    account_quantity2 = len(account_list2)
    main_log.info('大号：%s' % parameters.BOSS)
    main_log.info('农场1会长：%s' % parameters.FARM_1_LEADER)
    main_log.info('农场2会长：%s' % parameters.FARM_2_LEADER)
    main_log.info('农场1：%s' % parameters.FARM_1_NAME)
    main_log.info('农场2：%s' % parameters.FARM_2_NAME)
    main_log.info('模拟器数量：%s' % device_quantity)
    main_log.info('accountlist.txt内账号数量：%s' % account_quantity)
    main_log.info('accountlist2.txt内账号数量：%s' % account_quantity2)
    info = '大号：' + str(parameters.BOSS) + \
           '\n农场1会长：' + str(parameters.FARM_1_LEADER) + \
           '\n农场2会长：' + str(parameters.FARM_2_LEADER) + \
           '\n农场1：' + parameters.FARM_1_NAME + \
           '\n农场2：' + parameters.FARM_2_NAME + \
           '\n模拟器数量：' + str(device_quantity) + \
           '\naccountlist.txt内账号数量：' + str(account_quantity) + \
           '\naccountlist2.txt内账号数量：' + str(account_quantity2) + \
           '\nIS_NEW_DEV_LOGIN=' + str(parameters.IS_NEW_DEV_LOGIN) + \
           '\n请仔细确认！如果账号内容有改动要在parameters.py里进行相关配置'
    Tk().withdraw()
    if not messagebox.askokcancel("运行前请仔细核对账号等信息！", info):
        exit()

    # check_time = 8  # 任务执行前等待一段时间以便检查账号等数据是否符合预期
    # for i in range(0, check_time + 1):
    #     if i != check_time:
    #         print('\r脚本运行前倒计时:' + str(check_time - i), end=' ')
    #         time.sleep(1)
    #     else:
    #         print('\r开始执行设定任务...')


def check_log(file: str = None, info: str = None):
    # 用来找出登录失败的账号
    result = ''
    if file is None:
        file = log.filename
    else:
        file = 'log\\' + file

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if line.find('登录失败') != -1:
            print(line, end='')
            result += line

    if info is not None:
        result += info
    if result != '':
        messagebox.showinfo("请检查！", result)


if __name__ == '__main__':
    # -------------这些代码是脚本准备工作，不了解的情况下不要动---------------
    start = time.time()
    device.connect_ADB()
    log = LogTool()
    main_log = log.get_logging('main_log')
    device.init_device_list(log)
    device_list = device.get_device_list()
    account_list1 = get_account('accountlist.txt')
    account_list2 = get_account('accountlist2.txt')

    hint()  # 执行前检查账号
    device.start_priconne()  # 启动公主连结
    # ----------------------------------------------------------------

    # 下面两条用于创建农场行会
    # task.task_create_guild_and_join(device_list, account_list1, FARM_1_NAME)
    # task.task_create_guild_and_join(device_list, account_list2, FARM_2_NAME)

    # 下面两条用于通关1-1困难，使用时会买一管体力
    # task.task_adventure_1_1_hard_3_stars(device_list, account_list1)
    # task.task_adventure_1_1_hard_3_stars(device_list, account_list2)

    # 40对1刷玛娜
    # is_complete_daily可选是否完成每日任务，开启耗时会很久，建议先False，刷玛娜稳定且3星通关困难1-1后才考虑=True
    # buy_energy_round买体次数，数值不要超过8，平时建议6就够了，开了完成每日任务才会生效
    # task.task_40_to_1(device_list, account_list1, account_list2, is_complete_daily=False, buy_energy_round=6)

    # 刷1-1，不同之处在于这个是可以买8管以上的体力，用来紧急提升等级
    # task.task_adventure_1_1_leve_up(device_list, account_list1, buy_energy_round=8)
    # task.task_adventure_1_1_leve_up(device_list, account_list2, buy_energy_round=8)

    # 下面这几条预留代码方便后续调试
    # d_l = device.get_device_list()
    # d_l[0].click_byCv('btn_register')
    # d_l[0].click(535,205)
    # action
    # task
    # check_log(file='2020-08-08_03-59-37.log')

    # -------------这些代码是脚本收尾工作，不了解的情况下不要动---------------
    device.quit_ADB()
    run_time = divmod(math.ceil(time.time() - start), 60)
    run_time_info = '本次运行耗时：%s分%s秒' % (run_time[0], run_time[1])
    check_log(info=run_time_info)
    # ----------------------------------------------------------------
