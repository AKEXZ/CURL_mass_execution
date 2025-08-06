# 🔄 CURL Mass Execution - 数据采集与处理平台

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.47.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🚀 一个强大的基于Streamlit的数据采集与处理平台，支持CURL命令批量执行、JSON数据转换、结构化管理等功能。

## 📋 目录

- [✨ 功能特性](#-功能特性)
- [🎯 核心功能](#-核心功能)
- [🚀 快速开始](#-快速开始)
- [📦 安装说明](#-安装说明)
- [💡 使用指南](#-使用指南)
- [🔧 项目结构](#-项目结构)
- [📝 使用示例](#-使用示例)
- [🐛 常见问题](#-常见问题)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)

## ✨ 功能特性

- 🔄 **CURL批量执行**: 解析CURL命令，支持参数批量替换和多线程并发执行
- 📊 **JSON转Excel**: 智能JSON数据转换，支持自定义字段路径提取
- 🏗️ **结构化管理**: 自定义JSON结构模式，数据库存储和管理
- 📚 **帮助中心**: 交互式使用指南和实时测试功能
- ⚡ **高性能**: 多线程并发处理，支持大批量数据
- 🎨 **用户友好**: 现代化Web界面，操作简单直观
- 🔧 **离线支持**: 完整的离线安装包和依赖管理

## 🎯 核心功能

### 🔄 CURL批量执行工具
- **智能解析**: 自动解析CURL命令，提取URL、请求头、请求体等信息
- **参数替换**: 支持批量替换URL参数、请求体参数、请求头等
- **并发执行**: 多线程并发处理，可配置线程数和批处理大小
- **结果管理**: 实时显示执行结果，支持错误处理和重试机制
- **文件下载**: 自动下载响应文件，支持批量文件管理
- **数据导出**: 将API响应数据导出为Excel格式

### 📊 JSON转Excel工具
- **多格式支持**: 支持单个JSON对象、数组、多行JSON等格式
- **智能提取**: 支持自定义字段路径（如 `data.items`）提取数据
- **结构检测**: 自动检测JSON结构，推荐最佳导出路径
- **数据预览**: 提供数据结构分析和实时预览功能
- **批量处理**: 支持大量JSON数据的批量转换

### 🏗️ JSON结构管理
- **模式定义**: 自定义JSON结构模式，支持复杂嵌套结构
- **数据库存储**: SQLite数据库存储，支持结构版本管理
- **自动检测**: 基于历史数据的智能结构检测
- **测试验证**: 实时测试结构模式的有效性
- **批量导入**: 支持批量导入和导出结构模式

### 📚 帮助中心
- **交互式指南**: 详细的使用指南和操作说明
- **示例演示**: 丰富的示例代码和演示数据
- **实时测试**: 在线测试功能，验证操作效果
- **FAQ**: 常见问题解答和故障排除

## 🚀 快速开始

### 环境要求
- Python 3.11+
- Windows/Linux/macOS
- 4GB+ 内存（推荐8GB+）

### 一键启动（推荐）

#### Windows用户
```bash
# 下载并解压项目
git clone https://github.com/your-username/CURL_mass_execution.git
cd CURL_mass_execution

# 运行启动脚本
start_windows.bat
```

#### Linux/macOS用户
```bash
# 下载并解压项目
git clone https://github.com/your-username/CURL_mass_execution.git
cd CURL_mass_execution

# 运行启动脚本
chmod +x start.sh
./start.sh
```

### 手动安装
```bash
# 1. 克隆项目
git clone https://github.com/your-username/CURL_mass_execution.git
cd CURL_mass_execution

# 2. 安装依赖
pip install -r config/requirements_core.txt

# 3. 启动应用
streamlit run app.py
```

## 📦 安装说明

### 在线安装
```bash
# 使用pip安装核心依赖
pip install streamlit pandas requests openpyxl

# 或安装完整依赖
pip install -r config/requirements.txt
```

### 离线安装
项目提供了完整的离线安装包，包含所有依赖：

```bash
# Windows用户
1.python-3.11.9-amd64.exe  # Python安装包
2.install_quick.bat        # 快速安装脚本
3.install_packages.bat     # 完整安装脚本

# 运行安装脚本
2.install_quick.bat
```

### 依赖包说明
- **核心包**: 约20个，包含基本功能
- **完整包**: 约90个，包含所有功能
- **离线包大小**: 约200MB

## 💡 使用指南

### 1. CURL批量执行

#### 基本流程
1. 选择"🔄 API批量请求工具"
2. 粘贴CURL命令
3. 选择要替换的参数
4. 输入批量值（每行一个）
5. 配置执行参数（线程数、批处理大小等）
6. 点击"开始批量执行"

#### 示例CURL命令
```bash
curl 'https://api.example.com/data' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer your-token' \
  -d '{"param1":"value1","param2":"value2"}'
```

#### 参数替换示例
```
# 原始参数值
value1
value2
value3

# 系统会自动替换param1参数，执行3个请求
```

### 2. JSON转Excel

#### 基本流程
1. 选择"🔄 JSON转Excel工具"
2. 粘贴JSON数据
3. 选择导出字段路径（可选）
4. 点击"导出为Excel"

#### JSON数据示例
```json
{
  "data": [
    {"name": "张三", "age": 18, "score": 90},
    {"name": "李四", "age": 20, "score": 85}
  ]
}
```

#### 字段路径示例
- `data` - 导出data数组中的所有对象
- `data.items` - 如果data是对象，导出items数组
- 留空 - 导出全部数据

### 3. JSON结构管理

#### 添加结构模式
1. 选择"⚙️ JSON结构管理"
2. 填写结构名称和路径模式
3. 点击"添加结构"
4. 使用测试功能验证

#### 结构模式示例
- 名称: `用户列表`
- 路径: `data.users`
- 描述: `用户数据列表结构`

## 🔧 项目结构

```
CURL_mass_execution/
├── app.py                    # 主程序入口
├── src/                      # 源代码目录
│   ├── main.py              # 主程序逻辑
│   ├── core/                # 核心功能模块
│   │   ├── json_converter.py # JSON转Excel工具
│   │   ├── curl_runner.py   # CURL批量执行工具
│   │   ├── curl_parser.py   # CURL命令解析器
│   │   ├── batch_processor.py # 批量处理器
│   │   ├── request_processor.py # 请求处理器
│   │   ├── result_display.py # 结果显示器
│   │   ├── json_structure_manager.py # JSON结构管理
│   │   └── help_page.py     # 帮助中心
│   ├── utils/               # 工具函数
│   │   └── utils.py         # 通用工具函数
│   └── models/              # 数据模型
│       └── models.py        # 数据库模型
├── config/                  # 配置文件
│   ├── requirements.txt     # 完整依赖列表
│   ├── requirements_core.txt # 核心依赖列表
│   └── requirements_minimal.txt # 最小依赖列表
├── data/                    # 数据目录
│   └── json_structures.db  # SQLite数据库
├── docs/                    # 文档目录
├── pkgs/                    # 离线依赖包
├── start.py                 # Python启动脚本
├── start.sh                 # Linux/macOS启动脚本
├── start_windows.bat        # Windows启动脚本
└── README.md               # 项目说明
```

## 📝 使用示例

### 场景1: 批量获取用户数据
```bash
# 1. 准备CURL命令
curl 'https://api.example.com/users' \
  -H 'Authorization: Bearer token123' \
  -d '{"user_id":"123"}'

# 2. 批量替换user_id参数
123
456
789
101112

# 3. 执行批量请求，获取4个用户的数据
```

### 场景2: 数据格式转换
```json
// 输入JSON数据
{
  "result": {
    "items": [
      {"id": 1, "name": "产品A", "price": 100},
      {"id": 2, "name": "产品B", "price": 200}
    ]
  }
}

// 使用路径 "result.items" 导出Excel
// 得到包含id、name、price列的Excel文件
```

### 场景3: 复杂API响应处理
```json
// 复杂嵌套结构
{
  "status": "success",
  "data": {
    "page": 1,
    "total": 100,
    "items": [
      {
        "user": {"id": 1, "name": "张三"},
        "orders": [{"id": "order1", "amount": 100}]
      }
    ]
  }
}

// 使用路径 "data.items" 提取用户订单数据
```

## 🐛 常见问题

### Q: 安装依赖失败怎么办？
A: 
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r config/requirements_core.txt

# 或使用离线安装包
2.install_quick.bat
```

### Q: 大量请求时系统卡顿？
A: 
- 减少线程数（建议不超过10个）
- 增加请求间隔时间
- 分批处理大量数据

### Q: JSON结构检测不准确？
A: 
- 在"JSON结构管理"中添加自定义结构
- 使用测试功能验证结构模式
- 手动指定导出路径

### Q: 数据库文件损坏？
A: 
```bash
# 删除数据库文件，系统会自动重建
rm data/json_structures.db
```

### Q: 离线环境无法安装？
A: 
- 确保Python版本为3.11
- 使用管理员权限运行安装脚本
- 检查离线包是否完整

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发环境设置
```bash
# 克隆项目
git clone https://github.com/your-username/CURL_mass_execution.git
cd CURL_mass_execution

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装开发依赖
pip install -r config/requirements.txt

# 启动开发服务器
streamlit run app.py
```

### 代码规范
- 使用Python 3.11+语法
- 遵循PEP 8代码风格
- 添加适当的注释和文档字符串
- 编写单元测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**版本**: V2.0  
**最后更新**: 2024年12月  
**维护者**: [您的名字]  
**项目地址**: https://github.com/your-username/CURL_mass_execution

⭐ 如果这个项目对您有帮助，请给我们一个星标！ 