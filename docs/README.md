# xzx 数据采集平台

## 🚀 主要功能

### 核心功能
- **🔄 API批量请求工具**: 支持curl解析、参数批量替换、多线程执行、文件下载
- **⚙️ JSON结构管理**: 自定义和管理API响应的JSON结构模式
- **📚 帮助中心**: 交互式使用指南和示例
- **📥 JSON转Excel工具**: 数据格式转换和导出

### 新增功能
- **🗄️ 数据库驱动**: SQLite数据库存储JSON结构模式
- **🔍 自动检测**: 智能识别API响应的JSON结构
- **⚡ 快速选择**: 一键选择合适的导出路径
- **🧪 测试验证**: 内置测试功能验证结构正确性

## 📋 环境要求

- **Python版本**: 3.8+ (推荐 3.9+)
- **操作系统**: macOS (推荐), Windows, Linux
- **内存**: 建议 4GB+
- **存储**: 建议 2GB+ 可用空间

## 🛠️ 依赖安装

### 在线环境安装
```bash
# 克隆项目
git clone <repository-url>
cd xzx

# 安装依赖
pip install -r requirements.txt

# 启动项目
streamlit run main.py
```

### 离线环境安装（推荐方案）

#### 方案一：使用预打包依赖（推荐）
1. **下载预打包依赖**:
   ```bash
   # 在联网环境下运行
   python3 download_dependencies.py
   ```

2. **复制到离线环境**:
   - 将整个项目文件夹复制到离线电脑
   - 确保包含 `pkgs/` 目录

3. **在离线环境安装**:
   ```bash
   # Linux/macOS
   bash install_offline.sh
   
   # Windows
   install_offline.bat
   ```

#### 方案二：手动下载依赖
1. **在联网电脑上下载依赖包**:
   ```bash
   pip download --platform win_amd64 --python-version 3.11 --only-binary=:all: -r requirements_core.txt -d ./pkgs
   ```
   > 注意：在 Mac 上为 Windows 10 64位、Python 3.11.9 下载依赖，务必加上 `--platform win_amd64 --python-version 3.11` 参数。

2. **将整个 `xzx` 文件夹拷贝到离线电脑**

3. **在离线电脑上安装**:
   ```bash
   pip install --no-index --find-links=./pkgs -r requirements_core.txt
   ```

## 📦 核心依赖

### 必需依赖
- `streamlit==1.47.0` - Web应用框架
- `pandas==2.2.3` - 数据处理
- `requests==2.32.3` - HTTP请求
- `openpyxl==3.1.5` - Excel文件处理

### 可选依赖
- `beautifulsoup4==4.13.4` - 网页解析
- `selenium==4.33.0` - 浏览器自动化
- `lxml==5.3.0` - XML/HTML解析器
- `watchdog==6.0.0` - 文件监控

## 🚀 快速开始

1. **启动应用**:
   ```bash
   streamlit run main.py
   ```

2. **访问功能**:
   - 在侧边栏选择需要的功能模块
   - 按照界面提示操作

3. **JSON结构管理**:
   - 选择"⚙️ JSON结构管理"添加自定义结构
   - 选择"📚 帮助中心"查看详细使用指南

## 📁 项目结构

```
xzx/
├── main.py                    # 主程序入口
├── curl_runner.py             # API批量请求工具
├── models.py                  # 数据库模型
├── json_structure_manager.py  # JSON结构管理
├── help_page.py              # 帮助中心
├── utils.py                  # 工具函数
├── lineloss_collector.py     # 线损收集器
├── header_collector.py       # 网页信息采集
├── requirements.txt          # 基础依赖列表
├── requirements_core.txt     # 核心依赖列表（离线用，推荐）
├── requirements_minimal.txt  # 最小化依赖列表
├── OFFLINE_INSTALL.md       # 离线安装指南
├── DEPENDENCIES.md          # 依赖分析文档
├── json_structures.db        # SQLite数据库
└── pkgs/                    # 离线依赖包
```

## 🔧 功能说明

### API批量请求工具
- 支持curl命令解析
- 参数批量替换
- 多线程并发执行
- 自动JSON结构检测
- Excel数据导出

### JSON结构管理
- 自定义JSON结构模式
- 数据库存储和管理
- 自动结构检测
- 测试验证功能

### 帮助中心
- 交互式使用指南
- 示例演示
- 常见问题解答
- 实时测试功能

## 📝 使用示例

### 添加自定义JSON结构
1. 选择"⚙️ JSON结构管理"
2. 在侧边栏填写结构信息
3. 点击"添加结构"
4. 使用测试功能验证

### API批量请求
1. 选择"🔄 API批量请求工具"
2. 粘贴curl命令
3. 选择要替换的参数
4. 输入批量值
5. 开始执行

## 🐛 常见问题

### 依赖安装失败
```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 数据库错误
- 检查 `json_structures.db` 文件权限
- 确保有写入权限
- 重新初始化数据库

### 网络问题
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 离线安装问题
1. **确保依赖包完整**: 检查 `pkgs/` 目录是否包含所有 `.whl` 文件
2. **检查Python版本**: 确保使用Python 3.11
3. **使用正确的requirements文件**: 离线环境推荐使用 `requirements_core.txt`

## 📞 技术支持

如有问题请联系开发者。

---

**版本**: V2.0  
**更新日期**: 2024年  
**许可证**: MIT