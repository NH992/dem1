import sys
import subprocess
import time
import pyautogui
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import win32gui
import win32con
import win32process


class AICalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI计算器")
        self.setGeometry(300, 300, 300, 400)
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # 显示标签
        self.title_label = QLabel("AI计算器（脱裤子放屁版）")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.title_label)
        
        # 输入框
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入计算表达式，如: 5+3")
        layout.addWidget(self.input_field)
        
        # 结果显示
        self.result_label = QLabel("结果将显示在这里...")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("border: 1px solid gray; padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(self.result_label)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.calculate_button = QPushButton("计算 (=)")
        self.calculate_button.clicked.connect(self.perform_calculation)
        button_layout.addWidget(self.calculate_button)
        
        self.clear_button = QPushButton("清空")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # 添加说明标签
        self.info_label = QLabel("提示：本计算器会调用系统计算器进行计算\n(此为幽默项目，实际效率低于直接使用计算器)")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 10px; color: gray;")
        layout.addWidget(self.info_label)
        
        central_widget.setLayout(layout)
        
        # 存储计算器进程信息
        self.calc_process = None

    def perform_calculation(self):
        """执行计算：调用系统计算器并自动化输入输出"""
        expression = self.input_field.text().strip()
        if not expression:
            self.result_label.setText("请输入计算表达式")
            return
            
        # 验证表达式是否只包含数字和运算符
        if not re.match(r'^[0-9+\-*/(). ]+$', expression):
            self.result_label.setText("仅支持数字和 + - * / ( ) 运算符")
            return
        
        # 更新UI状态
        self.result_label.setText("正在调用系统计算器...")
        QApplication.processEvents()  # 立即更新UI
        
        try:
            # 启动Windows计算器
            self.calc_process = subprocess.Popen('calc.exe')
            
            # 等待计算器启动
            time.sleep(2)
            
            # 获取计算器窗口句柄并前置
            calc_hwnd = self.find_calculator_window()
            if calc_hwnd:
                win32gui.SetForegroundWindow(calc_hwnd)
                time.sleep(0.5)
                
                # 清除计算器内容（按C键或Escape键）
                pyautogui.press('esc')
                time.sleep(0.2)
                
                # 输入表达式
                self.type_expression(expression)
                
                # 按下等号得到结果
                pyautogui.press('=')
                time.sleep(1)  # 给计算器更多时间处理
                
                # 提示用户计算已完成
                self.result_label.setText("计算完成！请查看系统计算器结果")
                
                # 保持计算器窗口一段时间让用户可以看到计算过程
                time.sleep(3)
                
                # 关闭计算器
                if calc_hwnd:
                    win32gui.PostMessage(calc_hwnd, win32con.WM_CLOSE, 0, 0)
                
            else:
                self.result_label.setText("无法找到计算器窗口")
                
        except Exception as e:
            self.result_label.setText(f"计算出错: {str(e)}")

    def find_calculator_window(self):
        """查找计算器窗口"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if "计算器" in window_title or "Calculator" in window_title:
                    windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        for hwnd in windows:
            window_title = win32gui.GetWindowText(hwnd)
            if "计算器" in window_title or "Calculator" in window_title:
                return hwnd
        return None

    def type_expression(self, expression):
        """向计算器输入表达式"""
        # 处理表达式，将其转换为计算器可识别的按键序列
        expression = expression.replace(" ", "")
        
        for char in expression:
            if char.isdigit():  # 数字
                pyautogui.press(char)
            elif char == '+':
                pyautogui.press('add')
            elif char == '-':
                pyautogui.press('subtract')
            elif char == '*':  # 乘法
                pyautogui.press('*')  # 标准键盘乘法键
            elif char == '/':  # 除法
                pyautogui.press('/')  # 标准键盘除法键
            elif char == '(':  # 左括号
                pyautogui.press('(')
            elif char == ')':  # 右括号
                pyautogui.press(')')
            time.sleep(0.1)  # 短暂延迟确保计算器能跟上输入速度

    def clear_all(self):
        """清空输入和结果"""
        self.input_field.clear()
        self.result_label.setText("结果将显示在这里...")


def main():
    app = QApplication(sys.argv)
    calculator = AICalculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()