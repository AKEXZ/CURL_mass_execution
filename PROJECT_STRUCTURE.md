# 项目结构说明

## �� 目录结构

```
xzx/
├── 📖 README.md               # 项目主要说明
├── 📋 PROJECT_STRUCTURE.md    # 项目结构说明
├── 🚀 start.py                # Python启动脚本
├── 🪟 start.bat               # Windows批处理启动脚本
├── 🪟 start_windows.bat       # Windows PowerShell启动器（推荐）
├── 🪟 start.ps1               # PowerShell启动脚本
└── 🐧 start.sh                # Linux/macOS Shell启动脚本
├── app.py                    # 🚀 主程序入口
├── src/                      # 📦 源代码目录
│   ├── main.py              # 🎯 主程序逻辑
│   ├── core/                # ⚙️ 核心功能模块
│   │   ├── curl_runner.py   # 🔄 API批量请求工具
│   │   ├── json_structure_manager.py  # 📊 JSON结构管理
│   │   └── help_page.py     # 📚 帮助中心
│   ├── utils/               # 🔧 工具函数
│   │   └── utils.py         # 📋 通用工具函数
│   └── models/              # 🗄️ 数据模型
│       └── models.py        # 💾 数据库模型
├── config/                  # ⚙️ 配置文件
│   ├── requirements.txt     # 📋 基础依赖列表
│   ├── requirements_core.txt # ⭐ 核心依赖列表（推荐）
│   └── requirements_minimal.txt # 📦 最小化依赖列表
├── docs/                    # 📚 文档目录
│   ├── README.md           # 📖 项目说明
│   ├── OFFLINE_INSTALL.md  # 🔌 离线安装指南
│   ├── DEPENDENCIES.md     # 📊 依赖分析文档
│   ├── guides/             # 📖 使用指南
│   └── api/                # 🔌 API文档
├── data/                    # 💾 数据目录
│   └── json_structures.db  # 🗄️ SQLite数据库
└── pkgs/                    # 📦 离线依赖包
```

## 🔍 详细说明

### 🚀 根目录文件
- **`app.py`**: 主程序入口，负责启动Streamlit应用
- **`README.md`**: 项目主要说明文档

### 📦 src/ 源代码目录
- **`main.py`**: 主程序逻辑，包含所有功能模块的集成
- **`core/`**: 核心功能模块
  - `curl_runner.py`: API批量请求工具，支持curl解析和多线程执行
  - `json_structure_manager.py`: JSON结构管理，自定义和管理API响应结构
  - `help_page.py`: 帮助中心，提供交互式使用指南
- **`utils/`**: 工具函数
  - `utils.py`: 通用工具函数，包含JSON处理和Excel导出功能
- **`models/`**: 数据模型
  - `models.py`: 数据库模型，定义JsonStructure和JsonStructureDB类

### ⚙️ config/ 配置文件
- **`requirements_core.txt`**: 核心依赖列表（推荐使用）
- **`requirements_minimal.txt`**: 最小化依赖列表
- **`requirements_offline.txt`**: 离线依赖列表
- **`requirements.txt`**: 基础依赖列表

### 📚 docs/ 文档目录
- **`README.md`**: 项目详细说明
- **`OFFLINE_INSTALL.md`**: 离线安装指南
- **`DEPENDENCIES.md`**: 依赖分析文档
- **`guides/`**: 使用指南目录
- **`api/`**: API文档目录

### 💾 data/ 数据目录
- **`json_structures.db`**: SQLite数据库，存储JSON结构模式

### 📦 pkgs/ 离线依赖包
- 包含所有离线安装所需的Python包文件

## 🔧 模块依赖关系

```
app.py
└── src/main.py
    ├── src/core/curl_runner.py
    │   ├── src/utils/utils.py
    │   └── src/models/models.py
    ├── src/core/json_structure_manager.py
    │   └── src/models/models.py
    └── src/core/help_page.py
        └── src/models/models.py
```

## 🎯 功能模块说明

### 核心功能 (core/)
- **API批量请求工具**: 解析curl命令，支持参数批量替换和多线程执行
- **JSON结构管理**: 自定义和管理API响应的JSON结构模式
- **帮助中心**: 提供交互式使用指南和示例

### 工具函数 (utils/)
- **JSON处理**: 解析和操作JSON数据
- **Excel导出**: 将数据导出为Excel格式
- **路径处理**: 处理嵌套JSON路径

### 数据模型 (models/)
- **JsonStructure**: JSON结构数据类
- **JsonStructureDB**: 数据库操作类，提供CRUD功能

## 📋 启动方式

### 🪟 Windows 用户
```bash
# 推荐：PowerShell启动脚本（彩色界面，更好的用户体验）
start_windows.bat

# 或直接使用PowerShell脚本
start.ps1

# 传统批处理脚本（如果PowerShell不可用）
start.bat
```

### 🐧 Linux/macOS 用户
```bash
# 运行shell脚本（推荐）
./start.sh

# 或使用bash运行
bash start.sh
```

### 🐍 Python 脚本
```bash
# 运行Python启动脚本
python3 start.py
```

### 🔧 直接启动
```bash
# 启动应用
streamlit run app.py

# 或启动主程序
streamlit run src/main.py
```

### 🚀 生产环境
```bash
# 使用配置文件
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🔄 文件迁移说明

### 已完成的迁移
- ✅ 所有Python源代码文件已移动到 `src/` 目录
- ✅ 配置文件已移动到 `config/` 目录
- ✅ 文档文件已移动到 `docs/` 目录
- ✅ 数据库文件已移动到 `data/` 目录
- ✅ 导入路径已更新以适应新的目录结构

### 导入路径更新
- `from utils import ...` → `from src.utils.utils import ...`
- `from models import ...` → `from src.models.models import ...`
- `from curl_runner import ...` → `from src.core.curl_runner import ...`

## 🚀 部署说明

### 本地开发
1. 克隆项目到本地
2. 安装依赖：`pip install -r config/requirements_core.txt`
3. 启动应用：`streamlit run app.py`

### 离线部署
1. 下载依赖包到 `pkgs/` 目录
2. 复制整个项目到离线环境
3. 安装依赖：`pip install --no-index --find-links=./pkgs -r config/requirements_core.txt`
4. 启动应用：`streamlit run app.py`

---

**最后更新**: 2024年  
**版本**: V2.0 