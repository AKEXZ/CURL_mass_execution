import streamlit as st
from src.utils.utils import json_to_excel_demo
from src.core.json_structure_manager import JsonStructureManager
from src.core.help_page import HelpPage

# 初始化会话状态
if 'current_page' not in st.session_state:
    st.session_state.current_page = "主页"

def main():
    """主函数"""
    st.set_page_config(
        page_title="xzx 数据采集平台",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📊 xzx 数据采集平台")
    st.markdown("---")

    # 侧边栏导航
    with st.sidebar:
        st.header("🔧 功能导航")
        app_mode = st.selectbox(
            "选择功能模块:",
            ["主页", "JSON转Excel工具", "API批量请求工具", "JSON结构管理", "帮助中心"]
        )

    # 根据选择显示不同功能
    if app_mode == "主页":
        st.header("🏠 欢迎使用 xzx 数据采集平台")
        st.markdown("""
        ### 主要功能
        - **🔄 JSON转Excel工具**: 将JSON数据转换为Excel格式，支持自定义字段路径提取
        - **🔄 API批量请求工具**: 支持curl解析、参数批量替换、多线程执行、文件下载
        - **⚙️ JSON结构管理**: 自定义和管理API响应的JSON结构模式
        - **📚 帮助中心**: 交互式使用指南和示例
        
        ### 快速开始
        1. 在左侧导航栏选择需要的功能模块
        2. 按照界面提示进行操作
        3. 查看帮助中心获取详细使用指南
        """)
        
    elif app_mode == "JSON转Excel工具":
        from src.core.json_converter import JsonConverter
        converter = JsonConverter()
        converter.show_interface()
    elif app_mode == "API批量请求工具":
        from src.core.curl_runner import CurlRunner
        curl_runner = CurlRunner()
        curl_runner.show_interface()
    elif app_mode == "JSON结构管理":
        manager = JsonStructureManager()
        manager.show_interface()
    elif app_mode == "帮助中心":
        help_page = HelpPage()
        help_page.show_interface()

if __name__ == "__main__":
    main()