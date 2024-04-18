import subprocess

# 前端和后端可执行文件的路径
frontend_executable = "frontend/frontend/frontend.exe"
backend_executable = "backend/backend/backend.exe"

# 前端和后端可执行文件所在的文件夹
frontend_cwd = "frontend/frontend"
backend_cwd = "backend/backend"

# 启动前端服务
frontend_process = subprocess.Popen([frontend_executable], cwd=frontend_cwd)

# 启动后端服务
backend_process = subprocess.Popen([backend_executable], cwd=backend_cwd)

# 等待前端服务退出
frontend_process.wait()

# 前端服务退出后，结束后端服务
backend_process.terminate()
