import json

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWebSockets import QWebSocket


class WebSocketClient(QObject):
    message_received = pyqtSignal(dict)
    disconnected = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.websocket = QWebSocket()

        # 连接信号
        self.websocket.textMessageReceived.connect(self.process_text_message)
        self.websocket.disconnected.connect(self.on_disconnected)

    def open_connection(self, url):
        self.websocket.open(url)

    def close_connection(self):
        self.websocket.close()

    def send_json(self, json_data):
        self.websocket.sendTextMessage(json.dumps(json_data))

    def process_text_message(self, message):
        # 将接收到的文本消息转换为JSON
        try:
            data = json.loads(message)
            # 发射信号，将处理后的数据传递给UI
            self.message_received.emit(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def on_disconnected(self):
        # 发射信号，通知UI连接已断开
        self.disconnected.emit()
