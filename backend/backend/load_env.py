import json
import os


def load_env():
    if os.path.isfile('config.json'):
        # 读取JSON配置文件
        with open('config.json', 'r') as f:
            config = json.load(f)

        # 设置环境变量
        for key, value in config.items():
            os.environ[key] = value
    else:
        print('config.json does not exist.')
