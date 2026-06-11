import subprocess
import sys
import os

print("检查Python环境...")

# 检查是否已安装必要的库
required_packages = ['pyautogui', 'pytesseract', 'Pillow', 'PyQt5', 'pywin32']

missing_packages = []
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f"发现缺失的包: {', '.join(missing_packages)}")
    print("正在安装缺失的包...")
    
    # 使用国内镜像源安装包，避免网络问题
    pip_cmd = [sys.executable, "-m", "pip", "install"]
    pip_cmd.extend(missing_packages)
    pip_cmd.extend(["-i", "https://pypi.tuna.tsinghua.edu.cn/simple/"])
    
    try:
        subprocess.check_call(pip_cmd)
        print("所有依赖包安装完成！")
    except subprocess.CalledProcessError:
        print("依赖包安装失败，尝试使用默认源安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("依赖包安装完成！")
        except subprocess.CalledProcessError:
            print("依赖包安装失败，请检查网络连接或手动安装")
            input("按任意键退出...")
            exit()

else:
    print("所有依赖包已安装")

print("正在启动AI计算器...")
try:
    subprocess.check_call([sys.executable, "ai_calculator.py"])
except subprocess.CalledProcessError:
    print("启动AI计算器失败")
    input("按任意键退出...")

input("程序结束，按任意键退出...")