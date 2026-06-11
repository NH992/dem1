@echo off
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
pip install -r requirements.txt

REM 运行AI计算器
echo.
echo 启动AI计算器...
python ai_calculator.py

pause