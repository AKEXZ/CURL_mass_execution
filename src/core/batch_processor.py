#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量请求处理器
负责管理批量请求的执行、进度跟踪和结果收集
"""

import threading
import time
from queue import Queue
from typing import Dict, List, Any
import streamlit as st
from src.core.curl_parser import CurlRequest
from src.core.request_processor import RequestProcessor, RequestModifier
from src.utils.utils import Logger

class BatchProcessor:
    """批量请求处理器"""
    
    def __init__(self):
        # 优化线程和批处理设置
        self.max_threads = 10  # 最大线程数
        self.batch_size = 50   # 每批处理数量
        self.request_delay = 0.1  # 请求间隔(秒)
        self.max_requests = 999999  # 最大请求数限制（设置为很大值，实际无限制）
        
        # 结果管理
        self.max_results = 999999  # 最大结果数限制，设置为很大值，实际无限制
        
        self.request_processor = RequestProcessor()
        self.results = []
        self.errors = []
        self.downloaded_files = []
        self.logger = Logger()
    
    def run_batch_requests(self, base_request: CurlRequest, param_values: List[str], param_key: str):
        """执行批量请求"""
        # 清空之前的结果
        self.results = []
        self.errors = []
        self.downloaded_files = []
        
        total_requests = len(param_values)
        total_batches = max(1, (total_requests + self.batch_size - 1) // self.batch_size)  # 向上取整，确保所有请求都被处理
        
        # 更新进度状态
        st.session_state.batch_progress = {
            'current': 0,
            'total': total_requests,
            'batch': 0,
            'total_batches': total_batches
        }
        
        # 创建进度显示
        progress_bar = st.progress(0)
        status_text = st.empty()
        batch_text = st.empty()
        
        self.logger.log(f"开始批量请求: 共{len(param_values)}个, 参数key: {param_key}")
        
        try:
            # 分批处理
            for batch_idx in range(total_batches):
                start_idx = batch_idx * self.batch_size
                end_idx = min(start_idx + self.batch_size, total_requests)
                batch_values = param_values[start_idx:end_idx]
                
                st.session_state.batch_progress['batch'] = batch_idx + 1
                batch_text.text(f"处理批次 {batch_idx + 1}/{total_batches} (请求 {start_idx + 1}-{end_idx})")
                self.logger.log(f"开始处理批次 {batch_idx + 1}/{total_batches} (请求 {start_idx + 1}-{end_idx})")
                
                # 处理当前批次
                self._process_batch(base_request, batch_values, param_key, progress_bar, status_text)
                self.logger.log(f"完成批次 {batch_idx + 1}/{total_batches}")
                
                # 批次间延迟
                if batch_idx < total_batches - 1:
                    time.sleep(0.5)
            
            # 完成
            progress_bar.progress(1.0)
            status_text.success(f'✅ 处理完成! 成功: {len(self.results)}, 失败: {len(self.errors)}')
            self.logger.log(f"批量请求全部完成! 成功: {len(self.results)}, 失败: {len(self.errors)}")
            batch_text.empty()
            
            # 保存到session_state - 添加线程安全保护
            import threading
            if not hasattr(st.session_state, '_lock'):
                st.session_state._lock = threading.Lock()
            
            with st.session_state._lock:
                st.session_state['curl_results'] = self.results.copy()
                st.session_state['curl_errors'] = self.errors.copy()
                st.session_state['downloaded_files'] = self.downloaded_files.copy()
            
            # 防止页面自动刷新
            st.rerun()
            
        except Exception as e:
            self.logger.log(f"批量处理过程中出错: {e}", level='error')
            st.error(f"批量处理过程中出错: {e}")
            status_text.error(f"❌ 处理失败: {e}")
    
    def _process_batch(self, base_request: CurlRequest, batch_values: List[str], param_key: str, progress_bar, status_text):
        """处理单个批次的请求"""
        queue = Queue()
        for value in batch_values:
            queue.put(value)
            self.logger.log(f"加入队列: {param_key}={value}")
        
        # 创建线程池
        thread_count = min(self.max_threads, len(batch_values))
        threads = []
        
        # 添加线程安全保护
        import threading
        results_lock = threading.Lock()
        errors_lock = threading.Lock()
        files_lock = threading.Lock()
        
        for _ in range(thread_count):
            thread = threading.Thread(
                target=self._worker,
                args=(queue, base_request, param_key, results_lock, errors_lock, files_lock)
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # 监控进度
        initial_count = len(self.results) + len(self.errors)
        while any(thread.is_alive() for thread in threads):
            current_count = len(self.results) + len(self.errors)
            total_progress = current_count / st.session_state.batch_progress['total']
            
            progress_bar.progress(total_progress)
            status_text.text(f"处理中: {current_count}/{st.session_state.batch_progress['total']} "
                           f"(成功: {len(self.results)}, 失败: {len(self.errors)})")
            
            time.sleep(0.1)
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
    
    def _worker(self, queue: Queue, base_request: CurlRequest, param_key: str, results_lock, errors_lock, files_lock):
        """工作线程函数"""
        while not queue.empty():
            try:
                param_value = queue.get_nowait()
            except:
                break
            
            try:
                # 添加请求延迟
                time.sleep(self.request_delay)
                
                # 修改请求参数
                modified_request = self.request_processor.request_modifier.modify_request(base_request, param_key, param_value)
                
                # 执行请求
                result = self.request_processor.execute_request(modified_request, param_value)
                
                # 处理结果 - 使用线程安全保护
                if 'error' in result:
                    with errors_lock:
                        self.errors.append(result)
                    self.logger.log(f"请求失败: {param_key}={param_value}, 错误: {result['error']}", level='error')
                else:
                    with results_lock:
                        self.results.append(result)
                    # 如果是文件下载，添加到下载文件列表
                    if 'filename' in result:
                        file_info = {
                            'param_value': result['param_value'],
                            'filename': result['filename'],
                            'size': result['size'],
                            'timestamp': result.get('timestamp', '')
                        }
                        with files_lock:
                            self.downloaded_files.append(file_info)
                    self.logger.log(f"请求成功: {param_key}={param_value}, 状态码: {result.get('status_code', 'N/A')}")
                
            except Exception as e:
                error_result = {
                    'param_value': param_value,
                    'error': f'请求失败: {str(e)}',
                    'response_time': 0
                }
                with errors_lock:
                    self.errors.append(error_result)
                self.logger.log(f"请求失败: {param_key}={param_value}, 错误: {str(e)}", level='error')
            
            finally:
                queue.task_done()
    
    def set_config(self, max_threads: int = None, batch_size: int = None, request_delay: float = None, max_requests: int = None):
        """设置配置参数"""
        if max_threads is not None:
            self.max_threads = max_threads
        if batch_size is not None:
            self.batch_size = batch_size
        if request_delay is not None:
            self.request_delay = request_delay
        if max_requests is not None:
            self.max_requests = max_requests 