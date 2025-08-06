# 离线安装指南

## 📋 概述

本指南帮助您在离线环境下安装和运行 xzx 数据采集平台。

## 🚀 快速开始

### 步骤1：在联网环境下载依赖

在联网的电脑上运行以下命令：

```bash
# 下载所有依赖包
pip download --platform win_amd64 --python-version 3.11 --only-binary=:all: -r requirements_core.txt -d ./pkgs
```

**参数说明**：
- `--platform win_amd64`: 目标平台（Windows 64位）
- `--python-version 3.11`: Python版本
- `--only-binary=:all:`: 只下载二进制包
- `-r requirements_core.txt`: 使用核心依赖文件
- `-d ./pkgs`: 下载到pkgs目录

### 步骤2：复制项目到离线环境

将整个项目文件夹复制到离线电脑，确保包含：
- 所有Python源代码文件
- `pkgs/` 目录（包含所有依赖包）
- `requirements_core.txt` 文件

### 步骤3：在离线环境安装

在离线电脑上运行：

```bash
# 安装所有依赖
pip install --no-index --find-links=./pkgs -r requirements_core.txt
```

### 步骤4：启动应用

```bash
# 启动应用
streamlit run main.py
```

## 📦 依赖文件说明

### requirements_core.txt
包含项目运行所需的核心依赖集：
- **核心依赖**: streamlit, pandas, requests, openpyxl
- **数据处理**: numpy, python-dateutil, pytz
- **网络依赖**: urllib3, certifi, charset-normalizer, idna
- **类型提示**: typing-extensions
- **Streamlit相关**: altair, blinker, click等
- **其他工具**: 各种支持库

### requirements.txt
包含基础依赖，适合在线环境安装。

### requirements_minimal.txt
包含更多依赖，但可能包含平台特定的包。

## 🔧 平台特定说明

### Windows 环境
```bash
# 下载Windows依赖
pip download --platform win_amd64 --python-version 3.11 --only-binary=:all: -r requirements_core.txt -d ./pkgs

# 安装
pip install --no-index --find-links=./pkgs -r requirements_core.txt
```

### macOS 环境
```bash
# 下载macOS依赖
pip download --platform macosx_10_9_x86_64 --python-version 3.11 --only-binary=:all: -r requirements_core.txt -d ./pkgs

# 安装
pip install --no-index --find-links=./pkgs -r requirements_core.txt
```

### Linux 环境
```bash
# 下载Linux依赖
pip download --platform linux_x86_64 --python-version 3.11 --only-binary=:all: -r requirements_core.txt -d ./pkgs

# 安装
pip install --no-index --find-links=./pkgs -r requirements_core.txt
```

## 🐛 常见问题

### 1. 依赖下载失败
**问题**: 某些包无法下载
**解决**: 
- 检查网络连接
- 尝试使用国内镜像：`pip download -i https://pypi.tuna.tsinghua.edu.cn/simple ...`
- 手动下载缺失的包
- 使用 `requirements_core.txt` 而不是 `requirements_minimal.txt`

### 2. 安装时版本冲突
**问题**: 包版本不兼容
**解决**:
- 使用虚拟环境：`python -m venv venv`
- 激活环境：`source venv/bin/activate` (Linux/macOS) 或 `venv\Scripts\activate` (Windows)
- 重新安装依赖

### 3. Python版本不匹配
**问题**: Python版本与下载的包不兼容
**解决**:
- 确保使用Python 3.11
- 检查下载时的 `--python-version` 参数

### 4. 平台架构不匹配
**问题**: 下载的包与目标平台不匹配
**解决**:
- 确保下载时使用正确的 `--platform` 参数
- 检查目标平台的架构（32位/64位）

### 5. 特定包不可用
**问题**: 某些包在特定平台下不可用
**解决**:
- 使用 `requirements_core.txt` 而不是 `requirements_minimal.txt`
- 移除平台特定的包（如macOS的pyobjc包）
- 使用更兼容的版本

## 📊 依赖统计

### 核心依赖（4个）
- streamlit==1.47.0
- pandas==2.2.3
- requests==2.32.3
- openpyxl==3.1.5

### 总依赖数量
- 核心依赖：约70个包
- 最小化依赖：约80个包
- 完整依赖：约110个包

### 下载大小
- 预计下载大小：约400MB-800MB
- 安装后大小：约1.5-2.5GB

## 🔍 验证安装

安装完成后，运行以下命令验证：

```bash
# 检查核心依赖
python -c "import streamlit, pandas, requests, openpyxl; print('✅ 核心依赖安装成功')"

# 启动应用
streamlit run main.py
```

## 📞 技术支持

如果遇到问题，请检查：
1. Python版本是否为3.11
2. 是否使用了正确的requirements文件（推荐使用 `requirements_core.txt`）
3. pkgs目录是否包含所有依赖包
4. 网络环境是否正常（下载时）

---

**最后更新**: 2024年  
**适用版本**: V2.0 