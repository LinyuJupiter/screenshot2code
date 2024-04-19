# 后端项目概述

## 项目结构

```
│  app.log # 日志文件
│  config.json # 环境变量储存文件
│  favicon.ico # 打包应用的图标
│  load_env.py # 加载环境变量
│  main.py # 主程序
│  packing.sh # 打包脚本
│  run.bat # Windows系统所用的启动后端服务脚本
│  run.sh # Linux系统所用的启动后端服务脚本
│  start.py # 手动启动主程序的代码
│  stop.bat # Windows系统所用的停止后端服务脚本
│  stop.sh # Linux系统所用的停止后端服务脚本
│  test.html # 测试用网页文件
│  testing.py # 测试后端接口代码
│  
├─generation
│      generate_code.py # 总接口
│      image_generation.py # 向图像生成模型发送信息并接收响应
│      llm.py # 向大模型发送信息并接收响应
│      __init__.py
│      
└─prompts
        system_prompt.py # 系统提示词变量集合
        __init__.py # 提供组装提示词与对话记录数组的函数

```

## 项目逻辑

后端程序的主要逻辑主要在`generation/generate_code.py`中，该文件是整个后端程序的总接口。

前端程序与后端的`localhost:7001/generate-code`接口进行通信，该接口与前端建立websocket连接，调用`generation/generate_code.py`中的`stream_code`函数，该函数调用`generation/image_generation.py`中的函数与`generation/llm.py`中的函数，实现代码与图像生成功能，并向前端发送状态信息与流式响应。

## 运行后端界面

在安装了所有依赖之后，您可以通过以下命令启动后端服务：

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 7001

# 或者使用以下命令
python3 start.py
```

在Linux服务器上，您也可以通过以下命令启动或终止后端服务：

```bash
cd backend
sh run.sh  # 启动服务
sh stop.sh # 终止服务
```

在Windows系统上，您也可以通过以下命令启动或终止后端服务：

```bash
cd backend
run.bat  # 启动服务
stop.bat   # 终止服务

# 或者使用以下命令
python3 start.py
```
在Windows系统上，您也可以在[Releases](https://github.com/LinyuJupiter/screenshot2code/releases)里面直接下载backend.7z并解压，双击运行/backend/backend.exe，无需配置任何依赖。