# AI计算器启动指南

## 启动前准备

1. 确保已安装Python 3.7或更高版本
2. 将Python添加到系统PATH环境变量中

## 启动方法

### 方法一：使用批处理文件（推荐）
双击运行 `run_calculator.bat` 文件

### 方法二：使用Python脚本
打开命令提示符，切换到项目目录，运行：
```bash
python install_and_run.py
```

### 方法三：使用简化启动脚本
如果上述方法出现问题，可以尝试：
```bash
python simple_start.py
```

## 常见问题

1. 如果提示找不到Python，请确认Python已正确安装并添加到环境变量中
2. 如果依赖安装失败，可能是网络问题，脚本会自动尝试使用国内镜像源
3. 如果仍有问题，可手动安装依赖：
   ```
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

## 程序功能

这是一个AI计算器，可以自动识别屏幕上的数学表达式并计算结果。