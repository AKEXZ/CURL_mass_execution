#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON转Excel转换工具
独立的JSON数据转换功能
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any
from src.utils.utils import json_to_excel, get_by_path, parse_multi_json
from src.models.models import JsonStructureDB

class JsonConverter:
    """JSON转Excel转换器"""
    
    def __init__(self):
        try:
            self.db = JsonStructureDB()
            self.has_db = True
        except:
            self.has_db = False
            st.warning("⚠️ 数据库功能不可用，将使用基础功能")
    
    def show_interface(self):
        """显示主界面"""
        st.title('🔄 JSON转Excel工具')
        st.write('将JSON数据转换为Excel格式，支持自定义字段路径提取')
        
        # 示例数据
        with st.expander("📋 示例JSON数据", expanded=False):
            st.code("""{
  "data": [
    {"name": "张三", "age": 18, "score": 90},
    {"name": "李四", "age": 20, "score": 85}
  ]
}""")
        
        # JSON输入
        self._show_json_input()
        
        # 路径选择和导出
        if st.session_state.get('json_data'):
            self._show_path_selection()
            self._show_export_interface()
    
    def _show_json_input(self):
        """显示JSON输入界面"""
        st.subheader('📝 JSON数据输入')
        
        # 示例按钮
        if st.button("📋 插入示例JSON"):
            example_json = '''{
  "data": [
    {"name": "张三", "age": 18, "score": 90, "city": "北京"},
    {"name": "李四", "age": 20, "score": 85, "city": "上海"},
    {"name": "王五", "age": 22, "score": 92, "city": "广州"}
  ],
  "total": 3,
  "status": "success"
}'''
            st.session_state['json_input'] = example_json
        
        # JSON输入框
        json_str = st.text_area(
            "粘贴JSON数据:",
            height=200,
            key="json_input",
            value=st.session_state.get("json_input", "")
        )
        
        if st.button('🔍 解析JSON'):
            if json_str.strip():
                try:
                    json_data = parse_multi_json(json_str)
                    st.session_state['json_data'] = json_data
                    st.success('✅ JSON解析成功！')
                    
                    # 显示数据结构预览
                    self._show_data_preview(json_data)
                except Exception as e:
                    st.error(f'❌ JSON解析失败: {str(e)}')
            else:
                st.warning('⚠️ 请输入JSON数据')
    
    def _show_data_preview(self, json_data):
        """显示数据结构预览"""
        st.subheader('📊 数据结构预览')
        
        if isinstance(json_data, dict):
            # 分析结构
            structure_info = self._analyze_structure(json_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**数据结构分析:**")
                for key, info in structure_info.items():
                    st.write(f"• {key}: {info}")
            
            with col2:
                st.write("**数据预览:**")
                st.json(json_data)
        
        elif isinstance(json_data, list):
            st.write(f"**数组数据，共 {len(json_data)} 项**")
            if json_data:
                st.write("**第一项数据:**")
                st.json(json_data[0])
    
    def _analyze_structure(self, data, prefix="", max_depth=2, current_depth=0):
        """分析数据结构"""
        if current_depth >= max_depth:
            return {"...": "更深层级"}
        
        structure = {}
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    if value:
                        structure[f"{prefix}{key}"] = f"数组[{len(value)}项] - 示例: {type(value[0]).__name__}"
                    else:
                        structure[f"{prefix}{key}"] = "空数组"
                elif isinstance(value, dict):
                    structure[f"{prefix}{key}"] = "对象"
                else:
                    structure[f"{prefix}{key}"] = f"{type(value).__name__}: {str(value)[:50]}"
        return structure
    
    def _show_path_selection(self):
        """显示路径选择界面"""
        st.subheader('🎯 字段路径选择')
        
        json_data = st.session_state.get('json_data')
        if not json_data:
            return
        
        # 自动检测功能
        detected_path = None
        if self.has_db and isinstance(json_data, dict):
            detected_path = self.db.auto_detect_structure(json_data)
            if detected_path:
                st.success(f"🔍 自动检测到结构: `{detected_path}`")
        
        # 路径输入
        col1, col2 = st.columns([2, 1])
        
        with col1:
            default_path = st.session_state.get("json_export_path", detected_path or "")
            export_path = st.text_input(
                "导出字段路径（如 data、data.items，留空导出全部数据）",
                value=default_path,
                key="json_export_path_input"
            )
            st.session_state["json_export_path"] = export_path
        
        with col2:
            if st.button("🔍 测试路径"):
                if export_path and export_path.strip():
                    test_result = get_by_path(json_data, export_path.strip())
                    if test_result is not None:
                        st.success(f"✅ 路径有效，找到 {len(test_result) if isinstance(test_result, list) else 1} 项数据")
                        with st.expander("预览数据"):
                            st.json(test_result)
                    else:
                        st.error("❌ 路径无效，未找到数据")
                else:
                    st.info("将导出全部数据")
        
        # 显示数据库中的结构选项
        if self.has_db:
            active_structures = self.db.get_all_active()
            if active_structures:
                st.write("**数据库中的结构选项:**")
                cols = st.columns(3)
                for i, structure in enumerate(active_structures):
                    with cols[i % 3]:
                        if st.button(f"📋 {structure.name}", key=f"json_structure_{i}"):
                            st.session_state["json_export_path"] = structure.path_pattern
                            st.success(f"已选择结构: {structure.name} ({structure.path_pattern})")
                            st.rerun()
    
    def _show_export_interface(self):
        """显示导出界面"""
        st.subheader('📤 数据导出')
        
        json_data = st.session_state.get('json_data')
        if not json_data:
            st.info("暂无数据，请先解析JSON")
            return
        
        # 显示当前选择的路径
        export_path = st.session_state.get("json_export_path", "")
        if export_path and export_path.strip():
            st.info(f"当前导出路径: {export_path}")
        else:
            st.info("将导出全部数据")
        
        # 导出按钮
        if st.button('📊 导出为Excel', key="json_export_excel_btn"):
            try:
                # 获取当前最新的导出路径
                current_export_path = st.session_state.get("json_export_path", export_path)
                
                # 生成Excel文件
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"json_export_{timestamp}.xlsx"
                
                if current_export_path and current_export_path.strip():
                    # 使用指定路径提取数据
                    excel_bytes = json_to_excel(json_data, filename, current_export_path.strip())
                    st.info(f"📊 使用路径 '{current_export_path}' 导出数据")
                else:
                    # 导出全部数据
                    excel_bytes = json_to_excel(json_data, filename)
                    st.info("📊 导出全部数据")
                
                # 提供下载
                st.download_button(
                    label="📥 下载Excel文件",
                    data=excel_bytes,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.success("✅ 导出成功！")
                
            except Exception as e:
                st.error(f"❌ 导出失败: {str(e)}")
                st.info("💡 提示：请检查路径是否正确，或尝试留空路径导出全部数据") 