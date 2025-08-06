#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CURL命令解析器
负责解析CURL命令并转换为请求对象
"""

import re
import json
import urllib.parse
import shlex
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import streamlit as st

@dataclass
class CurlRequest:
    url: str
    method: str = 'GET'
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, str] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 30
    download_file: bool = False
    file_extension: str = ''

def parse_curl_headers(curl_command: str) -> Dict[str, str]:
    """解析CURL命令中的请求头"""
    headers = {}
    try:
        tokens = shlex.split(curl_command)
        for i, token in enumerate(tokens):
            if token == '-H' and i + 1 < len(tokens):
                header = tokens[i + 1]
                if ':' in header:
                    key, value = header.split(':', 1)
                    headers[key.strip()] = value.strip()
            elif token == '-b' and i + 1 < len(tokens):
                # 解析Cookie
                cookie_value = tokens[i + 1]
                headers['Cookie'] = cookie_value.strip()
    except Exception as e:
        st.warning(f"解析请求头时出错: {e}")
    return headers

class CurlParser:
    """CURL命令解析器"""
    
    @staticmethod
    def parse(curl_command: str) -> Optional[CurlRequest]:
        """解析CURL命令并返回请求对象"""
        try:
            # 清理命令格式
            curl_command = re.sub(r'\\\s*\n', ' ', curl_command)
            curl_command = re.sub(r'\s+', ' ', curl_command).strip()
            
            request = CurlRequest(url="", method="GET")
            
            # 处理Windows转义字符
            curl_command_clean = curl_command.replace('^', '')
            
            # 解析请求方法
            method_match = re.search(r'-X\s+(\w+)', curl_command_clean, re.IGNORECASE)
            if method_match:
                request.method = method_match.group(1).upper()
            
            # 解析URL - 使用shlex正确解析，支持各种格式
            import shlex
            tokens = shlex.split(curl_command_clean)
            url = ""
            
            # 查找URL：从curl开始，跳过-X POST等参数，找到第一个非参数项
            for i, token in enumerate(tokens):
                if token.lower() == 'curl':
                    # 从curl位置开始查找第一个非参数项
                    j = i + 1
                    while j < len(tokens):
                        next_token = tokens[j]
                        # 跳过-X和POST参数
                        if next_token == '-X' and j + 1 < len(tokens):
                            j += 2  # 跳过-X和POST/GET
                            continue
                        # 跳过其他参数
                        if next_token.startswith('-'):
                            j += 1
                            continue
                        # 找到第一个非参数项，就是URL
                        url = next_token.strip("'\"")
                        break
                    break
            
            if url:
                request.url = url
            
            # 检查是否是文件下载请求
            if 'export' in request.url.lower() or 'download' in request.url.lower():
                request.download_file = True
                if 'exportllxs2' in request.url:
                    request.file_extension = '.xlsx'
                elif 'export' in request.url:
                    request.file_extension = '.xlsx'
                else:
                    request.file_extension = '.bin'
            
            # 解析请求头
            request.headers = parse_curl_headers(curl_command_clean)
            
            # 解析URL参数
            if '?' in request.url:
                url, query = request.url.split('?', 1)
                request.url = url
                for param in query.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        # 对于params参数，不进行URL解码，因为它本身就是JSON字符串的URL编码
                        if key == 'params':
                            request.params[key] = value
                        else:
                            decoded_value = urllib.parse.unquote(value)
                            request.params[key] = decoded_value
            
            # 解析请求体 - 支持-d和--data参数
            data_str = None
            
            # 尝试匹配 -d 参数
            data_match = re.search(r'-d\s+(["\"]).*?\1', curl_command_clean, re.DOTALL | re.IGNORECASE)
            if not data_match:
                data_match = re.search(r"-d\s+'(.+?)'", curl_command_clean, re.DOTALL | re.IGNORECASE)
            if not data_match:
                data_match = re.search(r'-d\s+"(.+?)"', curl_command_clean, re.DOTALL | re.IGNORECASE)
            
            # 如果没有找到-d，尝试--data
            if not data_match:
                data_match = re.search(r'--data(?:-raw)?\s+(["\"]).*?\1', curl_command_clean, re.DOTALL | re.IGNORECASE)
                if not data_match:
                    data_match = re.search(r"--data(?:-raw)?\s+'(.+?)'", curl_command_clean, re.DOTALL | re.IGNORECASE)
                if not data_match:
                    data_match = re.search(r'--data(?:-raw)?\s+"(.+?)"', curl_command_clean, re.DOTALL | re.IGNORECASE)
            
            if data_match:
                try:
                    data_str = data_match.group(1)
                    # 去除转义字符
                    data_str = data_str.replace('\\"', '"').replace("\\'", "'")
                    data_str = data_str.replace('^', '')
                    request.data = json.loads(data_str)
                except json.JSONDecodeError as e:
                    st.error(f"请求体JSON解析失败: {e}")
                    st.error(f"原始数据: {data_str}")
                    return None
            
            # 特殊处理params字段
            if 'params' in request.params:
                try:
                    params_str = request.params['params']
                    # 处理Windows转义字符
                    params_str = params_str.replace('^', '')
                    # 处理URL编码
                    params_str = urllib.parse.unquote(params_str)
                    params_json = json.loads(params_str)
                    # 将params内容也放入data中，但不删除URL参数
                    request.data.update(params_json)
                except json.JSONDecodeError as e:
                    st.warning(f"params字段JSON解析失败，将作为字符串处理: {e}")
                    st.warning(f"原始params数据: {params_str}")
            
            return request
            
        except Exception as e:
            st.error(f"解析CURL命令时出错: {e}")
            return None
    
    @staticmethod
    def extract_parameters(request: CurlRequest) -> Dict[str, str]:
        """提取可替换的参数"""
        parameters = {}
        
        def extract_json_keys(d, prefix=''):
            if isinstance(d, dict):
                for key, value in d.items():
                    current_key = f"{prefix}.{key}" if prefix else key
                    if isinstance(value, (str, int, float)):
                        parameters[current_key] = str(value)
                    elif isinstance(value, (dict, list)):
                        extract_json_keys(value, current_key)
            elif isinstance(d, list):
                for i, item in enumerate(d):
                    current_key = f"{prefix}[{i}]" if prefix else f"[{i}]"
                    if isinstance(item, (str, int, float)):
                        parameters[current_key] = str(item)
                    elif isinstance(item, (dict, list)):
                        extract_json_keys(item, current_key)
        
        # 从URL参数中提取
        for key, value in request.params.items():
            # 特殊处理params字段 - 解析为嵌套参数
            if key == 'params':
                try:
                    import json
                    import urllib.parse
                    # 先进行URL解码，因为params参数是URL编码的JSON字符串
                    decoded_value = urllib.parse.unquote(value)
                    params_json = json.loads(decoded_value)
                    # 将params中的字段提取为嵌套参数
                    for param_key, param_value in params_json.items():
                        parameters[f"params.{param_key}"] = str(param_value)
                except json.JSONDecodeError:
                    # 如果解析失败，作为普通参数处理
                    parameters[key] = value
            else:
                # 其他URL参数直接添加
                parameters[key] = value
        
        # 从请求体中提取（排除已经在params中处理过的字段）
        if request.data:
            for key, value in request.data.items():
                # 如果这个字段已经在params中处理过，跳过
                if f"params.{key}" not in parameters:
                    if isinstance(value, (str, int, float)):
                        parameters[key] = str(value)
                    elif isinstance(value, (dict, list)):
                        extract_json_keys(value, key)
        
        return parameters 