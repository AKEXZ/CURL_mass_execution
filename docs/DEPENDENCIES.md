# 项目依赖分析

## 📋 核心依赖

### 必需依赖
| 库名 | 版本 | 用途 | 使用位置 |
|------|------|------|----------|
| `streamlit` | >=1.28.0 | Web应用框架 | 所有页面 |
| `pandas` | >=2.0.0 | 数据处理 | utils.py |
| `requests` | >=2.31.0 | HTTP请求 | curl_runner.py |
| `openpyxl` | >=3.1.0 | Excel文件处理 | utils.py |

### 数据处理
| 库名 | 版本 | 用途 | 使用位置 |
|------|------|------|----------|
| `numpy` | >=1.24.0 | 数值计算 | pandas依赖 |
| `python-dateutil` | >=2.8.0 | 日期处理 | pandas依赖 |
| `pytz` | >=2023.3 | 时区处理 | pandas依赖 |

### 网络和HTTP
| 库名 | 版本 | 用途 | 使用位置 |
|------|------|------|----------|
| `urllib3` | >=2.0.0 | HTTP客户端 | requests依赖 |
| `certifi` | >=2023.7.0 | SSL证书 | requests依赖 |
| `charset-normalizer` | >=3.2.0 | 字符编码 | requests依赖 |
| `idna` | >=3.4 | 国际化域名 | requests依赖 |

### 类型提示
| 库名 | 版本 | 用途 | 使用位置 |
|------|------|------|----------|
| `typing-extensions` | >=4.7.0 | 类型提示扩展 | 所有文件 |

## 🔧 内置库

### Python标准库
| 库名 | 用途 | 使用位置 |
|------|------|----------|
| `sqlite3` | 数据库 | models.py |
| `json` | JSON处理 | 所有文件 |
| `re` | 正则表达式 | curl_runner.py |
| `threading` | 多线程 | curl_runner.py |
| `time` | 时间处理 | curl_runner.py |
| `queue` | 队列 | curl_runner.py |
| `dataclasses` | 数据类 | curl_runner.py, models.py |
| `typing` | 类型提示 | curl_runner.py, models.py |
| `urllib.parse` | URL解析 | curl_runner.py |
| `shlex` | 命令行解析 | curl_runner.py |
| `io` | 输入输出 | utils.py |

## 🚀 可选依赖

### 增强功能
| 库名 | 版本 | 用途 | 状态 |
|------|------|------|------|
| `beautifulsoup4` | >=4.12.0 | 网页解析 | 可选 |
| `selenium` | >=4.15.0 | 浏览器自动化 | 可选 |
| `lxml` | >=4.9.0 | XML/HTML解析器 | 可选 |

### 开发工具
| 库名 | 版本 | 用途 | 状态 |
|------|------|------|------|
| `watchdog` | >=3.0.0 | 文件监控 | 可选 |

## 📊 依赖关系图

```
streamlit (Web框架)
├── pandas (数据处理)
│   ├── numpy (数值计算)
│   ├── python-dateutil (日期处理)
│   └── pytz (时区处理)
├── requests (HTTP请求)
│   ├── urllib3 (HTTP客户端)
│   ├── certifi (SSL证书)
│   ├── charset-normalizer (字符编码)
│   └── idna (国际化域名)
└── openpyxl (Excel处理)

内置库
├── sqlite3 (数据库)
├── json (JSON处理)
├── re (正则表达式)
├── threading (多线程)
├── time (时间处理)
├── queue (队列)
├── dataclasses (数据类)
├── typing (类型提示)
├── urllib.parse (URL解析)
├── shlex (命令行解析)
└── io (输入输出)
```

## 🛠️ 安装说明

### 最小安装（必需依赖）
```bash
pip install streamlit>=1.28.0 pandas>=2.0.0 requests>=2.31.0 openpyxl>=3.1.0
```

### 完整安装（包含可选依赖）
```bash
pip install -r requirements.txt
```

### 开发环境安装
```bash
pip install -r requirements.txt
pip install watchdog>=3.0.0  # 文件监控
```

## 🔍 依赖检查

### 检查缺失依赖
```bash
python -c "
import sys
required = ['streamlit', 'pandas', 'requests', 'openpyxl']
missing = []
for module in required:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        missing.append(module)
        print(f'❌ {module}')
if missing:
    print(f'\n缺失依赖: {missing}')
    print('请运行: pip install -r requirements.txt')
else:
    print('\n✅ 所有依赖已安装')
"
```

## 📝 版本兼容性

### Python版本
- **最低版本**: Python 3.8
- **推荐版本**: Python 3.9+
- **测试版本**: Python 3.11

### 操作系统
- ✅ macOS (推荐)
- ✅ Windows
- ✅ Linux

## 🔄 更新依赖

### 更新所有依赖
```bash
pip install --upgrade -r requirements.txt
```

### 更新特定依赖
```bash
pip install --upgrade streamlit pandas requests openpyxl
```

## 🐛 常见问题

### 1. 依赖冲突
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 权限问题
```bash
# 使用用户安装
pip install --user -r requirements.txt
```

### 3. 网络问题
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
``` 