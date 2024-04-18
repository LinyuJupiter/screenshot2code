@echo off
REM 启动uvicorn服务，并将输出重定向到nohup.out文件
start /b python main:app --host 0.0.0.0 --port 7001 > nohup.out 2>&1
