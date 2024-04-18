cd ./frontend
pyinstaller -D --add-data "main_form.py;." --add-data "main_window.py;." --add-data "settings_dialog.py;." --add-data "settings_window.py;." --add-data "websocket_client.py;." --add-data "images;images" -w -i ./images/favicon.ico -n frontend main.py --upx-dir D:\upx-3.96-win64\
