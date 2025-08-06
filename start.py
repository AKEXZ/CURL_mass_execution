#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
xzx 数据采集平台启动脚本
"""

import os
import sys
import subprocess

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import streamlit
        import pandas
        import requests
        import openpyxl
        print("✅ 核心依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 依赖检查失败: {e}")
        print("请运行: pip install -r config/requirements_core.txt")
        return False

def start_app():
    """启动应用"""
    if not check_dependencies():
        return False
    
    print("🚀 启动 xzx 数据采集平台...")
    print("📊 应用将在浏览器中打开")
    print("🔗 默认地址: http://localhost:8501")
    print("⏹️  按 Ctrl+C 停止应用")
    print("-" * 50)
    
    try:
        # 启动Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("📊 xzx 数据采集平台")
    print("=" * 50)
    
    # 检查当前目录
    if not os.path.exists("app.py"):
        print("❌ 请在项目根目录运行此脚本")
        return False
    
    # 启动应用
    return start_app()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 