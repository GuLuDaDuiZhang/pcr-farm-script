# --------------------------------------账号信息--------------------------------------
BOSS = ['账号', '密码']  # 大号
FARM_1_LEADER = ['账号', '密码']  # 农场1会长
FARM_2_LEADER = ['账号', '密码']  # 农场2会长

# 行会名要确保唯一性，搜索结果只有你创建的这一个行会
# 使用脚本创建行会时，推荐使用密码生成器生成一串数字当名字，但注意不能含有‘89’和‘64’否则会敏感词创建失败
FARM_1_NAME = '行会名'  # 农场1行会名字，脚本不支持中文输入，只能由英文和数字组成，不超过10个字符
FARM_2_NAME = '行会名'  # 农场2行会名字，脚本不支持中文输入，只能由英文和数字组成，不超过10个字符

# --------------------------------------cv2tool模块参数--------------------------------------
SCREEN_RESOLUTION = '2560'  # 输入电脑分辨率，这也要是存放对应分辨率识别素材的文件夹名字
IDENTIFY_THRESHOLD = 0.8  # 素材相关系数阈值，值越高识别精度越高，太高容易识别不到素材位置，太低则可能取到错误的位置不利于调试，按自己情况调整

# --------------------------------------device模块参数--------------------------------------
ADB_PATH = 'cd adb & '  # 如果电脑已经配置了adb环境变量，则=''，否则='cd adb & '使用脚本自带的adb
SCREENSHOT_DELAY = 2  # 截图延迟一段时间执行，单位s。减少截图过快截在了加载状态页面的情况
IDENTIFY_ROUND = 5  # 当截图里没有识别到所需内容时，会重新截图，截图次数达到这个最大值后会放弃识别当前素材
CLICK_DELAY = 2  # 点击会延迟一段时间执行，单位s。减少点击过快点在了加载状态页面的情况

# --------------------------------------action模块参数--------------------------------------
LOADING_TIME = 6.5  # 读条、加载状态、解锁动画时脚本的等待时间
LOGIN_PARAMETERS = 0  # =0无活动时的登录流程；=1跳过兰德索尔杯；
BACK_TO_JUNO = 2  # 用于刷1-1时回退到朱诺平原点击回退按钮的次数，如果号是刷到3图则填2，刷到4图填3以此类推

# 账号在模拟器上是首次登录会有解锁动画和指导对话，=True跳过这些
# 执行不同任务、修改代码、修改账号数据和尝试不同数量的模拟器都应=True
# 只有在脚本能稳定执行任务后，才=False提高运行速度,建议刷mana稳定运行两次后=False，如果开了做每日任务也要完成每日任务稳定运行两次后=False
IS_NEW_DEV_LOGIN = True
