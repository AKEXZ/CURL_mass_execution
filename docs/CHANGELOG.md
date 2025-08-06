# 变更日志

## 2024-07-28 - 功能精简

### 🗑️ 删除的功能

#### 台区线损接口数据提取工具
- **删除文件**: `src/tools/lineloss_collector.py`
- **功能描述**: 自动化台区线损数据采集和处理
- **删除原因**: 功能重复，API批量请求工具已能覆盖此需求

#### 网页信息采集工具
- **删除文件**: `src/tools/header_collector.py`
- **功能描述**: 智能网页内容提取和headers/cookies采集
- **删除原因**: 使用频率低，功能相对独立

#### 工具模块目录
- **删除目录**: `src/tools/`
- **删除原因**: 所有工具文件已删除，目录不再需要

### 🔄 更新的文件

#### 主程序文件
- **文件**: `src/main.py`
- **更新内容**:
  - 删除 `LineLossCollector` 和 `HeaderCollector` 的导入
  - 更新导航菜单，移除相关功能选项
  - 更新主页功能说明

#### 文档文件
- **文件**: `README.md`
- **更新内容**:
  - 删除线损数据收集和网页信息采集功能说明
  - 更新主要功能列表

- **文件**: `PROJECT_STRUCTURE.md`
- **更新内容**:
  - 删除 `tools/` 目录结构说明
  - 更新模块依赖关系图
  - 删除相关功能模块说明

- **文件**: `docs/README.md`
- **更新内容**:
  - 删除已删除功能的说明

- **文件**: `docs/DEPENDENCIES.md`
- **更新内容**:
  - 删除对已删除文件的依赖引用
  - 更新使用位置说明

### ✅ 保留的功能

#### 核心功能
- **API批量请求工具**: 支持curl解析、参数批量替换、多线程执行、文件下载
- **JSON结构管理**: 自定义和管理API响应的JSON结构模式
- **帮助中心**: 交互式使用指南和示例
- **JSON转Excel工具**: 数据格式转换和导出

#### 技术特性
- **数据库驱动**: SQLite数据库存储JSON结构模式
- **自动检测**: 智能识别API响应的JSON结构
- **快速选择**: 一键选择合适的导出路径
- **测试验证**: 内置测试功能验证结构正确性
- **文件下载**: 支持API文件下载和批量处理

### 🎯 优化效果

1. **代码精简**: 删除了约 200 行代码
2. **依赖简化**: 减少了不必要的依赖引用
3. **功能聚焦**: 专注于核心的API批量请求和JSON结构管理功能
4. **维护性提升**: 减少了需要维护的模块数量

### 📊 项目结构变化

#### 删除前
```
src/
├── main.py
├── core/
│   ├── curl_runner.py
│   ├── json_structure_manager.py
│   └── help_page.py
├── tools/                    # ❌ 已删除
│   ├── lineloss_collector.py # ❌ 已删除
│   └── header_collector.py   # ❌ 已删除
├── utils/
│   └── utils.py
└── models/
    └── models.py
```

#### 删除后
```
src/
├── main.py
├── core/
│   ├── curl_runner.py
│   ├── json_structure_manager.py
│   └── help_page.py
├── utils/
│   └── utils.py
└── models/
    └── models.py
```

### 🚀 启动方式

启动方式保持不变：
- **Windows**: `start_windows.bat` 或 `start.ps1`
- **Linux/macOS**: `./start.sh`
- **Python**: `python3 start.py`
- **直接启动**: `streamlit run app.py`

---

**版本**: V2.1  
**日期**: 2024-07-28  
**状态**: ✅ 已完成 