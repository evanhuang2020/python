import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

# 检查余额函数
def check_balance(api_key):
    url = 'https://api.siliconflow.cn/v1/user/info'
    headers = {
        'Authorization': f'Bearer {api_key.strip()}'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            if data.get('data', {}).get('balance') is not None:
                return f"✅ {data['data']['balance']} {api_key}"
            else:
                return f"❌ {api_key}, 无效响应数据"
        else:
            return f"❌ {api_key}, HTTP错误 {response.status_code}"
    except Exception as e:
        return f"❌ {api_key}, 请求错误: {e}"

# 工作线程类
class BalanceCheckerThread(QThread):
    finished = pyqtSignal(str)  # 信号，用于传递结果

    def __init__(self, api_keys):
        super().__init__()
        self.api_keys = api_keys

    def run(self):
        results = []
        for key in self.api_keys:
            result = check_balance(key)
            results.append(result)
        self.finished.emit("\n".join(results))

# 主窗口类
class BalanceCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("API余额检查器")
        self.setGeometry(100, 100, 800, 600)  # 增大窗口大小

        # 设置全局字体
        font = QFont()
        font.setPointSize(14)  # 设置字体大小为 14
        QApplication.setFont(font)

        # 布局
        layout = QVBoxLayout()

        # 输入框
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("在此粘贴API密钥，每行一个")
        self.input_text.setFont(QFont("Arial", 14))  # 设置输入框字体
        layout.addWidget(self.input_text)

        # 检查按钮
        self.check_button = QPushButton("检查余额", self)
        self.check_button.setFont(QFont("Arial", 16))  # 设置按钮字体
        self.check_button.clicked.connect(self.on_check_balance)
        layout.addWidget(self.check_button)

        # 结果展示区域
        self.result_label = QLabel("结果将显示在这里", self)
        self.result_label.setAlignment(Qt.AlignTop)
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont("Arial", 14))  # 设置结果区域字体

        # 滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.result_label)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def on_check_balance(self):
        # 获取输入并检查
        keys = self.input_text.toPlainText().strip().split('\n')
        keys = [key.strip() for key in keys if key.strip()]

        if not keys:
            self.result_label.setText("请输入至少一个API密钥")
            return

        # 禁用按钮
        self.check_button.setEnabled(False)
        self.result_label.setText("正在检查...")

        # 启动工作线程
        self.worker = BalanceCheckerThread(keys)
        self.worker.finished.connect(self.on_check_finished)
        self.worker.start()

    def on_check_finished(self, result):
        # 显示结果并启用按钮
        self.result_label.setText(result)
        self.check_button.setEnabled(True)

# 主程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BalanceCheckerApp()
    window.show()
    sys.exit(app.exec_())
