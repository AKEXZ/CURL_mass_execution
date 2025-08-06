#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
请求处理器
负责执行HTTP请求和处理响应
"""

import requests
import json
import os
import re
import copy
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from src.core.curl_parser import CurlRequest
from src.utils.utils import Logger
import urllib.parse

class RequestProcessor:
    """HTTP请求处理器"""
    
    def __init__(self):
        self.logger = Logger()
        self.request_modifier = RequestModifier(self.logger)
        self.max_json_size = 50 * 1024 * 1024  # 50MB (增加到50MB)
        self.max_preview_size = 1024 * 1024  # 1MB
    
    def execute_request(self, request: CurlRequest, param_value: str) -> Dict[str, Any]:
        """执行单个HTTP请求"""
        try:
            start_time = time.time()
            # 添加调试信息
            self.logger.log(f"DEBUG: request.params before logging: {request.params}", level='debug')
            # 构建完整的URL用于日志显示
            # 使用requests库构建实际发送的URL，但手动处理params参数避免双重编码
            import requests
            
            # 创建临时请求对象，但不包含params参数
            temp_request = requests.Request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                json=request.data if request.data else None
            )
            prepared_request = temp_request.prepare()
            base_url = prepared_request.url
            
            # 手动构建URL参数，避免requests库对params进行二次编码
            param_pairs = []
            for k, v in request.params.items():
                if k == 'params':
                    # params参数已经是URL编码的，直接使用
                    param_pairs.append(f"{k}={v}")
                else:
                    # 其他参数让requests库处理
                    encoded_key = urllib.parse.quote(str(k), safe='')
                    encoded_value = urllib.parse.quote(str(v), safe='')
                    param_pairs.append(f"{encoded_key}={encoded_value}")
            
            if param_pairs:
                actual_url = f"{base_url}?{'&'.join(param_pairs)}"
            else:
                actual_url = base_url
            
            self.logger.log(f"发起请求: {request.method} {actual_url} param_value={param_value}")
            
            # 发送请求时也使用手动构建的URL，避免双重编码
            response = requests.request(
                method=request.method,
                url=actual_url,  # 使用手动构建的URL
                headers=request.headers,
                json=request.data if request.data else None,
                timeout=request.timeout,
                stream=True
            )
            response_time = int((time.time() - start_time) * 1000)
            self.logger.log(f"收到响应: 状态码={response.status_code}, param_value={param_value}, 耗时={response_time}ms")
            
            content_type = response.headers.get('content-type', '')
            content_length = int(response.headers.get('content-length', 0) or 0)
            is_json = 'application/json' in content_type
            is_large = content_length > self.max_json_size
            
            # 处理文件下载
            if request.download_file or not is_json:
                return self._handle_file_download(response, request, param_value, response_time, content_type)
            elif is_large:
                # 大响应，尝试JSON处理
                return self._handle_large_json_response(response, request, param_value, response_time, content_type)
            else:
                return self._handle_json_response(response, param_value, response_time)
                
        except requests.exceptions.Timeout:
            self.logger.log(f"请求超时: param_value={param_value}", level='warn')
            return {
                'param_value': param_value,
                'error': '请求超时',
                'response_time': 0
            }
        except requests.exceptions.ConnectionError:
            self.logger.log(f"连接错误: param_value={param_value}", level='error')
            return {
                'param_value': param_value,
                'error': '连接错误',
                'response_time': 0
            }
        except Exception as e:
            self.logger.log(f"请求异常: param_value={param_value}, 错误: {str(e)}", level='error')
            return {
                'param_value': param_value,
                'error': f'请求失败: {str(e)}',
                'response_time': 0
            }
    
    def _handle_file_download(self, response, request: CurlRequest, param_value: str, response_time: int, content_type: str) -> Dict[str, Any]:
        """处理文件下载"""
        try:
            download_dir = "downloads"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = request.file_extension or self._guess_extension(content_type)
            filename = f"{download_dir}/export_{param_value}_{timestamp}{ext}"
            
            total_size = 0
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)
            
            self.logger.log(f"文件下载成功: {filename}, param_value={param_value}, size={total_size}")
            return {
                'param_value': param_value,
                'status_code': response.status_code,
                'response_time': response_time,
                'message': '文件下载成功',
                'filename': filename,
                'size': total_size,
                'content_type': content_type
            }
            
        except Exception as e:
            self.logger.log(f"文件下载失败: param_value={param_value}, 错误: {str(e)}", level='error')
            return {
                'param_value': param_value,
                'error': f'文件下载失败: {str(e)}',
                'response_time': response_time
            }
    
    def _handle_large_json_response(self, response, request: CurlRequest, param_value: str, response_time: int, content_type: str) -> Dict[str, Any]:
        """处理大JSON响应（超过50MB）"""
        try:
            raw_content = response.content
            content_size = len(raw_content)
            
            self.logger.log(f"处理大JSON响应: param_value={param_value}, size={content_size} bytes")
            
            # 尝试解析JSON
            try:
                json_data = response.json()
                self.logger.log(f"大JSON响应解析成功: param_value={param_value}")
                
                # 生成预览
                preview = raw_content[:self.max_preview_size].decode(errors='replace')
                
                # 同时保存到文件（作为备份）
                download_dir = "downloads"
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{download_dir}/large_json_{param_value}_{timestamp}.json"
                
                with open(filename, 'wb') as f:
                    f.write(raw_content)
                
                return {
                    'param_value': param_value,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'message': f'大JSON响应处理成功，已保存到文件',
                    'content': json_data,  # 完整的JSON数据用于导出
                    'preview': preview,    # 预览用于显示
                    'content_length': content_size,
                    'filename': filename,  # 备份文件路径
                    'is_large_response': True
                }
                
            except json.JSONDecodeError as e:
                self.logger.log(f"大响应JSON解析失败: param_value={param_value}, 错误: {e}", level='error')
                # JSON解析失败，作为文件下载处理
                return self._handle_file_download(response, request, param_value, response_time, content_type)
                
        except Exception as e:
            self.logger.log(f"大JSON响应处理失败: param_value={param_value}, 错误: {str(e)}", level='error')
            return {
                'param_value': param_value,
                'error': f'大JSON响应处理失败: {str(e)}',
                'response_time': response_time
            }

    def _handle_json_response(self, response, param_value: str, response_time: int) -> Dict[str, Any]:
        """处理JSON响应"""
        try:
            raw_content = response.content
            
            # 尝试解析JSON，无论大小
            try:
                json_data = response.json()
                self.logger.log(f"JSON响应处理成功: param_value={param_value}")
                
                # 如果响应过大，同时保存完整数据和预览
                if len(raw_content) > self.max_preview_size:
                    preview = raw_content[:self.max_preview_size].decode(errors='replace')
                    self.logger.log(f"JSON响应过大，仅显示前{self.max_preview_size}字节预览: param_value={param_value}")
                    return {
                        'param_value': param_value,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'message': f'响应过大，仅显示前{self.max_preview_size}字节预览',
                        'content': json_data,  # 保存完整的JSON数据用于导出
                        'preview': preview,    # 保存预览用于显示
                        'content_length': len(raw_content)
                    }
                else:
                    return {
                        'param_value': param_value,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'content': json_data
                    }
            except json.JSONDecodeError:
                # 非JSON响应
                text_content = raw_content.decode(errors='replace')
                self.logger.log(f"JSON响应处理失败: param_value={param_value}, 非JSON响应")
                
                if len(raw_content) > self.max_preview_size:
                    preview = text_content[:self.max_preview_size]
                    return {
                        'param_value': param_value,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'content': text_content,  # 保存完整内容用于导出
                        'preview': preview,       # 保存预览用于显示
                        'content_length': len(raw_content)
                    }
                else:
                    return {
                        'param_value': param_value,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'content': text_content
                    }
            
        except Exception as e:
            self.logger.log(f"JSON响应处理失败: param_value={param_value}, 错误: {str(e)}", level='error')
            return {
                'param_value': param_value,
                'error': f'响应处理失败: {str(e)}',
                'response_time': response_time
            }
    
    def _guess_extension(self, content_type: str) -> str:
        """根据Content-Type猜测文件扩展名"""
        if 'excel' in content_type or 'spreadsheet' in content_type:
            return '.xlsx'
        elif 'csv' in content_type:
            return '.csv'
        elif 'pdf' in content_type:
            return '.pdf'
        elif 'zip' in content_type:
            return '.zip'
        elif 'json' in content_type:
            return '.json'
        else:
            return '.bin'

class RequestModifier:
    """请求参数修改器"""
    def __init__(self, logger):
        self.logger = logger
    
    def modify_request(self, base_request: CurlRequest, param_key: str, param_value: str) -> CurlRequest:
        import re
        import json
        import urllib.parse
        modified_request = copy.deepcopy(base_request)
        
        # 添加调试日志
        self.logger.log(f"DEBUG: modify_request called with param_key='{param_key}', param_value='{param_value}'", level='debug')
        
        # 处理嵌套参数 (如 params.pageIndex, data.items, resultValue.items)
        if '.' in param_key:
            parts = param_key.split('.')
            self.logger.log(f"DEBUG: Processing nested parameter: {param_key}", level='debug')
            # 检查是否是 params.xxx 格式
            if parts[0] == 'params' and len(parts) > 1:
                self.logger.log(f"DEBUG: Processing params.{'.'.join(parts[1:])}", level='debug')
                # 处理 params 中的嵌套参数
                if 'params' in modified_request.params:
                    try:
                        # 先解码params字符串（params参数现在是URL编码的）
                        params_str = modified_request.params['params']
                        # 检查是否已经被URL编码
                        if '%' in params_str:
                            params_str = urllib.parse.unquote(params_str)
                        params_json = json.loads(params_str)
                        
                        # 设置嵌套字段
                        current = params_json
                        for i, part in enumerate(parts[1:-1]):
                            if part in current:
                                if isinstance(current[part], dict):
                                    current = current[part]
                                else:
                                    current[part] = {}
                                    current = current[part]
                            else:
                                current[part] = {}
                                current = current[part]
                        # 设置最终字段
                        # 对于某些字段，尝试转换为数字类型
                        if parts[-1] in ['pageIndex', 'pageSize']:
                            try:
                                current[parts[-1]] = int(param_value)
                            except ValueError:
                                current[parts[-1]] = param_value
                        else:
                            current[parts[-1]] = param_value
                        
                        # 重新生成JSON字符串，然后进行URL编码（因为params参数需要保持URL编码格式）
                        json_str = json.dumps(params_json, ensure_ascii=False, separators=(',', ':'))
                        # 对JSON字符串进行URL编码，因为params参数需要保持URL编码格式
                        encoded_json = urllib.parse.quote(json_str, safe='')
                        modified_request.params['params'] = encoded_json
                        self.logger.log(f"DEBUG: Successfully updated params JSON", level='debug')
                    except json.JSONDecodeError as e:
                        self.logger.log(f"DEBUG: Failed to parse params JSON: {e}", level='debug')
                        # 如果解析失败，不处理
                        pass
            elif parts[0] in modified_request.data:
                self.logger.log(f"DEBUG: Processing data.{'.'.join(parts[1:])}", level='debug')
                # 处理 data 中的嵌套参数
                def set_nested(d, nested_key, value):
                    if '.' in nested_key:
                        key, rest = nested_key.split('.', 1)
                        if key in d:
                            if isinstance(d[key], dict):
                                set_nested(d[key], rest, value)
                            else:
                                d[key] = value
                    else:
                        d[nested_key] = value
                set_nested(modified_request.data, '.'.join(parts[1:]), param_value)
            # 注意：嵌套参数处理完成后，直接返回，不执行后续逻辑
        else:
            self.logger.log(f"DEBUG: Processing non-nested parameter: {param_key}", level='debug')
            # 处理数组索引 (如 data.records[0])
            if '[' in param_key and ']' in param_key:
                array_match = re.match(r'(.+)\[(\d+)\]', param_key)
                if array_match:
                    array_key = array_match.group(1)
                    index = int(array_match.group(2))
                    if array_key in modified_request.data and isinstance(modified_request.data[array_key], list):
                        if index < len(modified_request.data[array_key]):
                            modified_request.data[array_key][index] = param_value
            else:
                # 1. 如果 param_key 原本就在 params 中，替换 params 中的值
                if param_key in modified_request.params:
                    self.logger.log(f"DEBUG: Replacing existing param: {param_key}", level='debug')
                    # 不进行URL编码，让requests库自动处理
                    modified_request.params[param_key] = str(param_value)
                # 2. 如果 param_key 在 data 中，替换 data 中的值（不添加到 params）
                elif param_key in modified_request.data:
                    self.logger.log(f"DEBUG: Replacing existing data: {param_key}", level='debug')
                    modified_request.data[param_key] = param_value
                # 3. 检查是否在 params 的 JSON 字符串中（如 params 字段）
                else:
                    found_in_json = False
                    # 检查 params 中是否有 JSON 字符串包含该字段
                    for key, value in modified_request.params.items():
                        if isinstance(value, str):
                            # 尝试解析为JSON
                            try:
                                # 先解码（如果已经被编码）
                                decoded_value = value
                                if '%' in value:
                                    decoded_value = urllib.parse.unquote(value)
                                json_data = json.loads(decoded_value)
                                if param_key in json_data:
                                    # 替换 JSON 中的字段
                                    json_data[param_key] = param_value
                                    # 重新生成JSON字符串，然后进行URL编码
                                    json_str = json.dumps(json_data, ensure_ascii=False, separators=(',', ':'))
                                    encoded_json = urllib.parse.quote(json_str, safe='')
                                    modified_request.params[key] = encoded_json
                                    found_in_json = True
                                    self.logger.log(f"DEBUG: Found and replaced in JSON: {param_key}", level='debug')
                                    break
                            except json.JSONDecodeError:
                                # 不是JSON，继续检查下一个
                                continue
                    
                    # 如果都没有找到，才根据请求方法智能判断添加位置
                    if not found_in_json:
                        method = getattr(modified_request, 'method', 'GET').upper()
                        if method in ['GET', 'DELETE']:
                            self.logger.log(f"DEBUG: Adding new param: {param_key}", level='debug')
                            # 不进行URL编码，让requests库自动处理
                            modified_request.params[param_key] = str(param_value)
                        else:
                            self.logger.log(f"DEBUG: Adding new data: {param_key}", level='debug')
                            modified_request.data[param_key] = param_value
        
        return modified_request 