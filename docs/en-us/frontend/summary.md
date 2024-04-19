# Frontend Project Overview

## Project Structure

```
│  main.py # Main execution program
│  main_form.py # Function implementation of the main panel
│  main_window.py # UI implementation of the main panel
│  main_window.ui # UI file of the main panel
│  packing.sh # Packaging script
│  settings_dialog.py # Function implementation of the settings window
│  settings_window.py # UI implementation of the settings window
│  settings_window.ui # UI file of the settings window
│  websocket_client.py # WebSocket client
│  
└─images
        favicon.ico # Icon of the main panel and file icon during packaging
        setting.png # Icon of the settings window
```

## Project Logic

The logic of the frontend program is mainly in `main_form.py`, which utilizes `main_window.py` and `settings_window.py` for UI implementation, and communicates with the backend through `websocket_client.py`. Finally, `main.py` serves as the main program to start and close the application.

## Running the Frontend Interface

The frontend program can only run on Windows systems. After installing all dependencies, you can start the frontend program with the following command:

```bash
cd frontend
python3 main.py
```
Alternatively, you can directly download frontend.7z from [Releases](https://github.com/LinyuJupiter/screenshot2code/releases) and extract it. Double-click on /frontend/frontend.exe to run it without configuring any dependencies.