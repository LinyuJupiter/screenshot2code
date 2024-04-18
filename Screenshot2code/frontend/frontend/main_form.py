import base64
import html
import json
import os.path

from PyQt5.QtCore import Qt, pyqtSlot, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout

from settings_dialog import SettingsDialog
from main_window import Ui_MainWindow
from websocket_client import WebSocketClient


def image_to_data_url(filepath: str):
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"{encoded_string}"


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, url: str, parent=None):
        super(MainForm, self).__init__(parent)
        self.url = url
        self.setupUi(self)
        self.run_variables()
        # 创建 QWebEngineView 实例
        self.web_view = QWebEngineView(self)
        self.web_view.setHtml(self.html)
        # 创建一个 QVBoxLayout 实例
        self.layout = QVBoxLayout(self.html_frame)
        # 将 QWebEngineView 添加到布局中
        self.layout.addWidget(self.web_view)
        # 设置 html_frame 的布局
        self.html_frame.setLayout(self.layout)
        # 连接单选按钮的 clicked 信号到槽函数
        self.web_Button.clicked.connect(self.toggle_view)
        self.web_Button.setCursor(Qt.PointingHandCursor)
        self.code_Button.clicked.connect(self.toggle_view)
        self.code_Button.setCursor(Qt.PointingHandCursor)
        # 为 img_label 控件添加点击事件
        self.img_label.mousePressEvent = self.open_image
        self.img_label.setCursor(Qt.PointingHandCursor)
        # 连接 export_Button 的 clicked 信号到槽函数
        self.export_Button.clicked.connect(self.export_html)
        self.export_Button.setCursor(Qt.PointingHandCursor)
        # 连接 toolButton 的 clicked 信号到槽函数
        self.toolButton.clicked.connect(self.show_settings_dialog)
        self.toolButton.setCursor(Qt.PointingHandCursor)
        # 连接 generate_Button 的 clicked 信号到槽函数
        self.generate_Button.clicked.connect(self.connect_to_server)
        self.generate_Button.setCursor(Qt.PointingHandCursor)
        # generate_Button 使用的WebSocket客户端
        self.websocket_client = WebSocketClient()
        self.websocket_client.message_received.connect(self.update_label)
        self.websocket_client.disconnected.connect(self.handle_disconnection)

    def run_variables(self):
        # 定义初始化变量
        self.html = ""  # 生成的网页源码
        self.img_path = None  # 选择的网页截图路径
        self.api_key = ""  # 智谱的API-key
        if os.path.isfile("api_key.txt"):
            with open("api_key.txt", "r", encoding="utf-8") as file:
                self.api_key = file.read()
        self.isImageGenerationEnabled = False  # 是否使用图像生成模型

    def open_image(self, event):
        # 打开文件选择窗口
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.png *.jpg *.bmp)")
        if file_name:
            self.img_path = file_name
            # 使用 QPixmap 加载图片
            pixmap = QPixmap(file_name)
            # 将图片缩放到 label 大小
            self.img_label.setPixmap(pixmap.scaled(self.img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    @pyqtSlot()
    def toggle_view(self):
        # 切换视图按钮点击调用，可以切换显示网页或源码
        if self.html == "":
            return
        if self.code_Button.isChecked():
            # 显示网页源码
            # 对 HTML 源码进行实体编码，确保特殊字符被正确显示
            encoded_html = html.escape(self.html)
            # 定义一些内联样式来改善源码的显示效果
            style = "<style>pre { font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; " \
                    "line-height: 1.5; letter-spacing: 0.1px; }</style>"
            # 将编码后的源码和样式设置到 QWebEngineView 中
            self.web_view.setHtml(f"<html><head>{style}</head><body><pre>{encoded_html}</pre></body></html>")
        else:
            # 显示网页
            self.web_view.setHtml(self.html)

    @pyqtSlot()
    def export_html(self):
        # 导出按钮点击调用
        if self.html != "":  # 如果 self.html 不为空
            # 打开文件夹选择对话框
            folder_path = QFileDialog.getExistingDirectory(self, "选择导出文件夹")
            if folder_path:  # 如果用户选择了文件夹
                # 构建要导出的文件路径
                file_path = folder_path + "/exported_page.html"
                # 将 HTML 内容写入文件
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.html)
                # 可以在这里显示一个消息框，告知用户导出成功
                QMessageBox.information(self, "导出成功", f"HTML 已导出到：{file_path}")
        else:
            # 如果 self.html 为空，可以在这里显示一个消息框，告知用户没有可导出的内容
            QMessageBox.information(self, "导出失败", "没有可导出的内容")

    @pyqtSlot()
    def show_settings_dialog(self):
        # 设置按钮点击调用
        self.dialog = SettingsDialog(self)
        self.dialog.ui.apiKey_lineEdit.setText(self.api_key)

        def save_settings():
            self.dialog.save_settings()
            self.api_key = self.dialog.api_key
            with open("api_key.txt", "w", encoding="utf-8") as file:
                file.write(self.api_key)
            self.isImageGenerationEnabled = self.dialog.isImageGenerationEnabled

        self.dialog.ui.save_buttonBox.accepted.connect(save_settings)
        self.dialog.show()

    @pyqtSlot()
    def connect_to_server(self):
        # 生成按钮点击调用
        self.status_label.setText("")
        if not self.img_path:
            # 如果 img_path 为空，可以在这里显示一个消息框，告知用户需要选择一张图片
            QMessageBox.information(self, "错误", "请先选择一张图片")
            return
        if self.api_key == "":
            # 如果 api_key 为空，可以在这里显示一个消息框，告知用户需要输入智谱的API-key
            QMessageBox.information(self, "警告",
                                    "尚未设置智谱的API-key\n请在设置中输入智谱的API-key\n本次将尝试使用服务器端的默认API-key")
        self.generate_Button.setText("正在生成...")
        self.generate_Button.setEnabled(False)
        self.export_Button.setEnabled(False)
        # 建立WebSocket连接
        self.websocket_client.open_connection(QUrl(self.url))

        # 连接成功建立的槽
        def on_connected():
            # 准备要发送的数据
            data = {
                "type": "message",
                "image": image_to_data_url(self.img_path),
                "visionModel": "glm-4v",
                "codeGenerationModel": "glm-4",
                "zhipuAiApiKey": self.api_key,
                "zhipuAiBaseURL": "https://open.bigmodel.cn/api/paas/v4",
                "isImageGenerationEnabled": self.isImageGenerationEnabled
            }
            # 发送JSON消息到服务器
            self.websocket_client.send_json(data)

        # 连接信号和槽
        self.websocket_client.websocket.connected.connect(on_connected)

    def update_label(self, message):
        # 接受到信息之后更新状态标签以及HTML
        try:
            data = message
            if data.get("type") == "status":
                self.status_label.setText(data.get("value"))
                if data.get("value") == "Generating description..." or data.get("value") == "Generating code...":
                    self.html = ""
            elif data.get("type") == "error":
                self.status_label.setText("ERROR!!!\n" + data.get("value"))
            elif data.get("type") == "chunk":
                self.html += data.get("value")
                self.toggle_view()
            elif data.get("type") == "setCode":
                self.html = data.get("value")
                self.toggle_view()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}, {message}")

    def handle_disconnection(self):
        # 处理连接断开
        self.generate_Button.setText("生成")
        self.generate_Button.setEnabled(True)
        self.export_Button.setEnabled(True)
