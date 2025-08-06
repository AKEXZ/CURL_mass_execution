import streamlit as st
import json
from src.models.models import JsonStructureDB

class HelpPage:
    def __init__(self):
        self.db = JsonStructureDB()
    
    def show_interface(self):
        st.title('📚 JSON结构管理帮助中心')
        st.write('了解如何使用JSON结构管理功能来自定义和管理API响应的JSON结构模式')
        
        # 侧边栏导航
        with st.sidebar:
            st.subheader('📖 帮助目录')
            help_sections = [
                "功能概述",
                "快速开始",
                "预设结构",
                "添加新结构",
                "管理结构",
                "测试功能",
                "在API工具中使用",
                "常见问题",
                "示例演示"
            ]
            
            selected_section = st.radio(
                "选择帮助主题",
                help_sections,
                index=0
            )
        
        # 主内容区域
        if selected_section == "功能概述":
            self.show_overview()
        elif selected_section == "快速开始":
            self.show_quick_start()
        elif selected_section == "预设结构":
            self.show_preset_structures()
        elif selected_section == "添加新结构":
            self.show_add_structure()
        elif selected_section == "管理结构":
            self.show_manage_structures()
        elif selected_section == "测试功能":
            self.show_test_function()
        elif selected_section == "在API工具中使用":
            self.show_api_integration()
        elif selected_section == "常见问题":
            self.show_faq()
        elif selected_section == "示例演示":
            self.show_examples()
    
    def show_overview(self):
        st.header('🎯 功能概述')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('✨ 主要特性')
            features = [
                "🔍 **自动检测**: 智能识别API响应的JSON结构",
                "🗄️ **数据库管理**: 所有结构存储在SQLite数据库中",
                "⚡ **快速选择**: 一键选择合适的导出路径",
                "🔄 **实时更新**: 结构变更立即生效",
                "🧪 **测试验证**: 内置测试功能验证结构正确性"
            ]
            
            for feature in features:
                st.write(feature)
        
        with col2:
            st.subheader('📊 支持的结构类型')
            structure_types = [
                "嵌套对象结构 (如: resultValue.items)",
                "数组结构 (如: data)",
                "混合结构 (如: result.data.items)",
                "自定义结构 (任意嵌套层级)"
            ]
            
            for structure_type in structure_types:
                st.write(f"• {structure_type}")
        
        st.subheader('🎨 界面预览')
        st.image("https://via.placeholder.com/800x400/4CAF50/FFFFFF?text=JSON结构管理界面预览", 
                caption="JSON结构管理界面", use_column_width=True)
    
    def show_quick_start(self):
        st.header('🚀 快速开始')
        
        st.subheader('第一步：访问管理界面')
        st.write('在主界面侧边栏选择 "⚙️ JSON结构管理"')
        
        st.subheader('第二步：查看预设结构')
        st.write('系统已预设了6种常见结构，可以直接使用')
        
        st.subheader('第三步：添加自定义结构')
        with st.expander("点击查看详细步骤"):
            st.write("""
            1. 在侧边栏填写结构信息
            2. 输入结构名称和描述
            3. 指定路径模式（如：resultValue.items）
            4. 可选：添加示例响应
            5. 点击"添加结构"按钮
            """)
        
        st.subheader('第四步：测试结构')
        st.write('使用测试功能验证结构是否正确匹配')
        
        st.subheader('第五步：在API工具中使用')
        st.write('运行API请求后，系统会自动检测并推荐导出路径')
    
    def show_preset_structures(self):
        st.header('📋 预设结构')
        st.write('系统预设了以下常见JSON结构，可以直接使用：')
        
        # 获取预设结构
        structures = self.db.get_all()
        
        for structure in structures:
            with st.expander(f"📌 {structure.name}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**描述**: {structure.description}")
                    st.write(f"**路径模式**: `{structure.path_pattern}`")
                    st.write(f"**状态**: {'✅ 激活' if structure.is_active else '❌ 停用'}")
                
                with col2:
                    if structure.example_response:
                        st.write("**示例响应**:")
                        st.code(structure.example_response, language="json")
    
    def show_add_structure(self):
        st.header('➕ 添加新结构')
        
        st.subheader('结构信息')
        
        with st.form("help_add_structure"):
            name = st.text_input("结构名称", placeholder="例如：自定义API结构")
            description = st.text_area("描述", placeholder="描述这个结构的用途和特点")
            path_pattern = st.text_input("路径模式", placeholder="例如：resultValue.items")
            example_response = st.text_area("示例响应（可选）", 
                                         placeholder='{"resultValue": {"items": [{"id": 1}]}}',
                                         height=150)
            
            if st.form_submit_button("📝 查看添加步骤"):
                if name and path_pattern:
                    st.success("✅ 结构信息填写完整！")
                    st.write("**下一步操作：**")
                    st.write("1. 切换到'JSON结构管理'页面")
                    st.write("2. 在侧边栏填写相同信息")
                    st.write("3. 点击'添加结构'按钮")
                else:
                    st.error("❌ 请填写结构名称和路径模式")
        
        st.subheader('路径模式语法')
        st.write("路径模式使用点号分隔的键名，支持嵌套结构：")
        
        syntax_examples = [
            ("resultValue.items", "访问 resultValue.items"),
            ("data.items", "访问 data.items"),
            ("result.data", "访问 result.data"),
            ("items", "直接访问 items"),
            ("response.data.items", "深层嵌套结构")
        ]
        
        for pattern, description in syntax_examples:
            st.code(f"{pattern}  # {description}")
    
    def show_manage_structures(self):
        st.header('⚙️ 管理结构')
        
        st.subheader('编辑结构')
        st.write("""
        1. 在JSON结构管理页面找到要编辑的结构
        2. 点击"编辑"按钮
        3. 修改结构信息
        4. 点击"保存"按钮
        """)
        
        st.subheader('删除结构')
        st.write("""
        1. 在JSON结构管理页面找到要删除的结构
        2. 点击"删除"按钮
        3. 确认删除操作
        ⚠️ **注意**: 删除操作不可恢复
        """)
        
        st.subheader('激活/停用结构')
        st.write("""
        1. 在JSON结构管理页面找到目标结构
        2. 点击"激活"或"停用"按钮
        3. 停用的结构不会出现在自动检测中
        """)
        
        st.subheader('结构状态说明')
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**✅ 激活状态**")
            st.write("- 参与自动检测")
            st.write("- 显示在API工具中")
            st.write("- 可以正常使用")
        
        with col2:
            st.write("**❌ 停用状态**")
            st.write("- 不参与自动检测")
            st.write("- 不显示在API工具中")
            st.write("- 可以重新激活")
    
    def show_test_function(self):
        st.header('🧪 测试功能')
        
        st.subheader('测试结构检测')
        st.write("在JSON结构管理页面的'测试结构检测'区域：")
        
        test_steps = [
            "1. 输入测试JSON响应",
            "2. 系统自动检测匹配的结构",
            "3. 显示所有激活结构的检测结果",
            "4. 验证结构是否正确"
        ]
        
        for step in test_steps:
            st.write(step)
        
        st.subheader('测试示例')
        test_json = {
            "resultValue": {
                "items": [
                    {"id": 1, "name": "设备1"},
                    {"id": 2, "name": "设备2"}
                ]
            }
        }
        
        st.write("**示例JSON响应：**")
        st.json(test_json)
        
        st.write("**预期检测结果：**")
        st.success("✅ 检测到匹配结构: resultValue.items")
    
    def show_api_integration(self):
        st.header('🔄 在API工具中使用')
        
        st.subheader('自动检测流程')
        steps = [
            "1. 运行API批量请求",
            "2. 系统自动分析第一个响应",
            "3. 使用数据库中的结构进行检测",
            "4. 自动推荐合适的导出路径",
            "5. 显示检测结果和推荐路径"
        ]
        
        for i, step in enumerate(steps, 1):
            st.write(f"{i}. {step}")
        
        st.subheader('导出路径选择')
        st.write("在'结果下载'区域会显示：")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🗄️ 数据库中的结构选项**")
            st.write("- 显示所有激活的结构")
            st.write("- 点击按钮快速选择")
            st.write("- 基于实际检测结果")
        
        with col2:
            st.write("**📋 常见路径选项**")
            st.write("- 预设的常见路径")
            st.write("- 快速选择按钮")
            st.write("- 备用选择方案")
        
        st.subheader('使用建议')
        tips = [
            "💡 优先使用自动检测的推荐路径",
            "💡 如果自动检测失败，手动选择合适路径",
            "💡 可以测试不同路径查看导出结果",
            "💡 添加新的API结构到数据库以便复用"
        ]
        
        for tip in tips:
            st.write(tip)
    
    def show_faq(self):
        st.header('❓ 常见问题')
        
        faqs = [
            {
                "question": "如何添加新的JSON结构？",
                "answer": "在JSON结构管理页面的侧边栏填写结构信息，包括名称、描述、路径模式和可选的示例响应，然后点击'添加结构'按钮。"
            },
            {
                "question": "自动检测失败怎么办？",
                "answer": "检查JSON响应格式是否正确，确认路径模式是否匹配实际结构，使用测试功能验证结构，或者手动选择导出路径。"
            },
            {
                "question": "可以删除预设结构吗？",
                "answer": "可以，但建议先停用而不是删除，因为预设结构通常适用于大多数情况。"
            },
            {
                "question": "数据库文件在哪里？",
                "answer": "数据库文件是 json_structures.db，存储在项目根目录下。"
            },
            {
                "question": "如何备份和恢复结构？",
                "answer": "可以复制 json_structures.db 文件来备份，或者导出结构信息到JSON文件。"
            },
            {
                "question": "支持多深的嵌套结构？",
                "answer": "支持任意深度的嵌套结构，路径模式使用点号分隔，如 'response.data.items.details'。"
            }
        ]
        
        for i, faq in enumerate(faqs):
            with st.expander(f"Q{i+1}: {faq['question']}", expanded=False):
                st.write(f"**A:** {faq['answer']}")
    
    def show_examples(self):
        st.header('📝 示例演示')
        
        st.subheader('常见JSON结构示例')
        
        examples = [
            {
                "name": "ResultValue结构",
                "description": "常见的API响应结构",
                "json": {
                    "resultValue": {
                        "items": [
                            {"id": 1, "name": "设备1", "status": "active"},
                            {"id": 2, "name": "设备2", "status": "inactive"}
                        ]
                    }
                },
                "path": "resultValue.items"
            },
            {
                "name": "Data结构",
                "description": "标准的数据结构",
                "json": {
                    "data": {
                        "items": [
                            {"id": 1, "title": "标题1", "content": "内容1"},
                            {"id": 2, "title": "标题2", "content": "内容2"}
                        ]
                    }
                },
                "path": "data.items"
            },
            {
                "name": "Result结构",
                "description": "结果包装结构",
                "json": {
                    "result": {
                        "data": [
                            {"id": 1, "value": 100},
                            {"id": 2, "value": 200}
                        ]
                    }
                },
                "path": "result.data"
            }
        ]
        
        for example in examples:
            with st.expander(f"📋 {example['name']}", expanded=False):
                st.write(f"**描述**: {example['description']}")
                st.write(f"**路径模式**: `{example['path']}`")
                st.write("**JSON结构**:")
                st.json(example['json'])
        
        st.subheader('交互式测试')
        st.write("你可以在这里测试JSON结构检测：")
        
        test_json = st.text_area(
            "输入测试JSON",
            value='{"resultValue": {"items": [{"id": 1, "name": "test"}]}}',
            height=150
        )
        
        if st.button("🔍 测试检测"):
            try:
                data = json.loads(test_json)
                detected = self.db.auto_detect_structure(data)
                if detected:
                    st.success(f"✅ 检测到匹配结构: `{detected}`")
                else:
                    st.warning("❌ 未检测到匹配的结构")
            except json.JSONDecodeError:
                st.error("❌ 无效的JSON格式")
            except Exception as e:
                st.error(f"❌ 检测失败: {e}")

def main():
    help_page = HelpPage()
    help_page.show_interface()

if __name__ == "__main__":
    main() 