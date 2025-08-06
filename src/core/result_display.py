#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结果显示模块
负责展示请求结果、文件下载和导出功能
"""

import os
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any
from src.utils.utils import json_to_excel, get_by_path
from src.models.models import JsonStructureDB

class ResultDisplay:
    """结果显示器"""
    
    def __init__(self):
        self.db = JsonStructureDB()
    
    def show_results(self, results: List[Dict], errors: List[Dict], downloaded_files: List[Dict]):
        """显示执行结果"""
        if not results and not errors:
            return
        
        # 显示统计信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总请求数", len(results) + len(errors))
        with col2:
            st.metric("成功", len(results), delta=len(results))
        with col3:
            st.metric("失败", len(errors), delta=-len(errors))
        with col4:
            if results:
                avg_time = sum(r['response_time'] for r in results) / len(results)
                st.metric("平均响应时间", f"{avg_time}ms")
        
        # 显示下载的文件
        if downloaded_files:
            self._show_downloaded_files(downloaded_files)
        
        # 显示详细结果
        if results:
            self._show_detailed_results(results)
        
        # 显示错误信息
        if errors:
            self._show_errors(errors)
    
    def _show_downloaded_files(self, downloaded_files: List[Dict]):
        """显示下载的文件"""
        st.subheader('📁 下载的文件')
        
        # 限制显示的文件数量，防止浏览器卡死
        max_display_files = st.session_state.get('max_display_files', 30)  # 使用用户配置或默认30
        total_files = len(downloaded_files)
        
        if total_files > max_display_files:
            st.warning(f"⚠️ 文件数量较多({total_files}个)，为避免浏览器卡死，仅显示前{max_display_files}个文件")
            display_files = downloaded_files[:max_display_files]
        else:
            display_files = downloaded_files
        
        # 添加分页功能
        file_page_size = st.session_state.get('page_size', 10)  # 使用用户配置或默认10
        if total_files > file_page_size:
            total_pages = (len(display_files) + file_page_size - 1) // file_page_size
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("◀️ 上一页", key="file_prev", disabled=st.session_state.get('file_page', 0) == 0):
                    st.session_state['file_page'] = max(0, st.session_state.get('file_page', 0) - 1)
                    st.rerun()
            
            with col2:
                st.write(f"第 {st.session_state.get('file_page', 0) + 1} 页，共 {total_pages} 页")
            
            with col3:
                if st.button("下一页 ▶️", key="file_next", disabled=st.session_state.get('file_page', 0) >= total_pages - 1):
                    st.session_state['file_page'] = min(total_pages - 1, st.session_state.get('file_page', 0) + 1)
                    st.rerun()
            
            # 计算当前页的文件
            current_page = st.session_state.get('file_page', 0)
            start_idx = current_page * file_page_size
            end_idx = min(start_idx + file_page_size, len(display_files))
            page_files = display_files[start_idx:end_idx]
            
            st.write(f"显示第 {start_idx + 1}-{end_idx} 个文件（共 {len(display_files)} 个）")
        else:
            page_files = display_files
        
        # 显示文件
        for file_info in page_files:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{os.path.basename(file_info['filename'])}**")
                st.write(f"参数值: {file_info['param_value']}")
            with col2:
                st.write(f"大小: {file_info['size']} bytes")
            with col3:
                # 使用更唯一的key
                unique_key = f"download_{file_info['param_value']}_{file_info['timestamp']}_{os.path.basename(file_info['filename'])}"
                if st.button(f"📥 下载", key=unique_key):
                    with open(file_info['filename'], 'rb') as f:
                        st.download_button(
                            label="保存文件",
                            data=f.read(),
                            file_name=os.path.basename(file_info['filename']),
                            key=unique_key + "_btn"
                        )
        
        # 显示完整文件统计
        if total_files > max_display_files:
            st.info(f"📊 完整文件统计: 共 {total_files} 个文件")
            st.info("💡 提示: 所有文件都已保存到本地，可以通过文件管理器查看")
    
    def _show_detailed_results(self, results: List[Dict]):
        """显示详细结果"""
        # 显示所有结果，不限制数量
        display_results = results
        total_results = len(results)
        
        with st.expander("📋 详细结果", expanded=False):
            # 添加分页功能
            page_size = st.session_state.get('page_size', 20)  # 使用用户配置或默认20
            if total_results > page_size:
                total_pages = (len(display_results) + page_size - 1) // page_size
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("◀️ 上一页", disabled=st.session_state.get('result_page', 0) == 0):
                        st.session_state['result_page'] = max(0, st.session_state.get('result_page', 0) - 1)
                        st.rerun()
                
                with col2:
                    st.write(f"第 {st.session_state.get('result_page', 0) + 1} 页，共 {total_pages} 页")
                
                with col3:
                    if st.button("下一页 ▶️", disabled=st.session_state.get('result_page', 0) >= total_pages - 1):
                        st.session_state['result_page'] = min(total_pages - 1, st.session_state.get('result_page', 0) + 1)
                        st.rerun()
                
                # 计算当前页的结果
                current_page = st.session_state.get('result_page', 0)
                start_idx = current_page * page_size
                end_idx = min(start_idx + page_size, len(display_results))
                page_results = display_results[start_idx:end_idx]
                
                st.write(f"显示第 {start_idx + 1}-{end_idx} 个结果（共 {len(display_results)} 个）")
            else:
                page_results = display_results
            
            # 显示结果
            for i, result in enumerate(page_results):
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.write(f"**请求 {start_idx + i + 1 if 'start_idx' in locals() else i + 1}**")
                        st.write(f"参数: {result.get('param_value', 'N/A')}")
                        st.write(f"状态: {result.get('status_code', 'N/A')}")
                        st.write(f"时间: {result.get('response_time', 'N/A')}ms")
                    
                    with col2:
                        if 'message' in result:
                            st.success(result['message'])
                            # 如果是大响应，显示额外信息
                            if result.get('is_large_response'):
                                st.info(f"📁 备份文件: {result.get('filename', 'N/A')}")
                                st.info(f"📊 响应大小: {result.get('content_length', 0):,} 字节")
                        elif 'error' in result:
                            st.error(result['error'])
                        else:
                            # 显示响应内容预览 - 限制内容长度
                            if 'preview' in result:
                                # 大响应，显示预览
                                preview_content = result['preview'][:500] + "..." if len(result['preview']) > 500 else result['preview']
                                st.text_area(f"响应内容预览:", preview_content, height=100, key=f"preview_{start_idx + i if 'start_idx' in locals() else i}")
                                st.info(f"完整响应大小: {result.get('content_length', 0):,} 字节")
                                if result.get('is_large_response'):
                                    st.info(f"📁 备份文件: {result.get('filename', 'N/A')}")
                            else:
                                # 正常响应，显示完整内容 - 限制内容长度
                                content = result.get('content', '')
                                if isinstance(content, dict):
                                    # 对于JSON，只显示前几个字段
                                    if len(str(content)) > 1000:
                                        st.json(dict(list(content.items())[:5]))
                                        st.info(f"显示前5个字段，完整内容共{len(content)}个字段")
                                    else:
                                        st.json(content)
                                else:
                                    content_str = str(content)
                                    if len(content_str) > 500:
                                        content_str = content_str[:500] + "..."
                                    st.text_area(f"响应内容:", content_str, height=100, key=f"content_{start_idx + i if 'start_idx' in locals() else i}")
            
            # 显示完整结果统计
            st.info(f"📊 完整统计: 成功 {len([r for r in results if 'error' not in r])} 个，失败 {len([r for r in results if 'error' in r])} 个")
    
    def _show_errors(self, errors: List[Dict]):
        """显示错误信息"""
        st.subheader('❌ 错误信息')
        
        # 限制显示的错误数量，防止浏览器卡死
        max_display_errors = st.session_state.get('max_display_errors', 20)  # 使用用户配置或默认20
        total_errors = len(errors)
        
        if total_errors > max_display_errors:
            st.warning(f"⚠️ 错误数量较多({total_errors}个)，为避免浏览器卡死，仅显示前{max_display_errors}个错误")
            display_errors = errors[:max_display_errors]
        else:
            display_errors = errors
        
        # 显示错误信息
        for error in display_errors:
            st.error(f"参数 {error.get('param_value', 'N/A')}: {error.get('error', 'Unknown error')}")
        
        # 显示完整错误统计
        if total_errors > max_display_errors:
            st.info(f"📊 完整错误统计: 共 {total_errors} 个错误")
            st.info("💡 提示: 使用导出功能可以获取所有错误详情")
    
    def show_export_interface(self, results: List[Dict], is_download_request: bool = False):
        """显示导出界面"""
        if is_download_request:
            return
        
        st.subheader('📤 数据导出')
        
        if not results:
            st.info("暂无响应数据，请先执行请求获取数据")
            return
        
        # 从数据库获取激活的结构
        active_structures = self.db.get_all_active()
        
        # 尝试自动检测合适的导出路径
        default_path = st.session_state.get("curl_export_path", "")
        if not default_path and results:
            first_result = results[0]
            if 'content' in first_result and isinstance(first_result['content'], dict):
                # 使用数据库自动检测
                detected_path = self.db.auto_detect_structure(first_result['content'])
                if detected_path:
                    default_path = detected_path
                    st.success(f"自动检测到结构: {detected_path}")
        
        export_path = st.text_input(
            "导出字段路径（如 resultValue.items、data.items，可留空导出全部response）", 
            value=default_path,
            key="export_path_input"
        )
        st.session_state["curl_export_path"] = export_path
        
        # 显示当前选择的路径
        if export_path and export_path.strip():
            st.info(f"当前导出路径: {export_path}")
        else:
            st.info("将导出全部响应数据")
        
        # 显示数据库中的结构选项
        if active_structures:
            st.write("**数据库中的结构选项:**")
            cols = st.columns(3)
            for i, structure in enumerate(active_structures):
                with cols[i % 3]:
                    if st.button(f"📋 {structure.name}", key=f"structure_{i}"):
                        st.session_state["curl_export_path"] = structure.path_pattern
                        st.success(f"已选择结构: {structure.name} ({structure.path_pattern})")
                        st.rerun()
        
        # 导出按钮
        if st.button('📊 导出为Excel', key="export_excel_btn"):
            try:
                excel_data = []
                # 获取当前最新的导出路径
                current_export_path = st.session_state.get("curl_export_path", export_path)
                
                # 移除调试信息
                
                for i, result in enumerate(results):
                    if 'content' in result and isinstance(result['content'], dict):
                        if current_export_path and current_export_path.strip():
                            # 使用指定路径提取数据
                            extracted_data = get_by_path(result['content'], current_export_path.strip())
                            
                            if extracted_data:
                                if isinstance(extracted_data, list):
                                    for item in extracted_data:
                                        item['_param_value'] = result['param_value']
                                        item['_request_index'] = i + 1  # 添加请求序号
                                        excel_data.append(item)
                                else:
                                    extracted_data['_param_value'] = result['param_value']
                                    extracted_data['_request_index'] = i + 1  # 添加请求序号
                                    excel_data.append(extracted_data)
                            else:
                                # 路径提取失败，记录错误（带序号）
                                st.warning(f"第{i+1}个请求: 路径 '{current_export_path}' 在结果中未找到数据")
                        else:
                            # 导出全部response
                            result['content']['_param_value'] = result['param_value']
                            result['content']['_request_index'] = i + 1  # 添加请求序号
                            excel_data.append(result['content'])
                
                if excel_data:
                    # 生成Excel文件内容（内存流）
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"export_results_{timestamp}.xlsx"
                    excel_bytes = json_to_excel(excel_data)
                    
                    # 显示导出信息
                    if current_export_path and current_export_path.strip():
                        st.info(f"📊 使用路径 '{current_export_path}' 导出数据")
                    else:
                        st.info("📊 导出全部响应数据")
                    
                    # 提供下载
                    st.download_button(
                        label="📥 下载Excel文件",
                        data=excel_bytes,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success(f"✅ 导出成功！共 {len(excel_data)} 条数据")
                else:
                    st.warning("⚠️ 没有可导出的数据")
            except Exception as e:
                st.error(f"❌ 导出失败: {str(e)}")
    
    def show_analysis_interface(self, results: List[Dict]):
        """显示分析界面"""
        st.subheader('🔍 响应结构分析')
        
        if not results:
            st.info("暂无响应数据，请先执行请求获取数据")
            return
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button('📊 导出到Excel'):
                try:
                    excel_data = json_to_excel(results)
                    st.download_button(
                        label="下载Excel文件",
                        data=excel_data,
                        file_name=f"export_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"导出失败: {e}")
        
        with col2:
            if st.button('🔍 分析响应结构'):
                self._analyze_response_structure(results)
    
    def _analyze_response_structure(self, results: List[Dict]):
        """分析响应结构"""
        if not results:
            st.warning("没有可分析的响应数据")
            return
        
        # 分析第一个成功的响应
        for result in results:
            if 'content' in result and isinstance(result['content'], dict):
                st.subheader("🔍 响应结构分析")
                st.json(result['content'])
                break
        else:
            st.info("未找到JSON格式的响应数据进行分析") 