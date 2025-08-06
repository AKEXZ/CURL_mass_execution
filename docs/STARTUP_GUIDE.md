# 启动脚本使用指南

## 📋 概述

项目提供了多种启动方式，适应不同操作系统和用户偏好。

## 🚀 启动脚本列表

| 脚本文件 | 适用系统 | 特点 | 推荐度 |
|----------|----------|------|--------|
| `start_windows.bat` | Windows | PowerShell包装器，彩色界面 | ⭐⭐⭐⭐⭐ |
| `start.ps1` | Windows | PowerShell脚本，最佳体验 | ⭐⭐⭐⭐⭐ |
| `start.bat` | Windows | 传统批处理脚本 | ⭐⭐⭐ |
| `start.sh` | Linux/macOS | Shell脚本，彩色输出 | ⭐⭐⭐⭐⭐ |
| `start.py` | 跨平台 | Python脚本，功能完整 | ⭐⭐⭐⭐ |

## 🪟 Windows 用户

### 使用 start_windows.bat（推荐）

#### 双击运行
1. 在文件资源管理器中找到 `start_windows.bat`
2. 双击运行
3. 脚本会自动检测并使用PowerShell或传统批处理模式

#### 命令行运行
```cmd
# 在项目根目录打开命令提示符
cd C:\path\to\xzx
start_windows.bat
```

#### 功能特点
- ✅ 自动检测PowerShell可用性
- ✅ 彩色输出界面
- ✅ 自动检查Python安装
- ✅ 自动检查依赖
- ✅ 交互式依赖安装
- ✅ 错误处理和提示
- ✅ 中文界面支持
- ✅ 信号处理（Ctrl+C）

### 使用 start.ps1（最佳体验）

#### 右键运行
1. 在文件资源管理器中找到 `start.ps1`
2. 右键选择"使用PowerShell运行"

#### 命令行运行
```powershell
# 在项目根目录打开PowerShell
cd C:\path\to\xzx
.\start.ps1
```

#### 功能特点
- ✅ 彩色输出界面
- ✅ 自动检查Python安装
- ✅ 自动检查依赖
- ✅ 交互式依赖安装
- ✅ 错误处理和提示
- ✅ 中文界面支持
- ✅ 信号处理（Ctrl+C）
- ✅ 更好的用户体验

### 使用 start.bat（备用方案）

#### 双击运行
1. 在文件资源管理器中找到 `start.bat`
2. 双击运行
3. 如果依赖未安装，脚本会提示安装

#### 命令行运行
```cmd
# 在项目根目录打开命令提示符
cd C:\path\to\xzx
start.bat
```

#### 功能特点
- ✅ 自动检查Python安装
- ✅ 自动检查依赖
- ✅ 交互式依赖安装
- ✅ 错误处理和提示
- ✅ 中文界面支持

## 🐧 Linux/macOS 用户

### 使用 start.sh（推荐）

#### 运行脚本
```bash
# 在项目根目录
./start.sh

# 或使用bash运行
bash start.sh
```

#### 功能特点
- ✅ 彩色输出界面
- ✅ 自动检查Python3
- ✅ 自动检查依赖
- ✅ 交互式依赖安装
- ✅ 信号处理（Ctrl+C）
- ✅ 错误处理和提示

## 🐍 Python 脚本

### 使用 start.py

```bash
# 运行Python启动脚本
python3 start.py
```

#### 功能特点
- ✅ 跨平台兼容
- ✅ 详细的依赖检查
- ✅ 完整的错误处理
- ✅ 可扩展性强

## 🔧 直接启动

### 使用 streamlit 命令

```bash
# 启动主应用
streamlit run app.py

# 或启动主程序
streamlit run src/main.py
```

### 生产环境启动

```bash
# 指定端口和地址
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# 禁用浏览器自动打开
streamlit run app.py --server.headless true
```

## 📊 启动脚本对比

| 特性 | start_windows.bat | start.ps1 | start.bat | start.sh | start.py |
|------|-------------------|-----------|-----------|----------|----------|
| 操作系统 | Windows | Windows | Windows | Linux/macOS | 跨平台 |
| 用户界面 | 彩色命令行 | 彩色命令行 | 命令行 | 彩色命令行 | 命令行 |
| 依赖检查 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 自动安装 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 错误处理 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 信号处理 | ✅ | ✅ | ❌ | ✅ | ✅ |
| 中文支持 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 双击运行 | ✅ | ❌ | ✅ | ❌ | ❌ |
| PowerShell | 自动检测 | 原生 | 不支持 | 不支持 | 不支持 |

## 🐛 常见问题

### 1. 权限问题（Linux/macOS）
```bash
# 设置执行权限
chmod +x start.sh

# 或使用bash运行
bash start.sh
```

### 2. 编码问题（Windows）
```cmd
# 如果出现中文乱码，确保使用UTF-8编码
chcp 65001
start.bat
```

### 3. Python路径问题
```bash
# 检查Python安装
python --version
python3 --version

# 如果只有python3，修改脚本中的python为python3
```

### 4. 依赖安装失败
```bash
# 手动安装依赖
pip install -r config/requirements_core.txt

# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r config/requirements_core.txt
```

### 5. 端口被占用
```bash
# 使用不同端口启动
streamlit run app.py --server.port 8502
```

## 📝 自定义启动

### 修改端口
编辑启动脚本，修改 `--server.port` 参数：
```bash
# 在start.sh中修改
python3 -m streamlit run app.py --server.port 8502 --server.address localhost
```

### 修改地址
```bash
# 允许外部访问
python3 -m streamlit run app.py --server.address 0.0.0.0
```

### 禁用浏览器自动打开
```bash
# 添加参数
python3 -m streamlit run app.py --server.headless true
```

## 🔍 调试模式

### 启用详细日志
```bash
# 使用详细模式启动
streamlit run app.py --logger.level debug
```

### 检查启动日志
```bash
# 查看启动过程中的详细信息
streamlit run app.py --server.headless true 2>&1 | tee startup.log
```

## 📞 技术支持

如果遇到启动问题：

1. **检查Python版本**: 确保使用Python 3.8+
2. **检查依赖**: 运行 `pip list` 查看已安装的包
3. **检查端口**: 确保8501端口未被占用
4. **查看日志**: 检查启动过程中的错误信息
5. **重启系统**: 有时重启可以解决环境问题

---

**最后更新**: 2024年  
**适用版本**: V2.0