# 🔄 CURL Mass Execution

> 一个强大的基于Streamlit的数据采集与处理平台，支持CURL命令批量执行、JSON数据转换、结构化管理等功能。

## 🚀 主要特性

- **🔄 CURL批量执行**: 智能解析CURL命令，支持参数批量替换和多线程并发执行
- **📊 JSON转Excel**: 智能JSON数据转换，支持自定义字段路径提取
- **🏗️ 结构化管理**: 自定义JSON结构模式，数据库存储和管理
- **⚡ 高性能**: 多线程并发处理，支持大批量数据
- **🎨 用户友好**: 现代化Web界面，操作简单直观
- **🔧 离线支持**: 完整的离线安装包和依赖管理

## 🎯 核心功能

### CURL批量执行工具
- 自动解析CURL命令，提取URL、请求头、请求体等信息
- 支持批量替换URL参数、请求体参数、请求头等
- 多线程并发处理，可配置线程数和批处理大小
- 实时显示执行结果，支持错误处理和重试机制
- 自动下载响应文件，支持批量文件管理
- 将API响应数据导出为Excel格式

### JSON转Excel工具
- 支持单个JSON对象、数组、多行JSON等格式
- 支持自定义字段路径（如 `data.items`）提取数据
- 自动检测JSON结构，推荐最佳导出路径
- 提供数据结构分析和实时预览功能
- 支持大量JSON数据的批量转换

### JSON结构管理
- 自定义JSON结构模式，支持复杂嵌套结构
- SQLite数据库存储，支持结构版本管理
- 基于历史数据的智能结构检测
- 实时测试结构模式的有效性
- 支持批量导入和导出结构模式

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/your-username/CURL_mass_execution.git
cd CURL_mass_execution

# 安装依赖
pip install -r config/requirements_core.txt

# 启动应用
streamlit run app.py
```

## 📦 离线安装

项目提供了完整的离线安装包：

```bash
# Windows用户
2.install_quick.bat

# Linux/macOS用户
./start.sh
```

## 💡 使用示例

### 批量获取用户数据
```bash
# CURL命令
curl 'https://api.example.com/users' \
  -H 'Authorization: Bearer token123' \
  -d '{"user_id":"123"}'

# 批量替换user_id参数
123
456
789
101112
```

### JSON数据转换
```json
{
  "data": [
    {"name": "张三", "age": 18, "score": 90},
    {"name": "李四", "age": 20, "score": 85}
  ]
}
```

## 🔧 技术栈

- **后端**: Python 3.11+, Streamlit
- **数据处理**: Pandas, NumPy
- **网络请求**: Requests, urllib3
- **文件处理**: openpyxl, xlsxwriter
- **数据库**: SQLite
- **界面**: Streamlit Web UI

## 📄 许可证

本项目采用 MIT 许可证。

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！ 