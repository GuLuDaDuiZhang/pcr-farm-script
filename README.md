## 简介
此项目为公主连接简体字b服40对1刷玛娜脚本. 使用OpenCV图像识别，辅以百度OCR进行按钮定位<br>
本脚本灵感来自 [panshujia/pcr-farm-script](https://github.com/panshujia/pcr-farm-script)  改进的地方增加了多线程支持速度更快，有更多更完善的功能且更加易用，支持不同分辨率的屏幕，引入OCR处理动态背景下的内容识别，增加了日志功能方便回溯调试<br>

## 功能
* 40对1刷mana，大号自动加农场，刷完两个农场然后从农场退出来
* 完成每日任务刷小号经验(目前可完成免费扭蛋、购买玛娜、3次困难1-1、10次普通1-1、自动领取任务和邮件奖励)
* 根据账号列表和行会名自动组建农场行会
* 3星通关困难1-1
* 碎钻1-1刷级


## 环境
* Python版本3.8，3.8以下的环境未测试，不支持2.x
* 雷电模拟器4.0，分辨率设置为 平板版 960×540(dpi160)，其余项默认
* 脚本存放路径里不能含有中文 [issues](https://github.com/GuLuDaDuiZhang/pcr-farm-script/issues/1)
* 本项目使用pyCharm进行开发，建议使用pyCharm来运行脚本


## 使用方法
1. 准备环境：
    * 安装python（安装时记得把带有PATH字母选项的勾上）
    * 安装好雷电模拟器后，用雷电多开器创建一个模拟器，通过模拟器里的应用商店下载安装公主连结下载前记得选择下载b服
    * 打开登录公主连结，等待游戏数据安装完毕（新装游戏会更新1G多的数据，所以这里先更新然后再复制模拟器）
    * 在雷电多开器里复制已准备好的模拟器（模拟器数量看电脑配置，建议3个起步，保障游戏能流畅运行最好）
    * 准备百度OCR的API Key、Secret Key，具体步骤可参考 [链接](https://ai.baidu.com/forum/topic/show/867951)
    
2. 运行脚本：
    * 在`parameters.py`模块里把基础信息补全。**详见注释**
    * 在`accountlist.txt`和`accountlist2.txt`里填入农场号数据，一个文件为1个行会，每个文件最多29个号
    
        ```
        格式（账号+空格+密码+回车换行） 如下所示
        id1 password1
        id2 password2
        id3 password3
        ...
        ```
    * 在`main.py`模块里定制要执行的任务。**详见注释**
    * 启动模拟器，运行脚本。
    * ~~脚本奔溃、流程卡死(≧▽≦*)~~
* **尽量在网络良好的环境下运行，不要下载和挂代理，以提高稳定性**
* **脚本的运行日志里面包含有账号密码信息，请谨慎处理！**



## 额外补充
* 游戏有大型更新（指需从应用商店重新下载安装），删除所有模拟器，重新准备环境详见使用方法，然后把脚本参数IS_NEW_DEV_LOGIN=True，跑过几轮后再False
* 农场号用的是网易邮箱的话，收验证码可以用 [网易邮箱大师](https://mail.163.com/dashi/) ，不用绑定手机号就可以登录，也没有登录验证码


## 更新历史
* 2020/9/29
    * 游戏登录UI有改动，脚本同步更新
    * 游戏登录需同意隐私协议，脚本同步更新

* 2020/9/13
    * 增加对弱网加载和游戏异常中断返回标题的处理
    * 补充账号登录失败时的处理
    * 增加一个控制日志开关的脚本参数
    * ocrtool模块更新完善功能

* 2020/9/9
    * 重新截取所有模板源，调整图像识别逻辑，脚本使用不受电脑屏幕分辨率影响
    * 优化40对1逻辑，现在默认使用战斗力最高的干员做为支援
    * 优化地下城逻辑，增加空支援、已进入地下城、昨日的地下城未刷完的判断处理
    * 优化完成每日，用ocr代替掉一个脚本参数
    * 优化行会创建，遇到已加入行会的小号会跳过剩下的操作并记录进日志
    * 增加单刷一个农场的任务 [issues](https://github.com/GuLuDaDuiZhang/pcr-farm-script/issues/1)
    * 增加独立的完成每日的任务 [issues](https://github.com/GuLuDaDuiZhang/pcr-farm-script/issues/1)
    * 补充各任务的注意事项
    * ocrtool模块更新完善功能
    * main模块优化运行前提示
    * 精简parameters模块里的参数项

* 2020/8/30
    * 解决百度OCR的QPS超限额导致的脚本运行出错

* 2020/8/22
    * 初步引入百度OCR，做为动态背景下OpenCV模板匹配识别乏力的补充（更新脚本后参考使用方法里的新步骤，申请并填写百度OCR的AK、SK）
    * 优化登录逻辑，现在脚本可以自己更新游戏、针对登录时数据加载慢和通知弹窗弹出慢的情况做了处理，脚本会等待动作完成
    * 针对完成每日任务，买体后点击底部导航栏的冒险，偶现游戏卡死的情况做了处理，遇到这种情况脚本会重启游戏
    * 修改挑战地下城的逻辑，无法进入地下城会直接退出游戏切到下一个账号
    * cv2tool模块里代码变量名修正、device模块增加判断元素是否存在的函数
    
* 2020/8/8
    * 优化登录逻辑，现在会记录登录失败的账号，在循环登录多个账号的action里，当前账号登录失败会跳过剩下的操作节省时间
    * 优化脚本执行前后的逻辑，现在脚本执行前会弹对话框来确认账号信息，脚本执行完毕后会弹对话框告知耗时和登录失败的账号
    
* 2020/8/4
    * 增加买8管体以上的刷1-1的任务，用于紧急提升等级
    * 代码细节优化提升性能

## 免责声明
当你下载或使用本项目，将默许<br>
本项目仅供交流和学习使用，请勿用此从事 违法/商业盈利等，开发者拥有本项目的最终解释权