#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API批量请求工具主界面
负责用户界面和流程控制
"""

import streamlit as st
from typing import List
from src.core.curl_parser import CurlParser, CurlRequest
from src.core.batch_processor import BatchProcessor
from src.core.result_display import ResultDisplay

class CurlRunner:
    """API批量请求工具主控制器"""
    
    def __init__(self):
        # 初始化组件
        self.parser = CurlParser()
        self.batch_processor = BatchProcessor()
        self.result_display = ResultDisplay()
        
        # 初始化session state
        self._init_session_state()
    
    def _init_session_state(self):
        """初始化session state"""
        if 'curl_history' not in st.session_state:
            st.session_state.curl_history = []
        if 'parsed_curl' not in st.session_state:
            st.session_state.parsed_curl = None
        if 'selected_param' not in st.session_state:
            st.session_state.selected_param = None
        if 'param_values' not in st.session_state:
            st.session_state.param_values = ''
        if 'available_parameters' not in st.session_state:
            st.session_state.available_parameters = {}
        if 'curl_results' not in st.session_state:
            st.session_state.curl_results = []
        if 'curl_errors' not in st.session_state:
            st.session_state.curl_errors = []
        if 'downloaded_files' not in st.session_state:
            st.session_state.downloaded_files = []
        if 'batch_progress' not in st.session_state:
            st.session_state.batch_progress = {'current': 0, 'total': 0, 'batch': 0, 'total_batches': 0}

    def show_interface(self):
        """显示主界面"""
        st.title('API批量请求工具')
        st.write('粘贴CURL命令，解析后批量执行API请求')
        
        # 性能警告
        with st.expander("⚠️ 性能优化提示", expanded=False):
            st.info("""
            **大量请求优化建议:**
            - 建议单次请求数量不超过 200 个
            - 可调整线程数量控制并发度
            - 系统会自动分批处理大量请求
            - 如遇到连接问题，请减少线程数或增加请求间隔
            
            **大数据量处理建议:**
            - 10,000条记录: 可以正常处理
            - 50,000条记录: 建议使用分页参数
            - 200,000条记录: 建议分批请求或直接导出文件
            - 超过50MB响应: 将自动解析JSON并支持路径提取，同时保存备份文件
            """)
        
        # 添加示例curl命令
        with st.expander("📋 示例CURL命令"):
            st.code("""curl 'http://example.com/api/export' \\
  -H 'Accept: application/json, text/plain, */*' \\
  -H 'Content-Type: application/json;charset=UTF-8' \\
  -H 'Authorization: Bearer your-token' \\
  --data-raw '{"param1":"value1","param2":"value2"}' \\
  --insecure""")
        
        # CURL命令输入和解析
        self._show_curl_input()
        
        # 请求配置和参数选择
        if st.session_state.parsed_curl:
            self._show_request_config()
            self._show_parameter_selection()
        
        # 显示结果
        self._show_results()
    
    def _show_curl_input(self):
        """显示CURL输入界面"""
        curl_command = st.text_area('粘贴CURL命令:', height=150)
        if st.button('解析CURL命令'):
            if curl_command.strip():
                parsed_request = self.parser.parse(curl_command)
                if parsed_request:
                    st.session_state.parsed_curl = parsed_request
                    st.session_state.available_parameters = self.parser.extract_parameters(parsed_request)
                    
                    # 显示解析结果
                    self._show_parse_result(parsed_request)
                else:
                    st.error('❌ 解析失败，请检查CURL命令格式')
            else:
                st.warning('⚠️ 请输入CURL命令')
    
    def _show_parse_result(self, parsed_request: CurlRequest):
        """显示解析结果"""
        col1, col2 = st.columns(2)
        with col1:
            st.success('✅ CURL命令解析成功！')
            st.info(f"**请求方法:** {parsed_request.method}")
            st.info(f"**请求URL:** {parsed_request.url}")
            if parsed_request.download_file:
                st.warning("📁 检测到文件下载请求")
                st.info(f"**文件类型:** {parsed_request.file_extension}")
        
        with col2:
            st.info(f"**请求头数量:** {len(parsed_request.headers)}")
            st.info(f"**参数数量:** {len(parsed_request.params)}")
            if parsed_request.data:
                st.info(f"**请求体:** {len(parsed_request.data)} 个字段")
    
    def _show_request_config(self):
        """显示请求配置"""
        parsed_request = st.session_state.parsed_curl
        
        with st.expander("🔧 请求配置", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                parsed_request.url = st.text_input('请求URL:', value=parsed_request.url)
                method_options = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
                method_index = method_options.index(parsed_request.method.upper()) if parsed_request.method.upper() in method_options else 0
                parsed_request.method = st.selectbox('请求方法:', method_options, index=method_index, disabled=False)
            
            with col2:
                # 优化线程设置
                self.batch_processor.max_threads = st.slider('最大线程数:', 1, 20, 10, help="建议不超过10个线程")
                self.batch_processor.batch_size = st.slider('批处理大小:', 10, 100, 50, help="每批处理的请求数量")
                self.batch_processor.request_delay = st.slider('请求间隔(秒):', 0.0, 1.0, 0.1, 0.1, help="请求间的延迟时间")
                parsed_request.timeout = st.slider('超时时间(秒):', 1, 60, 10)
            
            # 性能优化配置
            with st.expander("⚡ 性能优化配置", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.max_display_errors = st.slider('最大显示错误数:', 5, 50, 20, help="错误信息显示限制")
                    st.session_state.max_display_files = st.slider('最大显示文件数:', 10, 100, 30, help="下载文件显示限制")
                with col2:
                    st.session_state.page_size = st.slider('分页大小:', 5, 50, 20, help="每页显示的结果数量")
                
                st.info("💡 性能提示: 结果数量限制已取消，所有结果都会显示")
            
            # 显示请求详情
            with st.expander("📋 请求详情"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**请求头:**")
                    for key, value in parsed_request.headers.items():
                        st.code(f"{key}: {value}")
                
                with col2:
                    if parsed_request.data:
                        st.write("**请求体:**")
                        st.json(parsed_request.data)
    
    def _show_parameter_selection(self):
        """显示参数选择界面"""
        st.subheader('📝 参数选择')
        param_keys = list(st.session_state.available_parameters.keys())
        if param_keys:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.session_state.selected_param = st.selectbox('选择要批量替换的参数:', param_keys, index=0)
            
            with col2:
                st.session_state.param_values = st.text_area(
                    f'输入{st.session_state.selected_param}的批量值 (每行一个):',
                    height=120,
                    value="\n".join([f"value{i+1}" for i in range(3)])
                )
            
            # 显示请求数量统计
            param_list = [v.strip() for v in st.session_state.param_values.split('\n') if v.strip()]
            if param_list:
                st.info(f"📊 将执行 {len(param_list)} 个请求，预计分 {max(1, len(param_list) // self.batch_processor.batch_size)} 批处理")
            
            if st.button('🚀 开始批量执行', type='primary'):
                if st.session_state.selected_param and st.session_state.param_values:
                    param_list = [v.strip() for v in st.session_state.param_values.split('\n') if v.strip()]
                    if param_list:
                        # 执行批量请求
                        self.batch_processor.run_batch_requests(
                            st.session_state.parsed_curl,
                            param_list,
                            st.session_state.selected_param
                        )
                    else:
                        st.error('❌ 请输入有效的参数值')
                else:
                    st.error('❌ 请选择参数并输入批量值')
        else:
            st.warning('⚠️ 未检测到可替换参数')
    
    def _show_results(self):
        """显示结果"""
        results = st.session_state.get('curl_results', [])
        errors = st.session_state.get('curl_errors', [])
        downloaded_files = st.session_state.get('downloaded_files', [])
        
        # 始终显示结果区域
        st.subheader('📊 执行结果')
        
        if results or errors:
            # 显示结果
            self.result_display.show_results(results, errors, downloaded_files)
            
            # 显示导出界面
            is_download_request = st.session_state.parsed_curl.download_file if st.session_state.parsed_curl else False
            self.result_display.show_export_interface(results, is_download_request)
        else:
            st.info("暂无执行结果，请先执行批量请求")
        
        # 始终显示分析界面
        self.result_display.show_analysis_interface(results)