@echo off
REM 查找监听端口7001的进程ID
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :7001') do (
    set pid=%%a
)

REM 如果找到了进程ID，则结束该进程
if not "%pid%"=="" (
    taskkill /F /PID %pid%
    echo Process with PID %pid% has been killed.
) else (
    echo No process found listening on port 7001.
)
