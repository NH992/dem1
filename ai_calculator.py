import sys
import subprocess
import time
import pyautogui
import pytesseract
from PIL import ImageGrab
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import win32gui
import win32con


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
        layout.addWidget(self.title_label)
        
        # 输入框
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入计算表达式，如: 5+3")
        layout.addWidget(self.input_field)
        
        # 结果显示
        self.result_label = QLabel("结果将显示在这里...")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("border: 1px solid gray; padding: 10px;")
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
        self.info_label = QLabel("提示：本计算器会调用系统计算器进行计算")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        central_widget.setLayout(layout)
        
        # 初始化pytesseract路径（如果需要）
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        except:
            print("Tesseract未找到，请安装Tesseract-OCR以支持结果读取")

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
            subprocess.Popen('calc.exe')
            
            # 等待计算器启动
            time.sleep(2)
            
            # 获取计算器窗口句柄并前置
            calc_hwnd = self.find_calculator_window()
            if calc_hwnd:
                win32gui.SetForegroundWindow(calc_hwnd)
                time.sleep(0.5)
                
                # 清除计算器内容（按C键）
                pyautogui.press('c')
                
                # 将表达式转换为计算器可接受的格式并输入
                self.type_expression(expression)
                
                # 按下等号得到结果
                pyautogui.press('enter')  # 或者 '='
                time.sleep(0.5)
                
                # 尝试读取结果
                result = self.read_result_from_calculator()
                
                # 关闭计算器
                if calc_hwnd:
                    win32gui.PostMessage(calc_hwnd, win32con.WM_CLOSE, 0, 0)
                
                # 显示结果
                if result:
                    self.result_label.setText(f"AI计算结果: {result}")
                else:
                    self.result_label.setText("无法读取结果，可能需要安装OCR组件")
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
        # 移除空格并替换特殊字符
        expression = expression.replace(" ", "")
        expression = expression.replace("*", "x")  # 计算器可能使用x表示乘法
        
        for char in expression:
            if char == '+':
                pyautogui.press('add')
            elif char == '-':
                pyautogui.press('subtract')
            elif char == '*':
                pyautogui.press('multiply')  # 或者 'x'
            elif char == '/':
                pyautogui.press('divide')
            elif char == '(':
                pyautogui.press('left-parenthesis')
            elif char == ')':
                pyautogui.press('right-parenthesis')
            elif char == '=':
                pyautogui.press('enter')
            else:
                pyautogui.press(char)

    def read_result_from_calculator(self):
        """尝试从计算器窗口读取结果"""
        try:
            # 尝试截取屏幕区域来识别结果（这需要根据实际计算器界面调整坐标）
            # 这是一个简化的示例，实际可能需要更精确的定位
            screenshot = ImageGrab.grab()
            # 这里需要根据计算器窗口的位置和大小来裁剪图像
            # 由于不同版本计算器界面可能不同，这只是一个基础实现
            result_text = pytesseract.image_to_string(screenshot, lang='eng')
            
            # 查找数字模式
            numbers = re.findall(r'\d+\.?\d*', result_text)
            if numbers:
                return numbers[-1]  # 返回最后一个找到的数字（通常是结果）
        except:
            pass
        return None

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