import subprocess
import sys
import os


def install_requirements():
    """安装项目所需的依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖包安装成功！")
        return True
    except subprocess.CalledProcessError:
        print("依赖包安装失败，请检查网络连接或手动安装")
        return False


def run_calculator():
    """运行AI计算器"""
    print("正在启动AI计算器...")
    try:
        subprocess.check_call([sys.executable, "ai_calculator_improved.py"])
    except subprocess.CalledProcessError:
        print("程序运行失败")


def main():
    print("="*50)
    print("AI计算器（脱裤子放屁版）安装与运行工具")
    print("="*50)
    
    # 检查是否有requirements.txt文件
    if not os.path.exists("requirements.txt"):
        print("错误：找不到requirements.txt文件")
        input("按回车键退出...")
        return
    
    # 询问用户是否安装依赖
    response = input("是否安装依赖包？(y/n): ")
    if response.lower() == 'y' or response.lower() == 'yes':
        if install_requirements():
            print("\n依赖安装完成！")
        else:
            print("\n依赖安装失败，程序可能无法正常运行")
            input("按回车键退出...")
            return
    else:
        print("跳过依赖安装，请确保已手动安装所需依赖")
    
    # 询问是否立即运行程序
    response = input("\n是否立即运行AI计算器？(y/n): ")
    if response.lower() == 'y' or response.lower() == 'yes':
        run_calculator()
    
    print("\n感谢使用AI计算器（脱裤子放屁版）！")
    input("按回车键退出...")


if __name__ == "__main__":
    main()