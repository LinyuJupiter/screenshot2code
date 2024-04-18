import sys

from PyQt5.QtWidgets import QApplication

from main_form import MainForm

if __name__ == "__main__":
    # 固定的，PyQt5 程序都需要 QApplication 对象。sys.argv 是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MainForm(url="ws://localhost:7001/generate-code")
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit 方法确保程序完整退出。
    sys.exit(app.exec_())
