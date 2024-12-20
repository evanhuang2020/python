import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit

class MortgageCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('房贷计算器')
        self.setGeometry(100, 100, 400, 300)

        # 创建布局
        layout = QVBoxLayout()

        # 贷款总额输入
        self.principal_label = QLabel('贷款总额（元）:')
        self.principal_edit = QLineEdit()
        layout.addWidget(self.principal_label)
        layout.addWidget(self.principal_edit)

        # 年利率输入
        self.rate_label = QLabel('年利率（例如5%就输入0.05）:')
        self.rate_edit = QLineEdit()
        layout.addWidget(self.rate_label)
        layout.addWidget(self.rate_edit)

        # 贷款月数输入
        self.months_label = QLabel('贷款月数:')
        self.months_edit = QLineEdit()
        layout.addWidget(self.months_label)
        layout.addWidget(self.months_edit)

        # 计算按钮
        self.calculate_button = QPushButton('计算')
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # 显示结果
        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        layout.addWidget(self.result_text_edit)

        self.setLayout(layout)

    def calculate(self):
        try:
            principal = float(self.principal_edit.text())
            annual_interest_rate = float(self.rate_edit.text())
            months = int(self.months_edit.text())

            monthly_interest_rate = annual_interest_rate / 12
            monthly_payment = (principal * monthly_interest_rate * (1 + monthly_interest_rate) ** months) / ((1 + monthly_interest_rate) ** months - 1)
            total_interest = self.calculate_total_interest(principal, monthly_payment, months, annual_interest_rate)

            result = f"每月还款额为：{monthly_payment:.2f}元\n总支付利息为：{total_interest:.2f}元"
            self.result_text_edit.setText(result)
        except ValueError:
            self.result_text_edit.setText("请输入有效的数字")

    def calculate_total_interest(self, principal, monthly_payment, months, annual_interest_rate):
        total_interest = 0
        monthly_interest_rate = annual_interest_rate / 12
        remaining_principal = principal
        for _ in range(months):
            interest = remaining_principal * monthly_interest_rate
            remaining_principal -= min(monthly_payment - interest, remaining_principal)
            total_interest += interest
        return total_interest

def main():
    app = QApplication(sys.argv)
    ex = MortgageCalculator()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()