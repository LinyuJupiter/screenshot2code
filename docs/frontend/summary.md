# 前端项目概述

## 项目结构

```
│  main.py # 主执行程序
│  main_form.py # 主面板的功能实现
│  main_window.py # 主面板的UI实现
│  main_window.ui # 主面板的UI文件
│  packing.sh # 打包脚本
│  settings_dialog.py # 设置窗口的功能实现
│  settings_window.py # 设置窗口的UI实现
│  settings_window.ui # 设置窗口的UI文件
│  websocket_client.py # websocket客户端
│  
└─images
        favicon.ico # 主面板的图标，以及打包时的文件图标
        setting.png # 设置窗口的图标
```

## 项目逻辑

前端程序的逻辑主要在`main_form.py`中，通过调用`main_window.py`和`settings_window.py`实现UI界面，并通过`websocket_client.py`实现与后端的通信，最后，使用`main.py`作为主程序，实现程序的启动和关闭。

## 运行前端界面

前端程序只能在Windows系统上运行，在安装了所有依赖之后，您可以通过以下命令启动前端程序：

```bash
cd frontend
python3 main.py
```
您也可以在[Releases](https://github.com/LinyuJupiter/screenshot2code/releases)里面直接下载frontend.7z并解压，双击运行/frontend/frontend.exe，无需配置任何依赖。
