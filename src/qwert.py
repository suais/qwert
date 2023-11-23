import os
import sys
import json
import subprocess
import socket
import requests
import configparser
import platform
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
os_name = platform.system()

APP_NAME = '(qwert)'
VRESION = "beta 1.0"

if os_name == 'Darwin' or os_name == 'Linux':
    HOST_NAME = socket.gethostname().replace('.local', '')
if os_name == 'Windows':
    HOST_NAME = socket.gethostname()

CONFIG_local = "local"
CONFIG_remote = "remote"

# osx path
if os_name == 'Darwin':
    config_file = "/usr/local/share/qwert/config.ini"

# linux path
if os_name == 'Linux':    
    config_file = "/usr/local/share/qwert/config.ini"

# windows path
if os_name == 'Windows':
    app_data = dir_path = '%s\\qwert\\' %  os.environ['APPDATA']
    config_file = '%sconfig.ini' % app_data
    
def create_floder(path):
    floder = os.path.dirname(path) 
    if not os.path.exists(floder):
        os.makedirs(floder)

def create_ini(path):
    
    config = configparser.ConfigParser()
    config.add_section('network')
    config.set('network', 'type', 'remote')
    config.add_section('openai')
    config.set('openai', 'url', 'https://api.openai.com/v1/chat/completions')
    config.set('openai', 'key', 'this is your api key')
    
    if not os.path.exists(path):
        create_floder(config_file)
        with open(path, 'w') as file:
            config.write(file)
            
create_ini(config_file)

config = configparser.ConfigParser()
config.read(config_file)

# remote_qwert test api
NETWORK_CON = config.get('network', 'type')
remote_url = "https://api.freegpt.hgostand.com/"
authorization = "Bearer 1234567890"
headers = {"Authorization": authorization}

# openai api
openai_key = config.get('openai', 'key')
openai_url = config.get('openai', 'url')


def shell_prompt(prompt):
    text_1 = "You will imitate an intelligent terminal. By default, you are a Linux terminal. Do not provide any textual explanations to me. "
    # text_1 = "你将模仿一个智能的终端，默认情况下你是Linux终端，不要给我任何的文字解释 "
    
    text_2 = "Do not return symbol format containing code block, only give me the corresponding command code. "
    # text_2 = "不要返回包含代码块的符号格式，请只给我相应的命令代码即可 "

    text_3 = "Need to give examples of command parameters, such as ssh -p 24 root@remote. Do not use any extra text to explain the parameters. "
    # text_3 = "需要举例出命令的参数，例如 ssh -p 24 root@remote 不要用任何多余的文本解释参数 "

    text_4 = "Provide detailed answers and respond with only the necessary text "
    # text_4 = "给出详细的答案，请每次只回答一条，并返回不包含任何多余文本的响应 "

    text_5 = "If you need me to fill it in manually, please use <> to enclose it. If the command is not found, please return an empty string directly. "
    # text_5 = "如需我手动填写的请用<>包含, 如果没有找到该命令，请直接返回空字符串 "

    text_6 = "Please provide a one-line command. "
    # text_6 = "请返回一行命令行 "

    text_7 = "If there is no suitable answer, please don't return any content "
    # text_7 = "如果没有合适的答案请不要返回任何内容 "

    text_8 = "You are playing the role of a character who outputs command lines. "
    # text_8 = "你扮演的是一个输出命令行的角色 "

    text_9 = "The current system platform is:" + os_name + ' '
    # text_9 = "当前系统平台是" + os_name + ' '

    text_10 = " Please tell me only one command to return the contents in Markdown, without explaining any parameters. "
    # text_10 = "请只告诉一条命令 "

    text_11 = " No text No text No text "
    # text_10 = "请只告诉一条命令 "

    text_last = f"Please tell me how to execute this command in the terminal.{prompt}，Do not give me any textual explanations. "
    # text_last = f"请告诉我如何在终端中执行这条语句:{prompt}，不要给我任何的文字解释 "

    texts = text_1 + text_2 + text_3 + text_4 + text_5 + text_6 + text_7 + text_8 + text_9 + text_10 + text_last
    return texts

def ask_prompt(prompt):
    return prompt

class Color(object):
    RESET = "\033[0m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    BOLD = "\033[1m" 
    UNDERLINE = "\033[4m"
    REVERSE = "\033[7m"

    t_style = Style.from_dict({
        # User input (default text).
        '':          '#ff0066',

        # Prompt.
        'appname':  '#ffffff bg:#000000',
        'username': '#884444',
        'at':       '#00aa00',
        'colon':    '#0000aa',
        'pound':    '#000000',
        'host':     '#00ffff',
        'path':     'ansicyan',
        })

    def t_msg(name, user, host, path):
        
        message = [
            ('class:appname', name),
            ('class:username', ' '+user),
            ('class:at',       '@'),
            ('class:host',     host),
            ('class:colon',    ':'),
            ('class:path',     path),
            ('class:pound',    '# '),
        ]
        return message

class OhMyGPT(object):
    
    def __init__(self) -> None:
        self.KEY = openai_key
        self.url = openai_url

    def chatGPT(self, prompt):
        
        url = self.url
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
            ]
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.KEY}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            item = json.loads(response.text)
            result = item['choices'][0]['message']['content']
            return result
        else:
            return "network error"

def remote_chatgpt(prompt):
    
    data = {'prompt':prompt}
    response = requests.post(remote_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        return "network error"

def gpt_network(type_config, prompt):

    if type_config == CONFIG_remote:
        respone = remote_chatgpt(prompt)
        return respone
    
    if type_config == CONFIG_local:
        my_gpt = OhMyGPT()
        respone = my_gpt.chatGPT(prompt)
        return respone

def outputer(output):
    
    for line in output.split('\n'):
        if line in " ":
            continue
        else:
            print(line)

def terminal(app_name=APP_NAME):
    
    home_directory = os.path.expanduser("~")
    current_directory = home_directory
    
    if os_name == 'Darwin' or os_name == 'Linux':
        current_user = os.environ['USER']
    if os_name == 'Windows':
        current_user = os.getenv('USERNAME')
    
    print(Color.RED + VRESION + Color.RED)
    print(Color.RED + "Please enter 'exit' to terminate the program." + Color.RED )
    print(f'The application files are located in this path: {config_file}')
    print("You can setting this:")
    print("type = local, use local openai api")
    print("type = remote, use default (qwert) api, chat-gpt3.5 it's free! No restrictions.")

    session = PromptSession()
    
    while True:
        try:
            app_name = APP_NAME
            default = ""

            command = session.prompt(Color.t_msg(app_name, current_user, HOST_NAME, current_directory) ,default=default, style=Color.t_style)

            if command.lower() == 'exit':
                sys.exit()

            if command.startswith('cd '):

                if command[3:].strip() == "~":
                    os.chdir(home_directory)
                    current_directory = os.getcwd()
                else:
                    target_directory = command[3:].strip()
                    os.chdir(os.path.join(current_directory, target_directory))
                    current_directory = os.getcwd()
            
            elif command.startswith('su '):
                
                new_user = command[3:].strip()
                os.seteuid(0)
                current_user = new_user
            
            elif command.startswith('#'):
                
                default = gpt_network(type_config=NETWORK_CON, prompt=shell_prompt(command[1:].strip()))
                app_name = '(qwert edit)'
                command = session.prompt(Color.t_msg(app_name, current_user, HOST_NAME, current_directory), default=default, style=Color.t_style)

                try:
                    output = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, text=True, cwd=current_directory)
                    out, _ = output.communicate()
                    
                    if out is not None:
                        outputer(out)
                    
                except Exception as e:
                    print(str(e))
            
            elif command.startswith('?'):
                
                echo = gpt_network(type_config=NETWORK_CON, prompt=ask_prompt(command[1:].strip()))
                print(echo)
            else:
                
                output = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, text=True, cwd=current_directory)
                out, _ = output.communicate()
                
                if out is not None:
                        outputer(out)
        
        except subprocess.CalledProcessError as e:
            print(e.output)
        
        except Exception as e:
            print(str(e))                

        except KeyboardInterrupt:
            print("Please enter 'exit' to terminate the program.")


if __name__ == '__main__':
    app = terminal()