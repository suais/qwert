# qwert 基于ChatGPT终端工具


qwert是一个基于chatgpt开发的终端工具，其功能类似于Warp，与Warp不同的是qwert可以工作在不同的环境中，Warp是基于独立客户端使用的，并且只能在Mac上工作。

qwert可以在任何终端中工作，比如在VsCode中，这很大的提高了效率，避免了开发过程中频繁的应用切换。

目前还未完善自动命令补全

qwert主要有2种指令：
```
# <command> 生成指令模式
qwert
(qwert) root@hgodeMac:/Users/hgo# # 帮我远程连接主机192.168.0.2                                                                                                                                                 
(qwert edit) root@hgodeMac:/Users/hgo# ssh 192.168.0.2 
? <ask> 对话模式
qwert
(qwert) root@hgodeMac:/Users/hgo# ? 你好                                                                                                                                        
你好！有什么我可以帮助你的吗？
```
# 配置文件
默认情况下，qwert免费提供了ChatGPT3.5的api，不限制使用次数(Warp免费账户每日限制100条的AI功能)，不过目前还不能提供稳定的连接，如果您有可用的openai key可以自定义在配置文件中修改：

在Linux或Mac中：
```
sudo vim /usr/local/share/qwert/config.ini
```

将 type = remote 修改为 type = local
   key = <this is your api key>
替换为你自己的key即可
如遇网络错误，则会产生`network error`，您只需重试命令即可。

目前qwert还未对命令模式产生的结果进行校验，由ChatGPT默认生成的命令会有一些结果不准确，您只需删除不需要的字符即可

在Mac上安装

```
# 下载安装脚本
sudo curl -o install_qwert_mac_1.0.sh https://dev.hgostand.com/upload/install_qwert_mac_1.0.sh
# 赋予安装脚本权限
sudo chmod +x install_qwert_mac_beta_1.0.sh
# 安装qwert
sudo ./install_qwert_mac_beta_1.0.sh

sudo qwert # 首次运行获取权限
```

# 在终端输入
```
qwert

beta 1.0
Please enter 'exit' to terminate the program.
The application files are located in this path: /usr/local/share/qwert/config.ini
You can setting this:
type = local, use local openai api
type = remote, use default (qwert) api, chat-gpt3.5 it's free! No restrictions.
```
# 这表明安装成功
在Linux中安装

# 未编译
在Windows中安装

下载bat脚本文件：
https://dev.hgostand.com/upload/install_qwer_win_beta_1.0.bat
右键管理员运行
打开termin输入qwert即可运行
脚本自动配置了环境变量