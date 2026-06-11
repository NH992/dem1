@echo off
chcp 65001 >nul
echo 正在启动AI计算器（脱裤子放屁版）...
echo.

REM 检查是否已安装Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

REM 询问运行哪个版本
echo.
echo 请选择要运行的版本：
echo 1. 基础版 (ai_calculator.py)
echo 2. 改进版 (ai_calculator_improved.py)
set /p choice=请输入选择 (1 或 2):

if "%choice%"=="1" (
    echo 启动基础版AI计算器...
    python ai_calculator.py
) else if "%choice%"=="2" (
    echo 启动改进版AI计算器...
    python ai_calculator_improved.py
) else (
    echo 启动基础版AI计算器...
    python ai_calculator.py
)

pause