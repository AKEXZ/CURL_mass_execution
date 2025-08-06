import pandas as pd
import io
import json
import streamlit as st
from src.models.models import JsonStructureDB
import os
import logging
from datetime import datetime

def get_by_path(data, path):
    """按路径提取嵌套字段，支持 data.items 这种点号分隔，也支持数组索引"""
    if not path:
        return data
    
    keys = path.split('.')
    current = data
    
    for key in keys:
        if current is None:
            return None
        
        # 检查是否是数组索引
        if '[' in key and ']' in key:
            # 处理数组索引，如 records[0]
            array_name = key.split('[')[0]
            index_str = key.split('[')[1].split(']')[0]
            
            if isinstance(current, dict):
                current = current.get(array_name, None)
            else:
                return None
            
            if current is None:
                return None
            
            try:
                index = int(index_str)
                if isinstance(current, list) and 0 <= index < len(current):
                    current = current[index]
                else:
                    return None
            except (ValueError, TypeError):
                return None
        else:
            # 普通字段访问
            if isinstance(current, dict):
                current = current.get(key, None)
            else:
                return None
    
    return current

def parse_multi_json(text):
    """
    支持多种格式：
    1. 单个JSON对象或数组
    2. 多行，每行一个JSON对象
    3. 用 --- 分割的多个JSON对象
    """
    text = text.strip()
    # 1. 尝试标准JSON
    try:
        return json.loads(text)
    except Exception:
        pass
    # 2. 尝试每行一个JSON对象
    lines = [line for line in text.splitlines() if line.strip()]
    objs = []
    for line in lines:
        try:
            obj = json.loads(line)
            objs.append(obj)
        except Exception:
            break
    if len(objs) == len(lines) and objs:
        return objs
    # 3. 尝试用 --- 分割
    blocks = [b for b in text.split('---') if b.strip()]
    objs = []
    for block in blocks:
        try:
            obj = json.loads(block)
            objs.append(obj)
        except Exception:
            break
    if len(objs) == len(blocks) and objs:
        return objs
    raise ValueError('无法识别的JSON格式，请检查输入！')

def json_to_excel(json_data, file_name='data.xlsx', list_path=None):
    """
    :param list_path: str, 如 'data' 或 'data.items'，指定导出为表格的字段路径
    :return: bytes, Excel文件内容
    """
    import pandas as pd
    import io
    if list_path:
        # 如果 json_data 是 list，则对每个元素提取路径并合并
        if isinstance(json_data, list):
            all_rows = []
            for item in json_data:
                target = get_by_path(item, list_path)
                if isinstance(target, list):
                    all_rows.extend(target)
                elif target is not None:
                    all_rows.append(target)
            if not all_rows:
                raise ValueError('指定路径未找到 list 数据')
            df = pd.DataFrame(all_rows)
        else:
            target = get_by_path(json_data, list_path)
            if isinstance(target, list):
                df = pd.DataFrame(target)
            else:
                raise ValueError('指定路径未找到 list 数据')
    else:
        # 兼容原有自动推断
        if isinstance(json_data, dict):
            for v in json_data.values():
                if isinstance(v, list):
                    df = pd.DataFrame(v)
                    break
            else:
                df = pd.DataFrame([json_data])
        elif isinstance(json_data, list):
            df = pd.DataFrame(json_data)
        else:
            raise ValueError('无法识别的 json 数据结构')
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="数据")
    output.seek(0)
    return output.getvalue()

def json_to_excel_demo():
    st.title("JSON转Excel工具演示")
    st.write("粘贴你的JSON数据，点击按钮即可下载Excel文件")
    
    # 初始化数据库
    try:
        db = JsonStructureDB()
        has_db = True
    except:
        has_db = False
        st.warning("⚠️ 数据库功能不可用，将使用基础功能")
    
    example_json = '{\n  "data": [\n    {"name": "张三", "age": 18, "score": 90},\n    {"name": "李四", "age": 20, "score": 85}\n  ]\n}'
    
    if st.button("插入参考JSON模板"):
        st.session_state["json_demo_text"] = example_json
    
    json_str = st.text_area("粘贴JSON数据", height=200, key="json_demo_text", value=st.session_state.get("json_demo_text", ""))
    
    # 自动检测功能
    detected_path = None
    if has_db and json_str.strip():
        try:
            json_data = parse_multi_json(json_str)
            if isinstance(json_data, dict):
                detected_path = db.auto_detect_structure(json_data)
                if detected_path:
                    st.success(f"🔍 自动检测到结构: `{detected_path}`")
        except:
            pass
    
    # 路径选择
    col1, col2 = st.columns([2, 1])
    
    with col1:
        list_path = st.text_input(
            "要导出的字段路径（如 data 或 data.items，可留空自动推断）", 
            value=detected_path or st.session_state.get("json_demo_path", "data")
        )
    
    with col2:
        if has_db:
            # 显示数据库中的结构选项
            active_structures = db.get_all_active()
            if active_structures:
                st.write("**🗄️ 数据库结构:**")
                for structure in active_structures[:3]:  # 只显示前3个
                    if st.button(f"{structure.name}", key=f"demo_{structure.id}"):
                        st.session_state["json_demo_path"] = structure.path_pattern
                        st.rerun()
    
    # 路径选项（从数据库获取）
    if has_db:
        st.write("**📋 数据库中的结构选项:**")
        active_structures = db.get_all_active()
        if active_structures:
            cols = st.columns(3)
            for i, structure in enumerate(active_structures):
                if cols[i % 3].button(f"📋 {structure.name}", key=f"demo_path_{i}"):
                    st.session_state["json_demo_path"] = structure.path_pattern
                    st.rerun()
        else:
            st.info("数据库中没有激活的结构，请在'JSON结构管理'中添加")
    
    if st.button("生成Excel"):
        try:
            json_data = parse_multi_json(json_str)
            if json_data is not None:
                excel_bytes = json_to_excel(json_data, list_path=list_path.strip() or None)
                st.download_button("下载 Excel", data=excel_bytes, file_name="data.xlsx")
                
                # 显示导出信息
                st.success("✅ Excel文件生成成功！")
                if list_path.strip():
                    st.info(f"📊 导出路径: `{list_path}`")
                
                # 显示数据结构信息
                if isinstance(json_data, dict):
                    st.write("**📋 数据结构分析:**")
                    def analyze_structure(obj, prefix="", max_depth=2, current_depth=0):
                        if current_depth >= max_depth:
                            return f"{prefix}... (深度限制)"
                        if isinstance(obj, dict):
                            result = []
                            for k, v in obj.items():
                                if isinstance(v, (dict, list)):
                                    result.append(f"{prefix}{k}: {type(v).__name__}")
                                    if current_depth < max_depth - 1:
                                        result.append(analyze_structure(v, prefix + "  ", max_depth, current_depth + 1))
                                else:
                                    result.append(f"{prefix}{k}: {type(v).__name__} = {str(v)[:30]}")
                            return "\n".join(result)
                        elif isinstance(obj, list):
                            if len(obj) > 0:
                                return f"{prefix}list[{len(obj)}] - 第一个元素: {analyze_structure(obj[0], prefix + '  ', max_depth, current_depth + 1)}"
                            else:
                                return f"{prefix}list[0]"
                        else:
                            return f"{prefix}{type(obj).__name__}"
                    
                    structure_info = analyze_structure(json_data)
                    st.code(structure_info, language="text")
            else:
                st.error("请输入有效的JSON数据")
        except Exception as e:
            st.error(f"解析或导出失败: {e}")
            st.write("**💡 调试建议:**")
            st.write("1. 检查JSON格式是否正确")
            st.write("2. 确认导出路径是否存在")
            st.write("3. 尝试使用自动检测的路径")
            if has_db:
                st.write("4. 在'JSON结构管理'中添加新的结构模式") 

class Logger:
    """简单日志工具，按天分文件，写入data/logs/目录"""
    def __init__(self, log_dir='data/logs'):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.logger = None
        self.current_date = None
        self._update_logger()

    def _update_logger(self):
        today = datetime.now().strftime('%Y%m%d')
        if self.current_date != today:
            self.current_date = today
            log_file = os.path.join(self.log_dir, f'{today}.log')
            self.logger = logging.getLogger(f'xzx_{today}')
            # 设置为DEBUG级别
            self.logger.setLevel(logging.DEBUG)
            # 避免重复添加handler
            if not self.logger.handlers:
                fh = logging.FileHandler(log_file, encoding='utf-8')
                # 文件handler也设置为DEBUG级别
                fh.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)
                # 禁用控制台输出
                self.logger.propagate = False

    def log(self, msg, level='info'):
        self._update_logger()
        if level == 'debug':
            self.logger.debug(msg)
        elif level == 'info':
            self.logger.info(msg)
        elif level == 'warn':
            self.logger.warning(msg)
        elif level == 'error':
            self.logger.error(msg)
        else:
            self.logger.info(msg) 