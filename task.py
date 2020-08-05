import math
import action
from concurrent.futures import ThreadPoolExecutor, wait
from parameters import FARM_1_LEADER, FARM_2_NAME, FARM_2_LEADER, FARM_1_NAME


def chunks_account(arr: list, m: int) -> list:
    # 该函数用来将账号平均分配给模拟器
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]


def thread_run_action(fun, device_list: list, account_list: list, *other_parameter):
    # 为每一个模拟器启动一个线程执行任务
    # 注意传入的fun的第一个参数必须为Device类，第二个参数必须为一个账号数据列表
    device_amount = len(device_list)
    account_list = chunks_account(account_list, device_amount)
    result = []
    t = ThreadPoolExecutor(device_amount)  # 启动线程池，一个模拟器分一个线程
    for i in range(device_amount):
        result.append(t.submit(fun, device_list[i], account_list[i], *other_parameter))
    wait(result)
    for res in result:
        print(res.result())  # 捕捉抛出的异常


def task_40_to_1(device_list: list, account_list1: list, account_list2: list, is_complete_daily: bool,
                 buy_energy_round: int):
    # 40对1获取玛娜，运行逻辑是大号先加入第一个农场上架支援，然后农场小号借支援轮巡完，踢出大号加第二个农场重复一遍操作
    action.boss_join_guild_and_set_aid(device_list[0], FARM_1_NAME)  # 大号加入农场1
    thread_run_action(action.underground_city_battle_and_logout, device_list, account_list1, is_complete_daily,
                      buy_energy_round)
    action.boss_go_to_second_farm(device_list[0], FARM_1_LEADER, FARM_2_NAME)  # 踢掉大号加入农场2
    thread_run_action(action.underground_city_battle_and_logout, device_list, account_list2, is_complete_daily,
                      buy_energy_round)
    action.fire_role(device_list[0], FARM_2_LEADER)  # 踢掉大号


def task_create_guild_and_join(device_list: list, account_list: list, guild_name: str):
    # 账号数据中第一行的账号组建行会作为会长，然后其它账号加入
    leader = account_list.pop(0)
    action.create_guild(device_list[0], leader, guild_name)
    thread_run_action(action.join_guild_and_logout, device_list, account_list, guild_name)
    print('创建完毕，记得在parameters里填写农场会长的账号，默认会长是账号文件里的第一行账号')


def task_adventure_1_1_hard_3_stars(device_list: list, account_list: list):
    # 用来通1-1的3星
    thread_run_action(action.adventure_1_1_hard_3_stars, device_list, account_list)


def task_adventure_1_1_leve_up(device_list: list, account_list: list, buy_energy_round: int):
    # 买体刷1-1，和40对1里的买体刷1-1不同之处在于这个是可以买8管以上的体力，用来紧急刷级
    thread_run_action(action.adventure_1_1_leve_up, device_list, account_list, buy_energy_round)
