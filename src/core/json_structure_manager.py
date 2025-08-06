import streamlit as st
import json
from src.models.models import JsonStructureDB, JsonStructure

class JsonStructureManager:
    def __init__(self):
        self.db = JsonStructureDB()
    
    def show_interface(self):
        st.title('JSON结构管理')
        st.write('管理API响应的JSON结构模式，用于自动检测和导出数据')
        
        # 侧边栏用于添加/编辑结构
        with st.sidebar:
            st.subheader('添加新结构')
            with st.form("add_structure"):
                name = st.text_input("结构名称", key="new_name")
                description = st.text_area("描述", key="new_description")
                path_pattern = st.text_input("路径模式 (如: resultValue.items)", key="new_path")
                example_response = st.text_area("示例响应 (可选)", key="new_example")
                
                if st.form_submit_button("添加结构"):
                    if name and path_pattern:
                        try:
                            structure_id = self.db.add_structure(
                                name=name,
                                description=description,
                                path_pattern=path_pattern,
                                example_response=example_response
                            )
                            st.success(f"结构 '{name}' 添加成功！")
                            st.rerun()
                        except Exception as e:
                            st.error(f"添加失败: {e}")
                    else:
                        st.error("请填写名称和路径模式")
        
        # 主界面显示所有结构
        st.subheader('现有结构')
        
        # 获取所有结构
        structures = self.db.get_all()
        
        if not structures:
            st.info("还没有定义任何JSON结构")
            return
        
        # 显示结构列表
        for structure in structures:
            with st.expander(f"{structure.name} ({'✅' if structure.is_active else '❌'})", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**描述:** {structure.description}")
                    st.write(f"**路径模式:** `{structure.path_pattern}`")
                    if structure.example_response:
                        st.write("**示例响应:**")
                        st.code(structure.example_response, language="json")
                
                with col2:
                    st.write("**操作:**")
                    
                    # 编辑按钮
                    if st.button("✏️ 编辑", key=f"edit_{structure.id}"):
                        st.session_state.editing_structure = structure
                        st.rerun()
                    
                    # 删除按钮 - 使用确认对话框
                    delete_btn_key = f"delete_{structure.id}"
                    delete_state_key = f"delete_state_{structure.id}"
                    if delete_state_key not in st.session_state:
                        st.session_state[delete_state_key] = False
                    
                    if st.session_state.get(delete_state_key, False):
                        # 显示确认删除界面
                        st.warning(f"⚠️ 确认删除结构 '{structure.name}'?")
                        col_confirm1, col_confirm2 = st.columns(2)
                        with col_confirm1:
                            if st.button("✅ 确认删除", key=f"confirm_delete_{structure.id}"):
                                try:
                                    self.db.delete_structure(structure.id)
                                    st.success(f"✅ 结构 '{structure.name}' 删除成功！")
                                    del st.session_state[delete_state_key]
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ 删除失败: {e}")
                        with col_confirm2:
                            if st.button("❌ 取消", key=f"cancel_delete_{structure.id}"):
                                st.session_state[delete_state_key] = False
                                st.rerun()
                    else:
                        if st.button("🗑️ 删除", key=delete_btn_key):
                            st.session_state[delete_state_key] = True
                            st.rerun()
                    
                    # 激活/停用按钮
                    status_text = "⏸️ 停用" if structure.is_active else "▶️ 激活"
                    if st.button(status_text, key=f"toggle_{structure.id}"):
                        self.db.update_structure(
                            structure_id=structure.id,
                            name=structure.name,
                            description=structure.description,
                            path_pattern=structure.path_pattern,
                            example_response=structure.example_response,
                            is_active=not structure.is_active
                        )
                        st.success(f"✅ 已{status_text}结构 '{structure.name}'")
                        st.rerun()
        
        # 编辑模式
        if 'editing_structure' in st.session_state:
            structure = st.session_state.editing_structure
            st.subheader(f'编辑结构: {structure.name}')
            
            with st.form("edit_structure"):
                edit_name = st.text_input("结构名称", value=structure.name, key="edit_name")
                edit_description = st.text_area("描述", value=structure.description, key="edit_description")
                edit_path_pattern = st.text_input("路径模式", value=structure.path_pattern, key="edit_path")
                edit_example_response = st.text_area("示例响应", value=structure.example_response, key="edit_example")
                edit_is_active = st.checkbox("激活", value=structure.is_active, key="edit_active")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("保存"):
                        try:
                            self.db.update_structure(
                                structure_id=structure.id,
                                name=edit_name,
                                description=edit_description,
                                path_pattern=edit_path_pattern,
                                example_response=edit_example_response,
                                is_active=edit_is_active
                            )
                            st.success("更新成功！")
                            del st.session_state.editing_structure
                            st.rerun()
                        except Exception as e:
                            st.error(f"更新失败: {e}")
                
                with col2:
                    if st.form_submit_button("取消"):
                        del st.session_state.editing_structure
                        st.rerun()
        
        # 测试模式
        st.subheader('测试结构检测')
        test_response = st.text_area("输入测试响应JSON", height=200, key="test_response")
        
        if test_response:
            try:
                response_data = json.loads(test_response)
                st.write("**检测结果:**")
                
                # 使用数据库中的结构进行检测
                detected_path = self.db.auto_detect_structure(response_data)
                if detected_path:
                    st.success(f"检测到匹配结构: `{detected_path}`")
                    
                    # 显示匹配的结构信息
                    for structure in structures:
                        if structure.path_pattern == detected_path:
                            st.write(f"**结构名称:** {structure.name}")
                            st.write(f"**描述:** {structure.description}")
                            break
                else:
                    st.warning("未检测到匹配的结构")
                
                # 显示所有激活结构的检测结果
                st.write("**所有激活结构的检测结果:**")
                active_structures = self.db.get_all_active()
                for structure in active_structures:
                    try:
                        from utils import get_by_path
                        result = get_by_path(response_data, structure.path_pattern)
                        if result is not None:
                            st.success(f"✅ {structure.name} (`{structure.path_pattern}`): 匹配")
                        else:
                            st.info(f"❌ {structure.name} (`{structure.path_pattern}`): 不匹配")
                    except Exception as e:
                        st.error(f"❌ {structure.name} (`{structure.path_pattern}`): 错误 - {e}")
                        
            except json.JSONDecodeError:
                st.error("无效的JSON格式")
            except Exception as e:
                st.error(f"测试失败: {e}")

def main():
    manager = JsonStructureManager()
    manager.show_interface()

if __name__ == "__main__":
    main() 