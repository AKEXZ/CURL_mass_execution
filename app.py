#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xzx 数据采集平台
主入口文件
"""
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入并运行主程序
if __name__ == "__main__":
    from src.main import main
    main() 