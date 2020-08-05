import time
import action
import device
import task
from log import LogTool
from parameters import FARM_1_NAME, FARM_2_NAME, BOSS, FARM_1_LEADER, FARM_2_LEADER


def get_account(file: str) -> list:
    with open(file, 'r') as f:  # "r"方式读时，文件中的'\r\n'会被系统替换为'\n'
        account_list = f.readlines()
    return [[str.strip(account.split(' ')[0]), str.strip(account.split(' ')[1])] for account in account_list]


def hint():
    device_quantity = len(device_list)
    account_quantity = len(account_list1)
    account_quantity2 = len(account_list2)
    main_log.info('大号：%s' % BOSS)
    main_log.info('农场1会长：%s' % FARM_1_LEADER)
    main_log.info('农场2会长：%s' % FARM_2_LEADER)
    main_log.info('农场1：%s' % FARM_1_NAME)
    main_log.info('农场2：%s' % FARM_2_NAME)
    main_log.info('模拟器数量：%s' % device_quantity)
    main_log.info('accountlist.txt内账号数量：%s' % account_quantity)
    main_log.info('accountlist2.txt内账号数量：%s' % account_quantity2)

    check_time = 8  # 任务执行前等待一段时间以便检查账号等数据是否符合预期
    for i in range(0, check_time + 1):
        if i != check_time:
            print('\r脚本运行前倒计时:' + str(check_time - i), end=' ')
            time.sleep(1)
        else:
            print('\r开始执行设定任务...')


if __name__ == '__main__':
    # -------------这些代码是脚本准备工作，不理解的情况下不要动---------------
    device.connect_ADB()
    log = LogTool()
    main_log = log.get_logging('main_log')
    device.init_device_list(log)
    device_list = device.get_device_list()
    account_list1 = get_account('accountlist.txt')
    account_list2 = get_account('accountlist2.txt')
    # ----------------------------------------------------------------

    hint()
    device.start_priconne()  # 启动公主连结

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
    # d_l[0].click_byCv('btn_set_blue_small')
    # d_l[0].click(535,205)
    # action
    # task

    device.quit_ADB()
