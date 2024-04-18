from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

from settings_window import Ui_Dialog


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # 禁止显示帮助按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 创建QRegExp，允许数字、字母和特定符号
        regex = QRegExp("^[a-zA-Z0-9!@#$%^&*()_+{}|.:<>?/]*$")
        # 创建QValidator，使用上面的QRegExp
        validator = QRegExpValidator(regex, self.ui.apiKey_lineEdit)
        # 将验证器设置到lineEdit控件
        self.ui.apiKey_lineEdit.setValidator(validator)

        self.api_key = ""  # 智谱的API-key
        self.isImageGenerationEnabled = False  # 是否使用图像生成模型
        # 连接buttonBox的accepted信号到save_settings槽函数
        self.ui.save_buttonBox.accepted.connect(self.save_settings)
        # 连接buttonBox的rejected信号到对话框的reject槽函数
        self.ui.save_buttonBox.rejected.connect(self.reject)

    def save_settings(self):
        # 保存设置
        self.api_key = self.ui.apiKey_lineEdit.text()
        self.isImageGenerationEnabled = self.ui.img_checkBox.isChecked()
        # 通常在保存设置后，您可能想要关闭对话框
        self.accept()
