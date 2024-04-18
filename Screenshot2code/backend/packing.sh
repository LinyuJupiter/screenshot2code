cd ./backend
pyinstaller -D --add-data "main.py;." --add-data "load_env.py;." --add-data "config.json;." --add-data "app.log;." --add-data "prompts;prompts" --add-data "generation;generation" -w -i favicon.ico -n backend start.py --upx-dir D:\upx-3.96-win64\
