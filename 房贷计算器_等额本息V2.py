import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
import xlsxwriter


class MortgageCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('房贷计算器')
        self.setGeometry(100, 100, 500, 400)

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

        # 导出按钮
        self.export_button = QPushButton('导出Excel')
        self.export_button.clicked.connect(self.export_to_excel)
        self.export_button.setEnabled(False)  # 默认禁用
        layout.addWidget(self.export_button)

        # 显示结果
        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        layout.addWidget(self.result_text_edit)

        self.setLayout(layout)

    def calculate(self):
        try:
            # 获取用户输入
            principal = float(self.principal_edit.text())
            annual_interest_rate = float(self.rate_edit.text())
            months = int(self.months_edit.text())

            # 初始化变量
            monthly_interest_rate = annual_interest_rate / 12
            monthly_payment = (principal * monthly_interest_rate * (1 + monthly_interest_rate) ** months) / (
                    (1 + monthly_interest_rate) ** months - 1)

            # 计算每期还款明细
            remaining_principal = principal
            total_interest = 0
            self.payment_details = []  # 保存每月明细

            for i in range(1, months + 1):
                interest = remaining_principal * monthly_interest_rate
                principal_payment = monthly_payment - interest
                remaining_principal -= principal_payment
                total_interest += interest

                self.payment_details.append({
                    '期数': i,
                    '每月还款额': monthly_payment,
                    '本金': principal_payment,
                    '利息': interest,
                    '剩余本金': max(remaining_principal, 0)
                })

            # 显示结果
            result = f"每月还款额为：{monthly_payment:.2f}元\n总支付利息为：{total_interest:.2f}元\n"
            result += "还款明细（部分显示）：\n"
            for detail in self.payment_details[:10]:  # 仅显示前10期
                result += (f"第{detail['期数']}期：还款额 {detail['每月还款额']:.2f} 元，"
                           f"本金 {detail['本金']:.2f} 元，利息 {detail['利息']:.2f} 元，"
                           f"剩余本金 {detail['剩余本金']:.2f} 元\n")

            self.result_text_edit.setText(result)
            self.export_button.setEnabled(True)  # 启用导出按钮

        except ValueError:
            self.result_text_edit.setText("请输入有效的数字")
            self.export_button.setEnabled(False)

    def export_to_excel(self):
        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(self, "导出Excel文件", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        # 创建Excel文件并写入数据
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()

        # 写入表头
        headers = ['期数', '每月还款额', '本金', '利息', '剩余本金']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # 写入每期数据
        for row, detail in enumerate(self.payment_details, start=1):
            worksheet.write(row, 0, detail['期数'])
            worksheet.write(row, 1, detail['每月还款额'])
            worksheet.write(row, 2, detail['本金'])
            worksheet.write(row, 3, detail['利息'])
            worksheet.write(row, 4, detail['剩余本金'])

        workbook.close()
        self.result_text_edit.append(f"\nExcel文件已导出到：{file_path}")


def main():
    app = QApplication(sys.argv)
    ex = MortgageCalculator()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
